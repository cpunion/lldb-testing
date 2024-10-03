#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import os
import os.path
import subprocess
import sys
import glob
import argparse
import json
import multiprocessing
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
    TestConfig(name="inline -O0", opt="0", inline="1",
               file_prefix="test_inline_O0"),
    TestConfig(name="-O0", opt="0", inline="0", file_prefix="test_O0"),
    TestConfig(name="inline -O1", opt="1", inline="1",
               file_prefix="test_inline_O1"),
    TestConfig(name="-O1", opt="1", inline="0", file_prefix="test_O1"),
    TestConfig(name="inline -O2", opt="2", inline="1",
               file_prefix="test_inline_O2"),
    TestConfig(name="-O2", opt="2", inline="0", file_prefix="test_O2"),
    TestConfig(name="inline O2_O0", opt="O2_O0",
               inline="1", file_prefix="test_inline_O2_O0"),
    TestConfig(name="O2_O0", opt="O2_O0",
               inline="0", file_prefix="test_O2_O0"),
    TestConfig(name="inline O2_llc", opt="O2_llc",
               inline="1", file_prefix="test_inline_O2_llc"),
    TestConfig(name="O2_llc", opt="O2_llc",
               inline="0", file_prefix="test_O2_llc"),
    TestConfig(name="inline O0_llc", opt="O0_llc",
               inline="1", file_prefix="test_inline_O0_llc"),
    TestConfig(name="O0_llc", opt="O0_llc",
               inline="0", file_prefix="test_O0_llc"),
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


def get_tool_path(clang_path: str, tool_name: str) -> str:
    if not os.path.exists(clang_path):
        return tool_name

    clang_dir = os.path.dirname(clang_path)
    tool_path = os.path.join(clang_dir, tool_name)

    if os.path.exists(tool_path):
        return tool_path
    else:
        return tool_name


def build_single_config(args: Tuple[int, TestConfig, str, str, str]) -> None:
    i, t, clang_path, llc_path, dsymutil_path = args
    env = os.environ.copy()
    env['CC'] = clang_path

    out_file = t.get_output_file(i, "out", BUILD_DIR)
    ll_file = t.get_output_file(i, "ll", BUILD_DIR)

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    os.makedirs(os.path.dirname(ll_file), exist_ok=True)

    if t.opt == "O2_O0":
        intermediate_ll_file = t.get_output_file(i, "ll", BUILD_DIR)
        execute([
            clang_path, CFLAGS, "-O2",
            f"-DTEST_INLINE={t.inline}",
            "-S", "-emit-llvm", "-o", intermediate_ll_file, SOURCE
        ], env=env)
        execute([clang_path, CFLAGS, "-O0", "-o",
                out_file, intermediate_ll_file], env=env)
    elif t.opt in ["O2_llc", "O0_llc"]:
        intermediate_ll_file = t.get_output_file(i, "ll", BUILD_DIR)
        o_file = t.get_output_file(i, "o", BUILD_DIR)
        opt_level = "2" if t.opt == "O2_llc" else "0"
        execute([
            clang_path, CFLAGS, f"-O{opt_level}",
            f"-DTEST_INLINE={t.inline}",
            "-S", "-emit-llvm", "-o", intermediate_ll_file, SOURCE
        ], env=env)
        execute([llc_path, "-filetype=obj", "-o", o_file,
                intermediate_ll_file], env=env)
        execute([clang_path, CFLAGS, "-O0",
                "-o", out_file, o_file], env=env)
        execute([dsymutil_path, out_file], env=env)
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


def build(clang_versions: List[str]) -> None:
    build_args = []
    for i, clang_path in enumerate(clang_versions):
        print(f"Preparing build for {clang_path}")
        llc_path = get_tool_path(clang_path, "llc")
        dsymutil_path = get_tool_path(clang_path, "dsymutil")
        for t in TEST_MATRIX:
            build_args.append((i, t, clang_path, llc_path, dsymutil_path))

    with multiprocessing.Pool() as pool:
        pool.map(build_single_config, build_args)


def run_single_test(args: Tuple[int, TestConfig, str]) -> None:
    i, t, clang_path = args
    env = os.environ.copy()
    env['CC'] = clang_path

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
        print(f"Error occurred while testing {out_file}", file=sys.stderr)


