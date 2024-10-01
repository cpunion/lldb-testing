#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import argparse
import json
import os
import subprocess
import sys


def print_help():
    print(
        "Usage: runtest.py [-v] [-i] [-p plugin_path] -r result_file <target_path> <file1> [<file2> ...]")
    print("target_path: The path to the target executable")
    print("-r result_file: The path to save the JSON result")
    print("file1, file2, ...: List of source files to process")


def run_tests(args):
    lldb_path = os.environ.get('LLDB_PATH', 'lldb')
    python_script = os.path.join(os.path.dirname(__file__), "test.py")

    lldb_commands = [
        f"command script import {python_script}",
        f"script test.run_tests_with_result('{args.target_path}', {args.file_list}, {args.verbose}, {args.interactive}, '{args.result}')",
        "quit"
    ]

    lldb_command = [lldb_path] + sum([['-o', cmd]
                                     for cmd in lldb_commands], [])

    subprocess.run(lldb_command, check=True)


def process_result(result_file):
    try:
        with open(result_file, 'r') as f:
            data = json.load(f)

        if 'error' in data:
            print(f"Error occurred: {data['error']}")
            return 2

        total_tests = data['total']
        failed_tests = data['failed']

        print(f"Total tests: {total_tests}")
        print(f"Failed tests: {failed_tests}")

        return 1 if failed_tests > 0 else 0
    except FileNotFoundError:
        print(f"Error: Could not find result file {result_file}")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in result file {result_file}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Run LLDB tests")
    parser.add_argument('-v', '--verbose',
                        action='store_true', help="Verbose mode")
    parser.add_argument('-i', '--interactive',
                        action='store_true', help="Interactive mode")
    parser.add_argument('-r', '--result', required=True,
                        help="Path to save the JSON result")
    parser.add_argument('target_path', help="Path to the target executable")
    parser.add_argument('file_list', nargs='+',
                        help="List of source files to process")

    args = parser.parse_args()

    run_tests(args)
    sys.exit(process_result(args.result))


if __name__ == "__main__":
    main()
