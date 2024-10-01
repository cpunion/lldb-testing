#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import json
import argparse
import sys
from collections import defaultdict


def get_status_symbol(status):
    return "✅" if status == "pass" else "❌"


def main():
    parser = argparse.ArgumentParser(
        description="Generate summary from JSON files")
    parser.add_argument('files', nargs='+', help='JSON files to process')
    parser.add_argument('--columns', help='Column names separated by commas')
    args = parser.parse_args()

    columns = args.columns.split(',')

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
                key = (func, loc)

                if rows[key][0] == "":
                    rows[key] = [func, loc] + [""] * len(columns)

                rows[key][file_index + 2] = get_status_symbol(status)

    print(f"| Function | Loc | {' | '.join(columns)} |")
    print(f"|----------|-----|{' | '.join(['-----' for _ in columns])}|")

    sorted_rows = sorted(rows.items(), key=lambda x: (
        x[0][1].split(':')[0], int(x[0][1].split(':')[1])))
    for (func, loc), row in sorted_rows:
        print(f"| {func} | {loc} | {' | '.join(row[2:])} |")


if __name__ == "__main__":
    main()
