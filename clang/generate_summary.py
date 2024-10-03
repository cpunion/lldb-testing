#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from collections import defaultdict
from typing import List, Dict, Tuple, DefaultDict, TextIO, Optional


def get_status_symbol(status: str) -> str:
    return "✅" if status == "pass" else "❌"


def process_results(all_results: Dict[str, Dict[str, Dict]],
                    clang_versions: List[str],
                    columns: List[str]
                    ) -> DefaultDict[Tuple[str, int, str], List[str]]:
    rows: DefaultDict[Tuple[str, int, str], List[str]
                      ] = defaultdict(lambda: [""] * (len(columns) + 2))

    for _, version in enumerate(clang_versions):
        for column in columns:
            data = all_results[version][column]
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

                    col_index = columns.index(column) + 2
                    rows[key][col_index] += get_status_symbol(status)

    return rows


def print_summary_table(rows: Dict[Tuple[str, int, str], List[str]], columns: List[str],
                        file: Optional[TextIO] = None) -> None:
    print(f"| Function | Loc | {' | '.join(columns)} |", file=file)
    print(
        f"|----------|-----|{' | '.join(['-----' for _ in columns])}|", file=file)

    for key in sorted(rows.keys()):
        row = rows[key]
        func, loc = row[:2]
        results = row[2:]
        print(f"| {func} | {loc} | {' | '.join(results)} |", file=file)
