# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import os
import sys
import argparse
import signal
import json
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict, Any, Union
import lldb


def log(*args: Any, **kwargs: Any) -> None:
    print(*args, **kwargs, flush=True)


class LLDBTestException(Exception):
    pass


@dataclass
class Test:
    source_file: str
    line_number: int
    variable: str
    expected_value: str


@dataclass
class TestResult:
    test: Test
    status: str
    actual: Optional[Union[str, Set[str]]] = None
    message: Optional[str] = None
    missing: Optional[Set[str]] = None
    extra: Optional[Set[str]] = None


@dataclass
class TestCase:
    source_file: str
    start_line: int
    end_line: int
    tests: List[Test]


@dataclass
class CaseResult:
    test_case: TestCase
    function: str
    results: List[TestResult]


@dataclass
class TestResults:
    total: int = 0
    passed: int = 0
    failed: int = 0
    case_results: List[CaseResult] = field(default_factory=list)


class LLDBDebugger:
    def __init__(self, executable_path: str) -> None:
        self.executable_path: str = executable_path
        self.debugger: lldb.SBDebugger = lldb.SBDebugger.Create()
        self.debugger.SetAsync(False)
        self.target: Optional[lldb.SBTarget] = None
        self.process: Optional[lldb.SBProcess] = None
        self.type_mapping: Dict[str, str] = {
            'long': 'int',
            'unsigned long': 'uint',
        }

    def setup(self) -> None:
        self.target = self.debugger.CreateTarget(self.executable_path)
        if not self.target:
            raise LLDBTestException(
                f"Failed to create target for {self.executable_path}")

    def set_breakpoint(self, file_spec: str, line_number: int) -> lldb.SBBreakpoint:
        bp = self.target.BreakpointCreateByLocation(file_spec, line_number)
        if not bp.IsValid():
            raise LLDBTestException(
                f"Failed to set breakpoint at {file_spec}: {line_number}")
        return bp

    def run_to_breakpoint(self) -> None:
        if not self.process:
            self.process = self.target.LaunchSimple(None, None, os.getcwd())
        else:
            self.process.Continue()
        if self.process.GetState() != lldb.eStateStopped:
            raise LLDBTestException("Process didn't stop at breakpoint")

    def get_variable_value(self, var_expression: str) -> Optional[str]:
        frame = self.process.GetSelectedThread().GetFrameAtIndex(0)
        value = frame.EvaluateExpression(var_expression)
        if value and value.IsValid():
            return self.format_value(value)
        return None

    def format_value(self, value: lldb.SBValue) -> str:
        if value.GetType().IsPointerType():
            return f"({value.GetType()}) {value.GetValue()}"
        elif value.GetType().IsArrayType():
            return f"({value.GetType()}) {value.GetValue()}"
        else:
            return str(value.GetValue())

    def get_all_variable_names(self) -> Set[str]:
        frame = self.process.GetSelectedThread().GetFrameAtIndex(0)
        return set(var.GetName() for var in frame.GetVariables(True, True, True, True))

    def get_current_function_name(self) -> str:
        frame = self.process.GetSelectedThread().GetFrameAtIndex(0)
        return frame.GetFunctionName()

    def cleanup(self) -> None:
        if self.process and self.process.IsValid():
            self.process.Kill()
        lldb.SBDebugger.Destroy(self.debugger)

    def run_console(self) -> bool:
        log("\nEntering LLDB interactive mode.")
        log("Type 'quit' to exit and continue with the next test case.")
        log("Use Ctrl+D to exit and continue, or Ctrl+C to abort all tests.")

        old_stdin, old_stdout, old_stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = sys.__stdin__, sys.__stdout__, sys.__stderr__

        self.debugger.SetAsync(True)
        self.debugger.HandleCommand("settings set auto-confirm true")
        self.debugger.HandleCommand("command script import lldb")

        interpreter = self.debugger.GetCommandInterpreter()
        continue_tests = True

        def keyboard_interrupt_handler(_sig: Any, _frame: Any) -> None:
            nonlocal continue_tests
            log("\nTest execution aborted by user.")
            continue_tests = False
            raise KeyboardInterrupt

        original_handler = signal.signal(
            signal.SIGINT, keyboard_interrupt_handler)

        try:
            while continue_tests:
                log("\n(lldb) ", end="")
                try:
                    command = input().strip()
                except EOFError:
                    log("\nExiting LLDB interactive mode. Continuing with next test case.")
                    break
                except KeyboardInterrupt:
                    break

                if command.lower() == 'quit':
                    log("\nExiting LLDB interactive mode. Continuing with next test case.")
                    break

                result = lldb.SBCommandReturnObject()
                interpreter.HandleCommand(command, result)
                log(result.GetOutput().rstrip() if result.Succeeded()
                    else result.GetError().rstrip())

        finally:
            signal.signal(signal.SIGINT, original_handler)
            sys.stdin, sys.stdout, sys.stderr = old_stdin, old_stdout, old_stderr

        return continue_tests


