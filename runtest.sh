#!/bin/bash

set -e


# Parse command-line arguments
verbose=False
interactive=False
plugin_path=""
target_path=""
file_list=()

# Use LLDB_PATH from environment variable if set, otherwise default to "lldb"
LLDB_PATH=${LLDB_PATH:-"lldb"}
PYTHON_SCRIPT="$(dirname "$0")/test.py"

print_help() {
    echo "Usage: $0 <target_path> <file1> [<file2> ...]"
    echo "target_path: The path to the target directory"
    echo "file1, file2, ...: List of files to process"
}

# Check if target_path is provided
if [ -z "$1" ]; then
    print_help
    exit 1
fi

target_path=""

# Check if at least one file is provided
if [ $# -eq 0 ]; then
    print_help
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            verbose=True
            shift
            ;;
        -i|--interactive)
            interactive=True
            shift
            ;;
        -p|--plugin)
            plugin_path="\"$2\""
            shift 2
            ;;
        *)
            if [ -z "$target_path" ]; then
                target_path="$1"
            else
                file_list+=("$1")
            fi
            shift
            ;;
    esac
done

# Set up the result file path
result_file="/tmp/lldb_exit_code"

# Prepare LLDB commands
lldb_commands=(
    "command script import $PYTHON_SCRIPT"
    "script test.run_tests_with_result('${target_path}', [$(printf "'%s'," "${file_list[@]}")], $verbose, $interactive, '$result_file')"
    "quit"
)

# Run LLDB with prepared commands 
lldb_command_string=""
for cmd in "${lldb_commands[@]}"; do
    lldb_command_string+=" -o \"$cmd\""
done

# Run LLDB with the test script
eval "$LLDB_PATH $lldb_command_string"

# Read the exit code from the result file
if [ -f "$result_file" ]; then
    exit_code=$(cat "$result_file")
    rm "$result_file"
    exit "$exit_code"
else
    echo "Error: Could not find exit code file"
    exit 1
fi