def test(clang_versions: List[str]) -> None:
    test_args = [(i, t, clang_path)
                 for i, clang_path in enumerate(clang_versions)
                 for t in TEST_MATRIX]

    with multiprocessing.Pool() as pool:
        pool.map(run_single_test, test_args)


def report(clang_versions: List[str]) -> None:
    print("Generating summary...")

    all_results: Dict[str, Dict[str, Dict]] = {}

    for clang_path in clang_versions:
        all_results[clang_path] = {}
        for t in TEST_MATRIX:
            result_file = t.get_output_file(
                clang_versions.index(clang_path), "json", RESULTS_DIR)
            with open(result_file, 'r', encoding="utf-8") as json_file:
                all_results[clang_path][t.name] = json.load(json_file)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# clang test summary\n\n")

        f.write("## O2_O0 test\n\n")
        f.write(
            "The O2_O0 test used in this test consists of the following commands:\n\n")
        f.write("```shell\n")
        f.write(f"{CC} {CFLAGS} -O2 -DTEST_INLINE=$(INLINE) -S -emit-llvm \\\n")
        f.write(f"    -o {BUILD_DIR}/temp_$(INLINE).ll {SOURCE}\n")
        f.write(
            f"clang {CFLAGS} -O0 -o {BUILD_DIR}/test$(if $(filter 1,$(INLINE)),_inline)_O2_O0.out \\\n")
        f.write(f"    {BUILD_DIR}/temp_$(INLINE).ll\n")
        f.write("```\n\n")
        f.write("`INLINE` is `1` or `0`.\n\n")

        f.write("## O2_llc and O0_llc tests\n\n")
        f.write(
            "The O2_llc and O0_llc tests used in this test consist of the following commands:\n\n")
        f.write("```shell\n")
        f.write(
            f"clang {CFLAGS} -O$(OPT) -DTEST_INLINE=$(INLINE) -S -emit-llvm \\\n")
        f.write(f"    -o {BUILD_DIR}/temp_$(INLINE).ll {SOURCE}\n")
        f.write(
            f"llc -filetype=obj -o {BUILD_DIR}/temp_$(INLINE).o {BUILD_DIR}/temp_$(INLINE).ll\n")
        f.write(
            f"clang {CFLAGS} -O0 -o {BUILD_DIR}/test$(if $(filter 1,$(INLINE)),_inline)_O$(OPT)_llc.out \\\n")
        f.write(f"    {BUILD_DIR}/temp_$(INLINE).o\n")
        f.write(
            f"dsymutil {BUILD_DIR}/test$(if $(filter 1,$(INLINE)),_inline)_O$(OPT)_llc.out\n")
        f.write("```\n\n")
        f.write(
            "`INLINE` is `1` or `0`, and `OPT` is `2` for O2_llc or `0` for O0_llc.\n\n")

        f.write("## Test results\n\n")
        for i, clang_path in enumerate(clang_versions):
            version_results = {col: {"failed": 0, "total": 0}
                               for col in COLUMNS}

            for t in TEST_MATRIX:
                result_file = t.get_output_file(i, "json", RESULTS_DIR)
                with open(result_file, 'r', encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    version_results[t.name]["failed"] += data.get('failed', 0)
                    version_results[t.name]["total"] += data.get('total', 0)

            failed = sum(version_results[col]['failed'] for col in COLUMNS)
            total = sum(version_results[col]['total'] for col in COLUMNS)
            f.write(f"Version {i} failed: {failed}/{total}\n\n")
            f.write("| " + " | ".join(COLUMNS) + " |\n")
            f.write("| " + " | ".join(["---" for _ in COLUMNS]) + " |\n")
            f.write(
                "| " + " | ".join([f"{version_results[col]['failed']}/{version_results[col]['total']}" for col in COLUMNS]) + " |\n\n")

            clang_version = subprocess.check_output(
                [clang_path, "--version"]).decode().strip()
            f.write("```\n")
            f.write(f"{clang_version}\n")
            f.write("```\n\n")

        f.write("## Detailed results\n\n")
        processed_results = process_results(
            all_results, clang_versions, COLUMNS)
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
