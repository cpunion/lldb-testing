#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <complex.h>
#include <string.h>

// Update the INLINE macro definition
#if defined(TEST_INLINE) && TEST_INLINE == 1
    #define INLINE __attribute__((always_inline)) static inline
#elif defined(TEST_INLINE) && TEST_INLINE == 0
    #define INLINE __attribute__((noinline))
#else
    #define INLINE static inline
#endif

// Base struct
typedef struct {
    char* name;
} base;

// E struct
typedef struct {
    // base base;  // Commented out as it's commented in the original
    int i;
} e;

// StructWithAllTypeFields struct
typedef struct struct_with_all_type_fields {
    int8_t i8;
    int16_t i16;
    int32_t i32;
    int64_t i64;
    int i;
    uint8_t u8;
    uint16_t u16;
    uint32_t u32;
    uint64_t u64;
    unsigned int u;
    float f32;
    double f64;
    bool b;
    float complex c64;
    double complex c128;
    int* slice;
    int slice_len;
    int arr[3];
    e arr2[3];
    char* s;
    e e;
    struct struct_with_all_type_fields* pf;  // recursive
    int* pi;
    // interface, map, chan, error, and function pointer are omitted as requested
    int pad1;
    int pad2;
} struct_with_all_type_fields;

typedef struct {
    int i;
} tiny_struct;

typedef struct {
    int i;
    int j;
} small_struct;

typedef struct {
    int i;
    int j;
    int k;
} mid_struct;

typedef struct {
    int i;
    int j;
    int k;
    int l;
    int m;
    int n;
    int o;
    int p;
    int q;
    int r;
} big_struct;

INLINE void struct_params(tiny_struct t, small_struct s, mid_struct m, big_struct b) {
    // Expected:
    //   all variables: t s m b global_int global_struct global_struct_ptr
    //   t.i: 1
    //   s.i: 2
    //   s.j: 3
    //   m.i: 4
    //   m.j: 5
    //   m.k: 6
    //   b.i: 7
    //   b.j: 8
    //   b.k: 9
    //   b.l: 10
    //   b.m: 11
    //   b.n: 12
    //   b.o: 13
    //   b.p: 14
    //   b.q: 15
    //   b.r: 16
    printf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n", 
           t.i, s.i, s.j, m.i, m.j, m.k, b.i, b.j, b.k, b.l, b.m, b.n, b.o, b.p, b.q, b.r);
    t.i = 10;
    s.i = 20;
    s.j = 21;
    m.i = 40;
    m.j = 41;
    m.k = 42;
    b.i = 70;
    b.j = 71;
    b.k = 72;
    b.l = 73;
    b.m = 74;
    b.n = 75;
    b.o = 76;
    b.p = 77;
    b.q = 78;
    b.r = 79;
    // Expected:
    //   all variables: t s m b global_int global_struct global_struct_ptr
    //   t.i: 10
    //   s.i: 20
    //   s.j: 21
    //   m.i: 40
    //   m.j: 41
    //   m.k: 42
    //   b.i: 70
    //   b.j: 71
    //   b.k: 72
    //   b.l: 73
    //   b.m: 74
    //   b.n: 75
    //   b.o: 76
    //   b.p: 77
    //   b.q: 78
    //   b.r: 79
    printf("done\n");
}

INLINE void struct_ptr_params(tiny_struct* t, small_struct* s, mid_struct* m, big_struct* b) {
    // Expected:
    //   all variables: t s m b global_int global_struct global_struct_ptr
    //   t->i: 1
    //   s->i: 2
    //   s->j: 3
    //   m->i: 4
    //   m->j: 5
    //   m->k: 6
    //   b->i: 7
    //   b->j: 8
    //   b->k: 9
    //   b->l: 10
    //   b->m: 11
    //   b->n: 12
    //   b->o: 13
    //   b->p: 14
    //   b->q: 15
    //   b->r: 16
    printf("%p %p %p %p\n", (void*)t, (void*)s, (void*)m, (void*)b);
    t->i = 10;
    s->i = 20;
    s->j = 21;
    m->i = 40;
    m->j = 41;
    m->k = 42;
    b->i = 70;
    b->j = 71;
    b->k = 72;
    b->l = 73;
    b->m = 74;
    b->n = 75;
    b->o = 76;
    b->p = 77;
    b->q = 78;
    b->r = 79;
    // Expected:
    //   all variables: t s m b global_int global_struct global_struct_ptr
    //   t->i: 10
    //   s->i: 20
    //   s->j: 21
    //   m->i: 40
    //   m->j: 41
    //   m->k: 42
    //   b->i: 70
    //   b->j: 71
    //   b->k: 72
    //   b->l: 73
    //   b->m: 74
    //   b->n: 75
    //   b->o: 76
    //   b->p: 77
    //   b->q: 78
    //   b->r: 79
    printf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n", 
           t->i, s->i, s->j, m->i, m->j, m->k, b->i, b->j, b->k, b->l, b->m, b->n, b->o, b->p, b->q, b->r);
    printf("done\n");
}

