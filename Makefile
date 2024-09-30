CC = clang
CFLAGS = -g -O1
TARGET = example/test.out
SOURCE = example/test.c

.PHONY: all build test clean

all: build test

build: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $@ $<

test: $(TARGET)
	./runtest.sh -v $(TARGET) $(SOURCE)

clean:
	rm -f $(TARGET)