def parse_expected_values(source_files: List[str]) -> List[TestCase]:
    test_cases: List[TestCase] = []
    for source_file in source_files:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            i = 0
            while i < len(content):
                line = content[i].strip()
                if line.startswith('// Expected:'):
                    start_line = i + 1
                    tests: List[Test] = []
                    i += 1
                    while i < len(content):
                        line = content[i].strip()
                        if not line.startswith('//'):
                            break
                        parts = line.lstrip('//').strip().split(':', 1)
                        if len(parts) == 2:
                            var, value = map(str.strip, parts)
                            tests.append(Test(source_file, i + 1, var, value))
                        i += 1
                    end_line = i
                    test_cases.append(
                        TestCase(source_file, start_line, end_line, tests))
                else:
                    i += 1
    return test_cases


def execute_tests(executable_path: str, test_cases: List[TestCase],
                  verbose: bool, interactive: bool) -> TestResults:
    results = TestResults()

    for test_case in test_cases:
        debugger = LLDBDebugger(executable_path)
        try:
            if verbose:
                log(
                    f"\nSetting breakpoint at {test_case.source_file}:{test_case.end_line}")
            debugger.setup()
            debugger.set_breakpoint(test_case.source_file, test_case.end_line)
            debugger.run_to_breakpoint()

            all_variable_names = debugger.get_all_variable_names()

            case_result = execute_test_case(
                debugger, test_case, all_variable_names)

            results.total += len(case_result.results)
            results.passed += sum(1 for r in case_result.results if r.status == 'pass')
            results.failed += sum(1 for r in case_result.results if r.status != 'pass')
            results.case_results.append(case_result)

            case = case_result.test_case
            loc = f"{case.source_file}:{case.start_line}-{case.end_line}"
            if verbose or interactive or any(r.status != 'pass' for r in case_result.results):
                log(f"\nTest case: {loc} in function '{case_result.function}'")
            for result in case_result.results:
                print_test_result(result, verbose=verbose)

            if interactive and any(r.status != 'pass' for r in case_result.results):
                log("\nTest case failed. Entering LLDB interactive mode.")
                continue_tests = debugger.run_console()
                if not continue_tests:
                    log("Aborting all tests.")
                    break

        finally:
            debugger.cleanup()

    return results


def execute_test_case(debugger: LLDBDebugger, test_case: TestCase,
                      all_variable_names: Set[str]) -> CaseResult:
    results: List[TestResult] = []

    for test in test_case.tests:
        if test.variable == "all variables":
            result = execute_all_variables_test(test, all_variable_names)
        else:
            result = execute_single_variable_test(debugger, test)
        results.append(result)

    return CaseResult(test_case, debugger.get_current_function_name(), results)


def execute_all_variables_test(test: Test, all_variable_names: Set[str]) -> TestResult:
    expected_vars = set(test.expected_value.split())
    if expected_vars == all_variable_names:
        return TestResult(
            test=test,
            status='pass',
            actual=all_variable_names
        )
    else:
        return TestResult(
            test=test,
            status='fail',
            actual=all_variable_names,
            missing=expected_vars - all_variable_names,
            extra=all_variable_names - expected_vars
        )


def execute_single_variable_test(debugger: LLDBDebugger, test: Test) -> TestResult:
    actual_value = debugger.get_variable_value(test.variable)
    if actual_value is None:
        return TestResult(
            test=test,
            status='error',
            message=f'Unable to fetch value for {test.variable}'
        )

    actual_value = actual_value.strip()
    expected_value = test.expected_value.strip()

    if actual_value == expected_value:
        return TestResult(
            test=test,
            status='pass',
            actual=actual_value
        )
    else:
        return TestResult(
            test=test,
            status='fail',
            actual=actual_value
        )


