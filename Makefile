CC = clang
CFLAGS = -g -O1
LLTARGET = example/test.ll
INLINE_LLTARGET = example/test_inline.ll
TARGET = example/test.out
INLINE_TARGET = example/test_inline.out
SOURCE = example/test.c

.PHONY: all build test clean inline

all: build test test_inline


build: $(TARGET) $(INLINE_TARGET) $(LLTARGET) $(INLINE_LLTARGET)

$(LLTARGET): $(SOURCE)
	$(CC) $(CFLAGS) -DTEST_INLINE=0 -S -emit-llvm -o $@ $<

$(INLINE_LLTARGET): $(SOURCE)
	$(CC) $(CFLAGS) -DTEST_INLINE=1 -S -emit-llvm -o $@ $<

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -DTEST_INLINE=0 -o $@ $<

$(INLINE_TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -DTEST_INLINE=1 -o $@ $<

test: $(TARGET)
	./runtest.sh $(if $(VERBOSE),-v) $(TARGET) $(SOURCE)

test_inline: $(INLINE_TARGET)
	./runtest.sh $(if $(VERBOSE),-v) $(INLINE_TARGET) $(SOURCE)

clean:
	rm -f $(TARGET) $(INLINE_TARGET) $(LLTARGET)
