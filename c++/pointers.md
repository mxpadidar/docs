# Pointers

In C++, variables are stored in the computer's memory, each at a unique address. When a variable is declared, the operating system allocates memory for it, and the program can access this variable by its name rather than its physical address.

Memory is structured as a sequence of single-byte cells with unique, ordered addresses. Larger data types occupy consecutive memory cells. Although a program doesn’t control where variables are stored, it can retrieve a variable’s memory address at runtime, which allows direct access to specific memory cells. This is where pointers become useful, as they store memory addresses and provide a powerful way to manipulate data directly in memory.

## Address-of operator (&)

The address-of operator `&` returns the memory address of a variable. The actual address of a variable in memory cannot be known before runtime, so the address-of operator is used to retrieve it.

```cpp
foo = &bar;  // Assigns the memory address of 'bar' to 'foo'
```

## Dereference operator (\*)

The dereference operator `*` is used to access the value stored at a memory address. It is also used to declare pointers.

```cpp
baz = foo;   // baz equal to foo
baz = *foo;  // baz equal to value pointed to by foo (25)
```

## Pointer Declaration and Initialization

A pointer has different properties when it points to a char than when it points to an int or a float. The data type of the pointer must match the data type of the variable it points to.

Pointers can be initialized either to the address of a variable, or to the value of another pointer (or array).

```cpp
type * pointer;  // Pointer declaration
type * pointer = &variable;  // Pointer initialization to address of variable
type * pointer = otherPointer;  // Pointer initialization to value of another pointer
```

The asterisk (\*) used when declaring a pointer only means that it is a pointer. Its not related to the dereference operator.

```cpp
int firstValue, secondValue;
int * myPointer;

myPointer = &firstValue;
*myPointer = 10;
myPointer = &secondValue;
*myPointer = 20;
cout << "firstValue is " << firstValue << '\n'; // output: firstValue is 10
cout << "secondValue is " << secondValue << '\n'; // output: secondValue is 20
```

## Pointers and Arrays

Pointers and arrays are closely related in C++. An array name can be used as a pointer to the first element of the array. The main difference being that pointers can be assigned new addresses, while arrays cannot.

```cpp
int numbers[5];
int * p;
p = numbers;  *p = 10; // Equivalent to numbers[0] = 10;
p++;  *p = 20; // Equivalent to numbers[1] = 20;
p = &numbers[2];  *p = 30; // Equivalent to numbers[2] = 30;
p = numbers + 3;  *p = 40; // Equivalent to numbers[3] = 40;
p = numbers;  *(p+4) = 50; // Equivalent to numbers[4] = 50;
```

## Pointer arithmetic

To conduct arithmetical operations on pointers is a little different than to conduct them on regular integer types. To begin with, only addition and subtraction operations are allowed; the others make no sense in the world of pointers. But both addition and subtraction have a slightly different behavior with pointers, according to the size of the data type to which they point.

```cpp
char * p1; // Imagine that p1 is stored at address 1000
int * p2;  // Imagine that p2 is stored at address 2000

++p1; // p1 = 1001
++p2; // p2 = 2004
```

The increment (++) and decrement (--) operators can be used as either a prefix or suffix. As a prefix, the operation occurs before the expression is evaluated; as a suffix, it occurs after. This applies to pointers as well, where they often combine with the dereference operator (\*).

For example, `*p++` is equivalent to `*(p++)`: it dereferences p before incrementing it, so it points to the original address. The key combinations are:

```cpp
*p++   // Dereference current pointer, then increment
*++p   // Increment pointer, then dereference
++*p   // Increment value pointed to
(*p)++ // Dereference, then post-increment the pointed-to value
```

In a statement like `*p++ = *q++;`, both pointers are incremented after assignment. For clarity, parentheses can help avoid confusion.

## Pointers and `const`

Pointers can be used to modify or read the value they point to. However, by qualifying the type as `const`, we can make pointers that allow only reading, not modifying, the value they point to.

```cpp
int x;
int y = 10;
const int* p = &y; // Pointer to const int
x = *p;            // OK: reading p
*p = x;            // Error: modifying p, which is const-qualified
```

Here, `p` can read but not modify `y`. Converting a non-const pointer to a const pointer is allowed, but the reverse is not.

Pointers to const are often used in functions to indicate read-only access:

```cpp
void print_all(const int* start, const int* stop) {
  const int* current = start;
  while (current != stop) {
    cout << *current << '\n';
    ++current; // Moving pointer is allowed, modifying content is not
  }
}
```

Pointers themselves can also be `const`. This creates different combinations:

- `int * p1` - Non-const pointer to non-const int
- `const int * p2` - Non-const pointer to const int
- `int * const p3` - Const pointer to non-const int
- `const int * const p4` - Const pointer to const int

Both `const int *` and `int const *` mean the same thing: a non-const pointer to a const int.

## Pointers and String Literals

String literals are arrays of `const char` ending in a null character (`\0`). They can be accessed directly by pointers, but as constants, they cannot be modified.

```cpp
const char* foo = "hello";
```

This assigns `foo` a pointer to the first character of the `"hello"` string literal. Given `foo`, you can access elements like an array:

```cpp
*(foo+4)  // or
foo[4]    // Both yield 'o' (the fifth character)
```

Thus, `foo` points to a sequence of characters, similar to arrays. However, attempting to modify `foo` will result in a compilation error.

## Void Pointers

Void pointers (`void*`) can hold addresses of any data type, making them versatile. However, they can’t be directly dereferenced due to the lack of a specific type. To use the value they point to, a void pointer must be cast to a specific type:

```cpp
void increase(void* data, int psize) {
  if (psize == sizeof(char)) { char* pchar = (char*)data; ++(*pchar); }
  else if (psize == sizeof(int)) { int* pint = (int*)data; ++(*pint); }
}
```

In this example, `increase` can increment either a `char` or an `int` by casting `data` accordingly.

## Null Pointers and Invalid Pointers

Pointers can sometimes be uninitialized or out-of-bounds, which may lead to undefined behavior if dereferenced:

```cpp
int* p;                // uninitialized pointer
int myarray[10];
int* q = myarray + 20; // out-of-bounds pointer
```

To represent “nowhere,” use null pointers (`nullptr` or `0`):

```cpp
int* p = nullptr;      // explicitly points to no address
```

**Note**: Null pointers indicate “no address,” while void pointers can hold any address without specifying the type.
