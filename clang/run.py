#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import os
import subprocess
import sys
import glob

CC = "clang"
CFLAGS = "-g"
SOURCE = "test.c"
BUILD_DIR = "build"
RESULTS_DIR = "results"

OPTIMIZATION_LEVELS = ["0", "1", "2", "two-step"]
INLINE_OPTIONS = ["0", "1"]


def gen_names(suffix):
    for opt in OPTIMIZATION_LEVELS:
        for inline in INLINE_OPTIONS:
            inline_str = "_inline" if inline == "1" else ""
            if opt == "two-step":
                yield f"{BUILD_DIR}/test{inline_str}_two-step{suffix}"
            else:
                yield f"{BUILD_DIR}/test{inline_str}_O{opt}{suffix}"


TARGETS = list(gen_names(".out"))
LL_TARGETS = list(gen_names(".ll"))
RESULT_FILES = [t.replace(
    f"{BUILD_DIR}/", f"{RESULTS_DIR}/").replace(".out", ".json") for t in TARGETS]


def execute(cmd, stdout=None):
    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, check=True, stdout=stdout)


def build():
    os.makedirs(BUILD_DIR, exist_ok=True)

    for target in TARGETS + LL_TARGETS:
        if "two-step" in target:
            if target.endswith(".out"):
                ll_file = target[:-4] + ".ll"
                execute([
                    CC, CFLAGS, "-O2",
                    f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                    "-S", "-emit-llvm", "-o", ll_file, SOURCE
                ])
                execute([CC, CFLAGS, "-O0", "-o", target, ll_file])
            else:
                execute([
                    CC, CFLAGS, "-O2",
                    f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                    "-S", "-emit-llvm", "-o", target, SOURCE
                ])
        else:
            opt_level = next(c for c in target if c.isdigit())
            if target.endswith(".out"):
                execute([
                    CC, CFLAGS, f"-O{opt_level}",
                    f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                    "-o", target, SOURCE
                ])
            else:
                execute([
                    CC, CFLAGS, f"-O{opt_level}",
                    f"-DTEST_INLINE={1 if '_inline' in target else 0}",
                    "-S", "-emit-llvm", "-o", target, SOURCE
                ])


def test():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    for result_file in RESULT_FILES:
        out_file = result_file.replace(
            f"{RESULTS_DIR}/", f"{BUILD_DIR}/").replace(".json", ".out")
        try:
            cmd = ["python", "../runtest.py"]
            if os.environ.get("VERBOSE"):
                cmd.append("-v")
            cmd.extend(["-r", result_file, out_file, SOURCE])
            execute(cmd)
        except subprocess.CalledProcessError:
            pass


def report():
    print("Generating summary...")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# clang test summary\n\n")
        f.write("## clang --version\n\n")
        clang_version = subprocess.check_output(
            [CC, "--version"]).decode().strip()
        f.write(f"```\n{clang_version}\n```\n\n")
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

    columns = [
        "inline -O0", "-O0",
        "inline -O1", "-O1",
        "inline -O2", "-O2",
        "inline two-step", "two-step"
    ]

    cmd = [
        "python", "generate_summary.py"
    ] + RESULT_FILES + [
        "--columns", ",".join(columns)
    ]

    with open("README.md", "a", encoding="utf-8") as f:
        execute(cmd, stdout=f)

    print("Summary generated in README.md")


def clean():
    for directory in [BUILD_DIR, RESULTS_DIR]:
        if os.path.exists(directory):
            for file in glob.glob(f"{directory}/*"):
                os.remove(file)
            os.rmdir(directory)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "all"

    if command == "build":
        build()
    elif command == "test":
        test()
    elif command == "report":
        report()
    elif command == "clean":
        clean()
    elif command == "all":
        build()
        test()
        report()
    else:
        print(f"Usage: {sys.argv[0]} {{build|test|report|clean|all}}")
        sys.exit(1)


if __name__ == "__main__":
    main()
