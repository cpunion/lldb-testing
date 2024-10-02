#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import os
import subprocess
import sys
import glob
import argparse
import json

CC = "clang"
CFLAGS = "-g"
SOURCE = "test.c"
BUILD_DIR = "build"
RESULTS_DIR = "results"

OPTIMIZATION_LEVELS = ["0", "1", "2", "two-step"]
INLINE_OPTIONS = ["0", "1"]


def gen_names(suffix, version_index):
    for opt in OPTIMIZATION_LEVELS:
        for inline in INLINE_OPTIONS:
            inline_str = "_inline" if inline == "1" else ""
            if opt == "two-step":
                yield f"{BUILD_DIR}/{version_index}/test{inline_str}_two-step{suffix}"
            else:
                yield f"{BUILD_DIR}/{version_index}/test{inline_str}_O{opt}{suffix}"


def parse_args():
    parser = argparse.ArgumentParser(description="Run clang tests")
    parser.add_argument('command', nargs='?', default='all',
                        choices=['build', 'test', 'report', 'clean', 'all'],
                        help="Command to execute (default: all)")
    parser.add_argument('--add-clang', action='append',
                        help="Additional clang executable path")
    return parser.parse_args()


def execute(cmd, stdout=None, env=None):
    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, check=True, stdout=stdout, env=env)


def build(clang_versions):
    for i, clang_path in enumerate(clang_versions):
        print(f"Building with {clang_path}")
        env = os.environ.copy()
        env['CC'] = clang_path

        TARGETS = list(gen_names(".out", i))
        LL_TARGETS = list(gen_names(".ll", i))

        for target in TARGETS + LL_TARGETS:
            os.makedirs(os.path.dirname(target), exist_ok=True)

            if "two-step" in target:
                if target.endswith(".out"):
                    ll_file = target[:-4] + ".ll"
                    execute([
                        clang_path, CFLAGS, "-O2",
                        f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                        "-S", "-emit-llvm", "-o", ll_file, SOURCE
                    ], env=env)
                    execute([clang_path, CFLAGS, "-O0",
                            "-o", target, ll_file], env=env)
                else:
                    execute([
                        clang_path, CFLAGS, "-O2",
                        f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                        "-S", "-emit-llvm", "-o", target, SOURCE
                    ], env=env)
            else:
                opt_level = next(c for c in target if c.isdigit())
                if target.endswith(".out"):
                    execute([
                        clang_path, CFLAGS, f"-O{opt_level}",
                        f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                        "-o", target, SOURCE
                    ], env=env)
                else:
                    execute([
                        clang_path, CFLAGS, f"-O{opt_level}",
                        f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                        "-S", "-emit-llvm", "-o", target, SOURCE
                    ], env=env)


def test(clang_versions):
    for i, clang_path in enumerate(clang_versions):
        print(f"Testing with {clang_path}")
        env = os.environ.copy()
        env['CC'] = clang_path

        RESULT_FILES = [t.replace(f"{BUILD_DIR}/{i}/", f"{RESULTS_DIR}/{i}/").replace(
            ".out", ".json") for t in gen_names(".out", i)]

        for result_file in RESULT_FILES:
            os.makedirs(os.path.dirname(result_file), exist_ok=True)
            out_file = result_file.replace(
                RESULTS_DIR, BUILD_DIR).replace(".json", ".out")
            try:
                cmd = ["python", "../runtest.py"]
                if os.environ.get("VERBOSE"):
                    cmd.append("-v")
                cmd.extend(["-r", result_file, out_file, SOURCE])
                execute(cmd, env=env)
            except subprocess.CalledProcessError:
                pass


def report(clang_versions):
    print("Generating summary...")
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
        for i, clang_path in enumerate(clang_versions):
            # Calculate and write summary statistics
            result_files = [t.replace(f"{BUILD_DIR}/{i}/", f"{RESULTS_DIR}/{i}/").replace(
                ".out", ".json") for t in gen_names(".out", i)]
            total_tests = 0
            failed_tests = 0
            for file in result_files:
                if os.path.exists(file):
                    with open(file, 'r', encoding="utf-8") as json_file:
                        data = json.load(json_file)
                        total_tests += data.get('total', 0)
                        failed_tests += data.get('failed', 0)

            f.write(
                f"Version {i} failed: {failed_tests} / {total_tests}:\n\n")
            f.write("```\n")
            clang_version = subprocess.check_output(
                [clang_path, "--version"]).decode().strip()
            f.write(f"{clang_version}\n```\n\n")

    columns = [
        "inline -O0", "-O0",
        "inline -O1", "-O1",
        "inline -O2", "-O2",
        "inline two-step", "two-step"
    ]

    all_result_files = []
    for i in range(len(clang_versions)):
        all_result_files.extend([t.replace(
            f"{BUILD_DIR}/{i}/", f"{RESULTS_DIR}/{i}/").replace(".out", ".json") for t in gen_names(".out", i)])

    cmd = [
        "python", "generate_summary.py"
    ] + all_result_files + [
        "--columns", ",".join(columns),
        "--clang-count", str(len(clang_versions))
    ]

    with open("README.md", "a", encoding="utf-8") as f:
        execute(cmd, stdout=f)

    print("Summary generated in README.md")


def clean():
    for directory in [BUILD_DIR, RESULTS_DIR]:
        if os.path.exists(directory):
            for file in glob.glob(f"{directory}/**/*", recursive=True):
                if os.path.isfile(file):
                    os.remove(file)
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(directory)


def main():
    args = parse_args()
    clang_versions = [CC] + (args.add_clang or [])

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
            f"Usage: {sys.argv[0]} [{{build|test|report|clean|all}}] [--add-clang CLANG_PATH]...")
        sys.exit(1)


if __name__ == "__main__":
    main()