INLINE void scope_if(int branch) {
    int a = 1;
    // Expected:
    //   all variables: a branch global_int global_struct global_struct_ptr
    //   a: 1
    printf("ScopeIf %d\n", a);
    if (branch == 1) {
        int b = 2;
        int c = 3;
        // Expected:
        //   all variables: a b c branch global_int global_struct global_struct_ptr
        //   a: 1
        //   b: 2
        //   c: 3
        //   branch: 1
        printf("%d %d %d\n", a, b, c);
    } else {
        int c = 3;
        int d = 4;
        // Expected:
        //   all variables: a c d branch global_int global_struct global_struct_ptr
        //   a: 1
        //   c: 3
        //   d: 4
        //   branch: 0
        printf("%d %d\n", c, d);
    }
    // Expected:
    //   all variables: a branch global_int global_struct global_struct_ptr
    //   a: 1
    printf("a: %d\n", a);
}

INLINE void scope_for() {
    int a = 1;
    for (int i = 0; i < 10; i++) {
        switch (i) {
            case 0:
                printf("i is 0\n");
                // Expected:
                //   all variables: i a global_int global_struct global_struct_ptr
                //   i: 0
                //   a: 1
                printf("i: %d\n", i);
                break;
            case 1:
                printf("i is 1\n");
                // Expected:
                //   all variables: i a global_int global_struct global_struct_ptr
                //   i: 1
                //   a: 1
                printf("i: %d\n", i);
                break;
            default:
                printf("i is %d\n", i);
        }
    }
    printf("a: %d\n", a);
}

INLINE void scope_switch(int i) {
    int a = 0;
    switch (i) {
        case 1: {
            int b = 1;
            printf("i is 1\n");
            // Expected:
            //   all variables: i a b global_int global_struct global_struct_ptr
            //   i: 1
            //   a: 0
            //   b: 1
            printf("i: %d a: %d b: %d\n", i, a, b);
            break;
        }
        case 2: {
            int c = 2;
            printf("i is 2\n");
            // Expected:
            //   all variables: i a c global_int global_struct global_struct_ptr
            //   i: 2
            //   a: 0
            //   c: 2
            printf("i: %d a: %d c: %d\n", i, a, c);
            break;
        }
        default: {
            int d = 3;
            printf("i is %d\n", i);
            // Expected:
            //   all variables: i a d global_int global_struct global_struct_ptr
            //   i: 3
            //   a: 0
            //   d: 3
            printf("i: %d a: %d d: %d\n", i, a, d);
        }
    }
    // Expected:
    //   all variables: a i global_int global_struct global_struct_ptr
    //   a: 0
    printf("a: %d\n", a);
}


// Function definitions
INLINE void all_type_struct_param(struct_with_all_type_fields s) {
    printf("%p\n", (void*)&s);
    // Expected:
    //   all variables: s global_int global_struct global_struct_ptr
    //   s.i8: '\x01'
    //   s.i16: 2
    //   s.i32: 3
    //   s.i64: 4
    //   s.i: 5
    //   s.u8: '\x06'
    //   s.u16: 7
    //   s.u32: 8
    //   s.u64: 9
    //   s.u: 10
    //   s.f32: 11
    //   s.f64: 12
    //   s.b: true
    //   s.c64: 13 + 14i
    //   s.c128: 15 + 16i
    //   s.slice[0]: 21
    //   s.slice[1]: 22
    //   s.slice[2]: 23
    //   s.arr[0]: 24
    //   s.arr[1]: 25
    //   s.arr[2]: 26
    //   s.arr2[0].i: 27
    //   s.arr2[1].i: 28
    //   s.arr2[2].i: 29
    //   s.s[0]: 'h'
    //   s.s[1]: 'e'
    //   s.s[2]: 'l'
    //   s.s[3]: 'l'
    //   s.s[4]: 'o'
    //   s.e.i: 30
    //   s.pad1: 100
    //   s.pad2: 200
    s.i8 = '\b';
    // Expected:
    //   s.i8: '\b'
    //   s.i16: 2
    printf("%d %d\n", (int)strlen(s.s), s.i8);
}

