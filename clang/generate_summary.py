#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import json
import argparse
import sys
from collections import defaultdict


def get_status_symbol(status):
    return "✅" if status == "pass" else "❌"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='JSON files to process')
    parser.add_argument('--columns', help='Column names separated by commas')
    parser.add_argument('--clang-count', type=int, default=1,
                        help="Number of clang versions tested")
    return parser.parse_args()


def main():
    args = parse_args()

    columns = args.columns.split(',')
    clang_count = args.clang_count

    # +2 for Function and loc
    rows = defaultdict(lambda: [""] * (len(columns) + 2))

    for file_index, file in enumerate(args.files):
        print(f"Processing file: {file}", file=sys.stderr)

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for case_result in data['case_results']:
            source_file = case_result['source_file']
            func = case_result['function']

            for result in case_result['results']:
                line = result['line_number']
                status = result['status']

                loc = f"{source_file}:{line}"
                key = (source_file, int(line), func)

                if rows[key][0] == "":
                    rows[key] = [func, loc] + ["" for _ in columns]

                col_index = (file_index // clang_count) + 2
                clang_index = file_index % clang_count
                rows[key][col_index] += get_status_symbol(status)

    print(f"| Function | Loc | {' | '.join(columns)} |")
    print(f"|----------|-----|{' | '.join(['-----' for _ in columns])}|")

    for key in sorted(rows.keys()):
        row = rows[key]
        func, loc = row[:2]
        results = row[2:]
        print(f"| {func} | {loc} | {' | '.join(results)} |")


if __name__ == "__main__":
    main()
