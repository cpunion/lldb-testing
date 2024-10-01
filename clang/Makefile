CC = clang
CFLAGS = -g
SOURCE = test.c
OPTIMIZATION_LEVELS = 0 1 2
INLINE_OPTIONS = 0 1

# Generate target file name
define generate_target
test$(if $(filter 1,$(2)),_inline)_O$(1).out
endef

# Generate LLVM IR file name
define generate_ll_target
test$(if $(filter 1,$(2)),_inline)_O$(1).ll
endef

# Define all targets
TARGETS = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(call generate_target,$(opt),$(inline))))
LL_TARGETS = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(call generate_ll_target,$(opt),$(inline))))

.PHONY: all build test clean

all: build test
build: $(TARGETS) $(LL_TARGETS)

# Compilation rules
define compile_rule
$(call generate_target,$(1),$(2)): $(SOURCE)
	$(CC) $(CFLAGS) -O$(1) -DTEST_INLINE=$(2) -o $$@ $$<

$(call generate_ll_target,$(1),$(2)): $(SOURCE)
	$(CC) $(CFLAGS) -O$(1) -DTEST_INLINE=$(2) -S -emit-llvm -o $$@ $$<
endef

# Generate all compilation rules
$(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(eval $(call compile_rule,$(opt),$(inline)))))

# Define result file names
define generate_result_file
results/test$(if $(filter 1,$(2)),_inline)_O$(1).json
endef

RESULT_FILES = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(call generate_result_file,$(opt),$(inline))))

# Test rules
define test_rule
test_O$(1)_inline$(2): $(call generate_target,$(1),$(2))
	@mkdir -p results
	-python ../runtest.py $(if $(VERBOSE),-v) -r $(call generate_result_file,$(1),$(2)) $$< $(SOURCE)
endef

# Generate all test rules
$(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(eval $(call test_rule,$(opt),$(inline)))))

# Define test targets
TEST_TARGETS = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),test_O$(opt)_inline$(inline)))

test: $(TEST_TARGETS)
	@echo "All tests completed. Generating summary..."
	@echo "# clang test summary" > README.md
	@echo "" >> README.md
	@echo "## clang --version" >> README.md
	@echo "" >> README.md
	@clang --version >> README.md
	@echo "" >> README.md
	@echo "## Test results" >> README.md
	@echo "" >> README.md
	@python generate_summary.py $(RESULT_FILES) >> README.md
	@echo "Summary generated in README.md"

clean:
	rm -rf $(TARGETS) $(LL_TARGETS) *.dSYM