// Add this function definition near the bottom of the file
INLINE int all_type_params(
    int8_t i8, int16_t i16, int32_t i32, int64_t i64, int i,
    uint8_t u8, uint16_t u16, uint32_t u32, uint64_t u64, unsigned int u,
    float f32, double f64, bool b,
    float complex c64, double complex c128,
    int* slice, int arr[3], e arr2[3],
    char* s, e e,
    struct_with_all_type_fields f, struct_with_all_type_fields* pf, int* pi
    // interface, map, chan, error, and function pointer are omitted as requested
) {
    // Expected:
    //   all variables: i8 i16 i32 i64 i u8 u16 u32 u64 u f32 f64 b c64 c128 slice arr arr2 e f global_int global_struct global_struct_ptr pf pi s
    //   i32: 3
    //   i64: 4
    //   i: 5
    //   u32: 8
    //   u64: 9
    //   u: 10
    //   f32: 11
    //   f64: 12
    //   slice[0]: 21
    //   slice[1]: 22
    //   slice[2]: 23
    //   arr[0]: 24
    //   arr[1]: 25
    //   arr[2]: 26
    //   arr2[0].i: 27
    //   arr2[1].i: 28
    //   arr2[2].i: 29
    //   e.i: 30
    //   i8: '\x12'
    //   i16: 2
    //   u8: '\x06'
    //   u16: 7
    //   b: true
    printf("%d %d %d %lld %d %u %u %u %llu %u %f %f %d %f %f %p %d %d %d %s %d %p %p %p\n",
           i8, i16, i32, i64, i, u8, u16, u32, u64, u, f32, f64, b,
           crealf(c64), crealf(c128),
           (void*)slice, arr[0], arr2[0].i, e.i,
           s, f.i, (void*)pf, (void*)pi, (void*)&f);  // Added (void*)&f as the last argument

    i8 = 9;
    i16 = 10;
    i32 = 11;
    i64 = 12;
    i = 13;
    u8 = 14;
    u16 = 15;
    u32 = 16;
    u64 = 17;
    u = 18;
    f32 = 19;
    f64 = 20;
    b = false;
    c64 = 21 + 22 * I;
    c128 = 23 + 24 * I;
    slice[0] = 31; slice[1] = 32; slice[2] = 33;
    arr[0] = 34; arr[1] = 35; arr[2] = 36;
    arr2[0].i = 37; arr2[1].i = 38; arr2[2].i = 39;
    s = "world";
    e.i = 40;

    printf("%d %d %d %lld %d %u %u %u %llu %u %f %f %d %f %f %d %d %d %d %d %d %s %d %p %p %p\n",
           i8, i16, i32, i64, i, u8, u16, u32, u64, u, f32, f64, b,
           crealf(c64), crealf(c128),
           slice[0], slice[1], slice[2], arr[0], arr[1], arr[2],
           s, e.i, (void*)&f, (void*)pf, (void*)pi);

    // Expected:
    //   i8: '\t'
    //   i16: 10
    //   i32: 11
    //   i64: 12
    //   i: 13
    //   u8: '\x0e'
    //   u16: 15
    //   u32: 16
    //   u64: 17
    //   u: 18
    //   f32: 19
    //   f64: 20
    //   b: false
    //   c64: 21 + 22i
    //   c128: 23 + 24i
    //   slice[0]: 31
    //   slice[1]: 32
    //   slice[2]: 33
    //   arr[0]: 34
    //   arr[1]: 35
    //   arr[2]: 36
    //   arr2[0].i: 37
    //   arr2[1].i: 38
    //   arr2[2].i: 39
    //   s[0]: 'w'
    //   s[1]: 'o'
    //   s[2]: 'r'
    //   s[3]: 'l'
    //   s[4]: 'd'
    //   e.i: 40

    // Expected(skip):
    //   arr: [34, 35, 36]
    printf("FuncWithAllTypeParams %p\n", (void*)&f);
    return 1;
}

