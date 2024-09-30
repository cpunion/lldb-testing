# LLDB 调试符号测试框架

[English](README.md) | [中文](README_zh.md)

本项目提供了一个使用 LLDB 验证编译器调试符号实现的测试框架。它允许您在程序执行期间验证变量值，这对于确保编译器生成的调试信息的正确性至关重要。

## 特性

- 自动设置断点和验证变量值
- 支持测试单个变量和作用域内的所有变量
- 详细输出选项，提供详细的测试结果
- 交互模式用于调试失败的测试
- 与 LLDB 集成，提供强大的调试功能
- 适用于测试 LLDB 支持的各种编程语言的调试符号实现

## 快速示例

```c
#include <stdio.h>

int main() {
    int x = 5;
    int y = 10;
    // Expected:
    //   x: 5
    //   y: 10
    //   all variables: x y
    printf("x = %d, y = %d\n", x, y);
    return 0;
}
```

编译并运行测试：

```bash
$ clang -g -o test_program test_program.c

$ ./runtest.sh ./test_program test_program.c -v
(lldb) command script import ./test.py
(lldb) script test.run_tests_with_result('./test_program', ['test_program.c',], True, False, '/tmp/lldb_exit_code')
Running tests for test_program.c with ./test_program
Found 1 test cases

Setting breakpoint at test_program.c:9

Test case: test_program.c:6-9 in function 'main'
✓ Line 7, x: Pass
✓ Line 8, y: Pass
✓ Line 9, all variables: Pass
    Variables: x, y

Test results:
  Total tests: 3
  Passed tests: 3
  Failed tests: 0
All tests passed!
0
(lldb) quit
```

## 要求

- LLDB（推荐版本 18 或更高，以支持 DWARF 5）
- 适用于目标语言的编译器（例如，C/C++ 使用 Clang，Go 使用 Go 编译器）

## 安装

1. 克隆此仓库：

   ```
   git clone https://github.com/cpunion/lldb-test.git
   cd lldb-test
   ```

2. 确保已安装 LLDB 并可在 PATH 中访问。

## 使用方法

1. 准备带有内联测试注释的程序。

2. 使用适当的编译器编译程序，并启用调试符号。

3. 运行测试：

   ```
   ./runtest.sh 路径/到/你的/编译后的/程序 路径/到/你的/源文件...
   ```

   要获得详细输出，请使用：

   ```
   ./runtest.sh -v 路径/到/你的/编译后的/程序 路径/到/你的/源文件...
   ```

   要在测试失败时进入交互模式，请使用：

   ```
   ./runtest.sh -i 路径/到/你的/编译后的/程序 路径/到/你的/源文件...
   ```

## 支持的语言

该框架可用于测试 LLDB 支持的任何编程语言的调试符号实现。一些示例包括但不限于：

- C/C++
- Objective-C/Objective-C++
- Swift
- Rust
- Go
- 汇编语言

确保为目标语言使用适当的编译器和编译标志，包括生成调试符号。该框架的灵活性使其能够与 LLDB 可以调试的任何语言一起工作，使其成为在各种编程环境中测试调试符号实现的多功能工具。

## 示例：测试 C 编译器调试符号实现

以下是如何编写和运行 C 编译器调试符号实现测试的详细示例：

1. 编写带有内联测试注释的 C 程序：

   ```c
   #include <stdio.h>

   int main() {
       int x = 5;
       int y = 10;
       // Expected:
       //   x: 5
       //   y: 10
       //   all variables: x y
       printf("x = %d, y = %d\n", x, y);
       return 0;
   }
   ```

2. 使用调试符号编译程序：

   ```
   clang -g -o test_program test_program.c
   ```

3. 按照使用方法部分所述运行测试：

   ```
   ./runtest.sh ./test_program test_program.c -v
   ```

### 编写用于调试符号验证的内联测试

- 使用 `// Expected:` 注释定义测试用例
- 每个后续行应采用 `//   变量名: 预期值` 的格式
- 使用 `//   all variables: var1 var2 ...` 测试作用域中特定变量的存在
- 这些内联测试通过在程序执行的特定点检查变量值和作用域来验证调试符号实现的正确性

## 故障排除

如果在运行测试时遇到 "Unable to import 'lldb'" 错误：

1. 确保正确安装了 LLDB 并在 PATH 中可访问。
2. 如果使用虚拟环境，请确保已激活该环境，并且 LLDB Python 模块在其中可访问。

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

本项目采用 MIT 许可证 - 有关详细信息，请参阅 LICENSE 文件。