def print_test_results(results: TestResults) -> None:
    log("\nTest results:")
    log(f"  Total tests: {results.total}")
    log(f"  Passed tests: {results.passed}")
    log(f"  Failed tests: {results.failed}")
    if results.total == results.passed:
        log("All tests passed!")
    else:
        log("Some tests failed")


def print_test_result(result: TestResult, verbose: bool) -> None:
    status_symbol = "✓" if result.status == 'pass' else "✗"
    status_text = "Pass" if result.status == 'pass' else "Fail"
    test = result.test

    if result.status == 'pass':
        if verbose:
            log(f"{status_symbol} Line {test.line_number}, {test.variable}: {status_text}")
            if test.variable == 'all variables':
                log(f"    Variables: {', '.join(sorted(result.actual))}")
    else:  # fail or error
        log(f"{status_symbol} Line {test.line_number}, {test.variable}: {status_text}")
        if test.variable == 'all variables':
            if result.missing:
                log(f"    Missing variables: {', '.join(sorted(result.missing))}")
            if result.extra:
                log(f"    Extra variables: {', '.join(sorted(result.extra))}")
            log(f"    Expected: {', '.join(sorted(test.expected_value.split()))}")
            log(f"    Actual: {', '.join(sorted(result.actual))}")
        elif result.status == 'error':
            log(f"    Error: {result.message}")
        else:
            log(f"    Expected: {test.expected_value}")
            log(f"    Actual: {result.actual}")


def run_tests(executable_path: str, source_files: List[str],
              verbose: bool, interactive: bool) -> int:
    test_cases = parse_expected_values(source_files)
    if verbose:
        log(f"Running tests for {', '.join(source_files)} with {executable_path}")
        log(f"Found {len(test_cases)} test cases")

    results = execute_tests(executable_path, test_cases,
                            verbose, interactive)
    print_test_results(results)

    # Return 0 if all tests passed, 1 otherwise
    return 0 if results.failed == 0 else 1


def run_tests_with_result(executable_path: str, source_files: List[str],
                          verbose: bool, interactive: bool, result_path: str) -> int:
    test_cases = parse_expected_values(source_files)
    if verbose:
        log(f"Running tests for {', '.join(source_files)} with {executable_path}")
        log(f"Found {len(test_cases)} test cases")

    results = execute_tests(executable_path, test_cases,
                            verbose, interactive)

    # Convert results to JSON-serializable format
    json_results = {
        "total": results.total,
        "passed": results.passed,
        "failed": results.failed,
        "case_results": [
            {
                "source_file": cr.test_case.source_file,
                "start_line": cr.test_case.start_line,
                "end_line": cr.test_case.end_line,
                "function": cr.function,
                "results": [
                    {
                        "line_number": r.test.line_number,
                        "variable": r.test.variable,
                        "expected": r.test.expected_value,
                        "actual": list(r.actual) if isinstance(r.actual, set) else r.actual,
                        "status": r.status,
                        "missing": list(r.missing) if r.missing else None,
                        "extra": list(r.extra) if r.extra else None
                    } for r in cr.results
                ]
            } for cr in results.case_results
        ]
    }

    # Write results to JSON file
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, indent=2)

    return 0 if results.failed == 0 else 1


def main() -> None:
    log(sys.argv)
    parser = argparse.ArgumentParser(
        description="LLDB 18 Debug Script with DWARF 5 Support")
    parser.add_argument("executable", help="Path to the executable")
    parser.add_argument("sources", nargs='+', help="Paths to the source files")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Enable interactive mode on test failure")
    parser.add_argument("--result-path", help="Path to write the result")
    args = parser.parse_args()

    try:
        if args.result_path:
            exit_code = run_tests_with_result(args.executable, args.sources,
                                              args.verbose, args.interactive, args.result_path)
        else:
            exit_code = run_tests(args.executable, args.sources,
                                  args.verbose, args.interactive)
    except Exception as e:
        log(f"An unexpected error occurred: {str(e)}")
        exit_code = 2  # Use a different exit code for unexpected errors

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