int global_int = 301;
struct_with_all_type_fields global_struct;
struct_with_all_type_fields* global_struct_ptr;

INLINE void Test() {
    struct_params((tiny_struct){1}, (small_struct){2, 3}, (mid_struct){4, 5, 6}, 
                  (big_struct){7, 8, 9, 10, 11, 12, 13, 14, 15, 16});
    
    tiny_struct t = {1};
    small_struct s = {2, 3};
    mid_struct m = {4, 5, 6};
    big_struct b = {7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    struct_ptr_params(&t, &s, &m, &b);

    int i = 100;
    struct_with_all_type_fields s_all = {
        .i8 = 1,
        .i16 = 2,
        .i32 = 3,
        .i64 = 4,
        .i = 5,
        .u8 = 6,
        .u16 = 7,
        .u32 = 8,
        .u64 = 9,
        .u = 10,
        .f32 = 11,
        .f64 = 12,
        .b = true,
        .c64 = 13 + 14 * I,
        .c128 = 15 + 16 * I,
        .slice = (int[]){21, 22, 23},
        .slice_len = 3,
        .arr = {24, 25, 26},
        .arr2 = {{27}, {28}, {29}},
        .s = "hello",
        .e = {30},
        .pf = NULL,
        .pi = &i,
        .pad1 = 100,
        .pad2 = 200
    };

    // Expected:
    //   all variables: s_all i global_int global_struct global_struct_ptr t s m b
    //   s_all.i8: '\x01'
    //   s_all.i16: 2
    //   s_all.i32: 3
    //   s_all.i64: 4
    //   s_all.i: 5
    //   s_all.u8: '\x06'
    //   s_all.u16: 7
    //   s_all.u32: 8
    //   s_all.u64: 9
    //   s_all.u: 10
    //   s_all.f32: 11
    //   s_all.f64: 12
    //   s_all.b: true
    //   s_all.c64: 13 + 14i
    //   s_all.c128: 15 + 16i
    //   s_all.slice[0]: 21
    //   s_all.slice[1]: 22
    //   s_all.slice[2]: 23
    //   s_all.arr[0]: 24
    //   s_all.arr[1]: 25
    //   s_all.arr[2]: 26
    //   s_all.arr2[0].i: 27
    //   s_all.arr2[1].i: 28
    //   s_all.arr2[2].i: 29
    //   s_all.s[0]: 'h'
    //   s_all.s[1]: 'e'
    //   s_all.s[2]: 'l'
    //   s_all.s[3]: 'l'
    //   s_all.s[4]: 'o'
    //   s_all.e.i: 30
    //   *s_all.pi: 100
    global_struct_ptr = &s_all;
    global_struct = s_all;
    printf("globalInt: %d\n", global_int);

    printf("s_all: %p\n", (void*)&s_all);
    all_type_struct_param(s_all);
    printf("called function with struct\n");

    scope_if(1);
    scope_if(0);
    scope_for();
    scope_switch(1);
    scope_switch(2);
    scope_switch(3);
    printf("%p\n", (void*)global_struct_ptr);
    printf("%p\n", (void*)&global_struct);
    s_all.i8 = 0x12;
    printf("%d\n", s_all.i8);
    // Expected:
    //   all variables: s_all i global_int global_struct global_struct_ptr t s m b
    //   s_all.i8: '\x12'

    // Expected(skip):
    //   global_struct.i8: '\x01'

    all_type_params(s_all.i8, s_all.i16, s_all.i32, s_all.i64,
                    s_all.i, s_all.u8, s_all.u16, s_all.u32,
                    s_all.u64, s_all.u,
                    s_all.f32, s_all.f64, s_all.b,
                    s_all.c64, s_all.c128,
                    s_all.slice, s_all.arr, s_all.arr2,
                    s_all.s, s_all.e,
                    s_all, global_struct_ptr, &i);
    printf("%d\n", (*global_struct_ptr).i8);
    printf("done\n");
    printf("\n");
    printf("%p %p %d %p\n", (void*)&s_all, (void*)&global_struct, global_struct_ptr->i16, (void*)global_struct_ptr);
    global_struct_ptr = NULL;
}

int main() {
    Test();
    return 0;
}