#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import json
import argparse
import re
from collections import defaultdict


def get_status_symbol(status):
    return "✅" if status == "pass" else "❌"


def extract_file_info(filename):
    opt_level = re.search(r'O(\d)', filename)
    opt_level = opt_level.group(1) if opt_level else None
    inline = "inline" if "inline" in filename else "no_inline"
    return opt_level, inline


def get_column_index(opt_level, inline):
    return {
        ("0", "inline"): 3,
        ("0", "no_inline"): 4,
        ("1", "inline"): 5,
        ("1", "no_inline"): 6,
        ("2", "inline"): 7,
        ("2", "no_inline"): 8
    }.get((opt_level, inline))


def main():
    parser = argparse.ArgumentParser(
        description="Generate summary from JSON files")
    parser.add_argument('files', nargs='+', help='JSON files to process')
    args = parser.parse_args()

    rows = defaultdict(lambda: [""] * 9)

    for file in args.files:
        opt_level, inline = extract_file_info(file)
        col_index = get_column_index(opt_level, inline)

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for case_result in data['case_results']:
            source_file = case_result['source_file']
            start_line = case_result['start_line']
            end_line = case_result['end_line']
            func = f"{case_result['function']}[{start_line}-{end_line}]"

            for result in case_result['results']:
                line = result['line_number']
                status = result['status']

                case = source_file
                key = (case, func, line)

                if rows[key][0] == "":
                    rows[key] = [case, func, str(line)] + [""] * 6

                rows[key][col_index] = get_status_symbol(status)

    print("| Case | Function | Line | inline -O0 | -O0 | inline -O1 | -O1 | inline -O2 | -O2 |")
    print("|------|----------|------|------------|-----|------------|-----|------------|-----|")

    sorted_rows = sorted(rows.items(), key=lambda x: (x[0][0], int(x[0][2])))
    for (case, func, line), row in sorted_rows:
        print(f"| {case} | {func} | {line} | {' | '.join(row[3:])} |")


if __name__ == "__main__":
    main()
