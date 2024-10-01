#!/bin/bash

CC="clang"
CFLAGS="-g"
SOURCE="test.c"
BUILD_DIR="build"
RESULTS_DIR="results"

OPTIMIZATION_LEVELS="0 1 2 two-step"
INLINE_OPTIONS="0 1"

# Function to generate target names
gen_names() {
    local suffix=$1
    for opt in $OPTIMIZATION_LEVELS; do
        for inline in $INLINE_OPTIONS; do
            if [ "$inline" = "1" ]; then
                inline_str="_inline"
            else
                inline_str=""
            fi
            if [ "$opt" = "two-step" ]; then
                echo "${BUILD_DIR}/test${inline_str}_two-step${suffix}"
            else
                echo "${BUILD_DIR}/test${inline_str}_O${opt}${suffix}"
            fi
        done
    done
}

# Generate target lists
TARGETS=$(gen_names ".out")
LL_TARGETS=$(gen_names ".ll")
RESULT_FILES=$(echo "$TARGETS" | sed "s|${BUILD_DIR}/|${RESULTS_DIR}/|g" | sed 's/\.out/.json/g')

# Function to execute a command and print it
execute() {
    echo "Executing: $@"
    "$@"
}

build() {
    mkdir -p "$BUILD_DIR"
    
    for target in $TARGETS $LL_TARGETS; do
        if [[ $target == *"two-step"* ]]; then
            if [[ $target == *.out ]]; then
                ll_file="${target%.out}.ll"
                execute $CC $CFLAGS -O2 -DTEST_INLINE=$(echo "$target" | grep -q "inline" && echo "1" || echo "0") -S -emit-llvm -o "$ll_file" "$SOURCE"
                execute $CC $CFLAGS -O0 -o "$target" "$ll_file"
            else
                execute $CC $CFLAGS -O2 -DTEST_INLINE=$(echo "$target" | grep -q "inline" && echo "1" || echo "0") -S -emit-llvm -o "$target" "$SOURCE"
            fi
        else
            opt_level=$(echo "$target" | sed -n 's/.*O\([0-2]\).*/\1/p')
            if [[ $target == *.out ]]; then
                execute $CC $CFLAGS -O"$opt_level" -DTEST_INLINE=$(echo "$target" | grep -q "inline" && echo "1" || echo "0") -o "$target" "$SOURCE"
            else
                execute $CC $CFLAGS -O"$opt_level" -DTEST_INLINE=$(echo "$target" | grep -q "inline" && echo "1" || echo "0") -S -emit-llvm -o "$target" "$SOURCE"
            fi
        fi
    done
}

test() {
    mkdir -p "$RESULTS_DIR"
    
    for result_file in $RESULT_FILES; do
        out_file=$(echo "$result_file" | sed "s|${RESULTS_DIR}/|${BUILD_DIR}/|g" | sed 's/\.json/.out/g')
        execute python ../runtest.py ${VERBOSE:+-v} -r "$result_file" "$out_file" "$SOURCE" || true
    done
}

report() {
    echo "Generating summary..."
    {
        echo "# clang test summary"
        echo
        echo "## clang --version"
        echo
        execute clang --version
        echo
        echo "## Two-step test"
        echo
        echo "The two-step test used in this test consists of the following commands:"
        echo
        echo '```shell'
        echo "$CC $CFLAGS -O2 -DTEST_INLINE=\$(INLINE) -S -emit-llvm \\"
        echo "    -o ${BUILD_DIR}/temp_\$(INLINE).ll $SOURCE"
        echo "$CC $CFLAGS -O0 -o ${BUILD_DIR}/test\$(if \$(filter 1,\$(INLINE)),_inline)_two-step.out \\"
        echo "    ${BUILD_DIR}/temp_\$(INLINE).ll"
        echo '```'
        echo
        echo `INLINE` is `1` or `0`.
        echo
        echo "## Test results"
        echo
    } > README.md
    
    execute python generate_summary.py $RESULT_FILES \
        --columns "inline -O0,-O0,inline -O1,-O1,inline -O2,-O2,inline two-step,two-step" \
        >> README.md
    
    echo "Summary generated in README.md"
}

clean() {
    execute rm -rf "$BUILD_DIR" "$RESULTS_DIR"
}

# Main execution logic
main() {
    local command=${1:-all}  # Default to 'all' if no argument is provided
    case "$command" in
        build)
            build
            ;;
        test)
            test
            ;;
        report)
            report
            ;;
        clean)
            clean
            ;;
        all)
            build
            test
            report
            ;;
        *)
            echo "Usage: $0 {build|test|report|clean|all}"
            exit 1
            ;;
    esac
}

# Call the main function with all script arguments
main "$@"