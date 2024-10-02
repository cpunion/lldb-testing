# clang test summary

## Two-step test

The two-step test used in this test consists of the following commands:

```shell
clang -g -O2 -DTEST_INLINE=$(INLINE) -S -emit-llvm \
    -o build/temp_$(INLINE).ll test.c
clang -g -O0 -o build/test$(if $(filter 1,$(INLINE)),_inline)_two-step.out \
    build/temp_$(INLINE).ll
```

`INLINE` is `1` or `0`.

## Test results

Version 0 failed: 72 / 1800:

```
Homebrew clang version 19.1.0
Target: arm64-apple-darwin23.4.0
Thread model: posix
InstalledDir: /opt/homebrew/Cellar/llvm/19.1.0/bin
```

Version 1 failed: 296 / 1800:

```
Homebrew clang version 18.1.8
Target: arm64-apple-darwin23.4.0
Thread model: posix
InstalledDir: /opt/homebrew/Cellar/llvm@18/18.1.8/bin
```

| Function | Loc | inline -O0 | -O0 | inline -O1 | -O1 | inline -O2 | -O2 | inline two-step | two-step |
|----------|-----|----- | ----- | ----- | ----- | ----- | ----- | ----- | -----|
| struct_params | test.c:87 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:88 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅✅ | ✅✅ | ✅✅ | ❌✅ |
| struct_params | test.c:89 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅✅ | ✅✅ | ✅✅ | ❌✅ |
| struct_params | test.c:90 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ |
| struct_params | test.c:91 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ |
| struct_params | test.c:92 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ |
| struct_params | test.c:93 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ | ❌✅ |
| struct_params | test.c:94 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:95 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:96 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:97 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:98 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:99 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:100 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:101 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:102 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:103 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:123 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:124 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:125 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:126 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:127 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:128 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:129 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_params | test.c:130 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:131 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:132 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:133 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:134 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:135 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:136 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:137 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:138 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_params | test.c:139 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| struct_ptr_params | test.c:145 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:146 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:147 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:148 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:149 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:150 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:151 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:152 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:153 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:154 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:155 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:156 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:157 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:158 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:159 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:160 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:161 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:180 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| struct_ptr_params | test.c:181 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:182 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:183 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:184 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:185 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:186 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:187 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:188 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:189 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:190 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:191 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:192 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:193 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:194 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:195 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| struct_ptr_params | test.c:196 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅✅ | ✅✅ | ✅✅ | ✅❌ |
| scope_if | test.c:205 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:206 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:212 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:213 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:214 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:215 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:216 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:222 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:223 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:224 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:225 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:226 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:230 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_if | test.c:231 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_for | test.c:242 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ✅✅ |
| scope_for | test.c:243 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ✅✅ |
| scope_for | test.c:244 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_for | test.c:250 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ✅✅ |
| scope_for | test.c:251 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ✅✅ |
| scope_for | test.c:252 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:269 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:270 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:271 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:272 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:280 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:281 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:282 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:283 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:291 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:292 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:293 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:294 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:299 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| scope_switch | test.c:300 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:309 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:310 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:311 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:312 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:313 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:314 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:315 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:316 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:317 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:318 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:319 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:320 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:321 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:322 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:323 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:324 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:325 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:326 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:327 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:328 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:329 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:330 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:331 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:332 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:333 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:334 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:335 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:336 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:337 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:338 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:339 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:340 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:341 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:344 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_struct_param | test.c:345 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:361 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:362 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:363 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:364 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:365 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:366 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:367 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:368 | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:369 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:370 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:371 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:372 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅✅ |
| all_type_params | test.c:373 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:374 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:375 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:376 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:377 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:378 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:379 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅❌ | ✅❌ | ✅❌ | ❌✅ |
| all_type_params | test.c:380 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅❌ | ✅❌ | ✅❌ | ❌✅ |
| all_type_params | test.c:381 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅❌ | ✅❌ | ✅❌ | ❌✅ |
| all_type_params | test.c:382 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅❌ | ✅❌ | ✅❌ | ❌✅ |
| all_type_params | test.c:383 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅❌ | ✅❌ | ✅❌ | ❌✅ |
| all_type_params | test.c:384 | ✅✅ | ✅✅ | ✅✅ | ❌✅ | ✅❌ | ✅❌ | ✅❌ | ❌✅ |
| all_type_params | test.c:419 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:420 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:421 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:422 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:423 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:424 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:425 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:426 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:427 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:428 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:429 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:430 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:431 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:432 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:433 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:434 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:435 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:436 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| all_type_params | test.c:437 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:438 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:439 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:440 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:441 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:442 | ✅✅ | ✅✅ | ✅✅ | ✅❌ | ✅❌ | ✅❌ | ✅❌ | ✅❌ |
| all_type_params | test.c:443 | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:444 | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:445 | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:446 | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:447 | ✅✅ | ✅✅ | ✅✅ | ❌❌ | ❌❌ | ❌❌ | ❌❌ | ❌❌ |
| all_type_params | test.c:448 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:500 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:501 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:502 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:503 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:504 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:505 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:506 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:507 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:508 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:509 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:510 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:511 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:512 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:513 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:514 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:515 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:516 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:517 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:518 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:519 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:520 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:521 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:522 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:523 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:524 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:525 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:526 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:527 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:528 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:529 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:530 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:531 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:551 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
| Test | test.c:552 | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅✅ |
