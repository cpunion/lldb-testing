#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import os
import subprocess
import sys
import glob
import argparse
import json
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass
from generate_summary import process_results, print_summary_table


CC = "clang"
CFLAGS = "-g"
SOURCE = "test.c"
BUILD_DIR = "build"
RESULTS_DIR = "results"


@dataclass
class TestConfig:
    name: str
    opt: str
    inline: str
    file_prefix: str

    def get_output_file(self, version_index: int, ext: str, output_dir: str) -> str:
        return f"{output_dir}/{version_index}/{self.file_prefix}.{ext}"


TEST_MATRIX = [
    TestConfig("inline -O0", "0", "1", "test_inline_O0"),
    TestConfig("-O0", "0", "0", "test_O0"),
    TestConfig("inline -O1", "1", "1", "test_inline_O1"),
    TestConfig("-O1", "1", "0", "test_O1"),
    TestConfig("inline -O2", "2", "1", "test_inline_O2"),
    TestConfig("-O2", "2", "0", "test_O2"),
    TestConfig("inline two-step", "two-step", "1", "test_inline_two-step"),
    TestConfig("two-step", "two-step", "0", "test_two-step"),
]

COLUMNS = [test.name for test in TEST_MATRIX]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run clang tests")
    parser.add_argument('command', nargs='?', default='all',
                        choices=['build', 'test', 'report', 'clean', 'all'],
                        help="Command to execute (default: all)")
    parser.add_argument('--clang', action='append', metavar='CLANG_PATH',
                        help="Clang executable path(s). Can be specified multiple times.")
    return parser.parse_args()


def execute(cmd: List[str], stdout: Optional[Any] = None,
            env: Optional[Dict[str, str]] = None) -> None:
    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, check=True, stdout=stdout, env=env)


def build(clang_versions: List[str]) -> None:
    for i, clang_path in enumerate(clang_versions):
        print(f"Building with {clang_path}")
        env = os.environ.copy()
        env['CC'] = clang_path

        for t in TEST_MATRIX:
            out_file = t.get_output_file(i, "out", BUILD_DIR)
            ll_file = t.get_output_file(i, "ll", BUILD_DIR)

            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            os.makedirs(os.path.dirname(ll_file), exist_ok=True)

            if t.opt == "two-step":
                intermediate_ll_file = t.get_output_file(i, "ll", BUILD_DIR)
                execute([
                    clang_path, CFLAGS, "-O2",
                    f"-DTEST_INLINE={t.inline}",
                    "-S", "-emit-llvm", "-o", intermediate_ll_file, SOURCE
                ], env=env)
                execute([clang_path, CFLAGS, "-O0", "-o",
                        out_file, intermediate_ll_file], env=env)
            else:
                execute([
                    clang_path, CFLAGS, f"-O{t.opt}",
                    f"-DTEST_INLINE={t.inline}",
                    "-o", out_file, SOURCE
                ], env=env)
                execute([
                    clang_path, CFLAGS, f"-O{t.opt}",
                    f"-DTEST_INLINE={t.inline}",
                    "-S", "-emit-llvm", "-o", ll_file, SOURCE
                ], env=env)


def test(clang_versions: List[str]) -> None:
    for i, clang_path in enumerate(clang_versions):
        print(f"Testing with {clang_path}")
        env = os.environ.copy()
        env['CC'] = clang_path

        for t in TEST_MATRIX:
            out_file = t.get_output_file(i, "out", BUILD_DIR)
            result_file = t.get_output_file(i, "json", RESULTS_DIR)

            os.makedirs(os.path.dirname(result_file), exist_ok=True)

            try:
                cmd = ["python", "../runtest.py"]
                if os.environ.get("VERBOSE"):
                    cmd.append("-v")
                cmd.extend(["-r", result_file, out_file, SOURCE])
                execute(cmd, env=env)
            except subprocess.CalledProcessError:
                print(
                    f"Error occurred while testing {out_file}", file=sys.stderr)


def report(clang_versions: List[str]) -> None:
    print("Generating summary...")

    all_results: List[Dict[str, Any]] = []
    version_summaries: List[Tuple[int, str, Dict[str, Dict[str, int]]]] = []

    for i, clang_path in enumerate(clang_versions):
        version_results = {col: {"failed": 0, "total": 0} for col in COLUMNS}

        for t in TEST_MATRIX:
            result_file = t.get_output_file(i, "json", RESULTS_DIR)

            if os.path.exists(result_file):
                with open(result_file, 'r', encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    version_results[t.name]["failed"] += data.get('failed', 0)
                    version_results[t.name]["total"] += data.get('total', 0)
                all_results.append(data)

        version_summaries.append((i, clang_path, version_results))

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# clang test summary\n\n")

        f.write("## Two-step test\n\n")
        f.write(
            "The two-step test used in this test consists of the following commands:\n\n")
        f.write("```shell\n")
        f.write(f"{CC} {CFLAGS} -O2 -DTEST_INLINE=$(INLINE) -S -emit-llvm \\\n")
        f.write(f"    -o {BUILD_DIR}/temp_$(INLINE).ll {SOURCE}\n")
        f.write(
            f"{CC} {CFLAGS} -O0 -o {BUILD_DIR}/test$(if $(filter 1,$(INLINE)),_inline)_two-step.out \\\n")
        f.write(f"    {BUILD_DIR}/temp_$(INLINE).ll\n")
        f.write("```\n\n")
        f.write("`INLINE` is `1` or `0`.\n\n")

        f.write("## Test results\n\n")
        for i, clang_path, rs in version_summaries:
            failed = sum(rs[col]['failed'] for col in COLUMNS)
            total = sum(rs[col]['total'] for col in COLUMNS)
            f.write(f"Version {i} failed: {failed}/{total}\n\n")
            f.write("| " + " | ".join(COLUMNS) + " |\n")
            f.write("| " + " | ".join(["---" for _ in COLUMNS]) + " |\n")
            f.write(
                "| " + " | ".join([f"{rs[col]['failed']}/{rs[col]['total']}" for col in COLUMNS]) + " |\n\n")

            clang_version = subprocess.check_output(
                [clang_path, "--version"]).decode().strip()
            f.write("```\n")
            f.write(f"{clang_version}\n")
            f.write("```\n\n")

        f.write("## Detailed results\n\n")
        processed_results = process_results(
            all_results, COLUMNS, len(clang_versions))
        print_summary_table(processed_results, COLUMNS, file=f)

    print("Summary generated in README.md")


def clean() -> None:
    for directory in [BUILD_DIR, RESULTS_DIR]:
        if os.path.exists(directory):
            for file in glob.glob(f"{directory}/**/*", recursive=True):
                if os.path.isfile(file):
                    os.remove(file)
            for root, dirs, _ in os.walk(directory, topdown=False):
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(directory)


def main() -> None:
    args = parse_args()
    clang_versions = args.clang if args.clang else [CC]

    if args.command == "build":
        build(clang_versions)
    elif args.command == "test":
        test(clang_versions)
    elif args.command == "report":
        report(clang_versions)
    elif args.command == "clean":
        clean()
    elif args.command == "all":
        build(clang_versions)
        test(clang_versions)
        report(clang_versions)
    else:
        print(
            f"Usage: {sys.argv[0]} [{{build|test|report|clean|all}}] [--clang CLANG_PATH]...")
        print("Note: --clang can be specified multiple times for different clang versions.")
        sys.exit(1)


if __name__ == "__main__":
    main()
