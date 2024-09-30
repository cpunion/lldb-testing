CC = clang
CFLAGS = -g
SOURCE = example/test.c
OPTIMIZATION_LEVELS = 0 1 2
INLINE_OPTIONS = 0 1

# 生成目标文件名
define generate_target
example/test$(if $(filter 1,$(2)),_inline)_O$(1).out
endef

# 生成LLVM IR文件名
define generate_ll_target
example/test$(if $(filter 1,$(2)),_inline)_O$(1).ll
endef

# 定义所有目标
TARGETS = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(call generate_target,$(opt),$(inline))))
LL_TARGETS = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(call generate_ll_target,$(opt),$(inline))))

.PHONY: all build test clean

all: build test
build: $(TARGETS) $(LL_TARGETS)

# 编译规则
define compile_rule
$(call generate_target,$(1),$(2)): $(SOURCE)
	$(CC) $(CFLAGS) -O$(1) -DTEST_INLINE=$(2) -o $$@ $$<

$(call generate_ll_target,$(1),$(2)): $(SOURCE)
	$(CC) $(CFLAGS) -O$(1) -DTEST_INLINE=$(2) -S -emit-llvm -o $$@ $$<
endef

# 生成所有编译规则
$(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(eval $(call compile_rule,$(opt),$(inline)))))

# 测试规则
define test_rule
test_O$(1)_inline$(2): $(call generate_target,$(1),$(2))
	-./runtest.sh $(if $(VERBOSE),-v) $$< $(SOURCE)
endef

# 生成所有测试规则
$(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),$(eval $(call test_rule,$(opt),$(inline)))))

# 定义测试目标
TEST_TARGETS = $(foreach opt,$(OPTIMIZATION_LEVELS),$(foreach inline,$(INLINE_OPTIONS),test_O$(opt)_inline$(inline)))

test: $(TEST_TARGETS)
	@echo "All tests completed. Check output for any failures."

clean:
	rm -rf $(TARGETS) $(LL_TARGETS) example/*.dSYM
