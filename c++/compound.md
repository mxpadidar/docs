# Compound Data Types

Compound data types in C++ include arrays and character sequences, which provide a way to store collections of values under a single name.

## Array

An array is a collection of elements of the same type stored in contiguous memory locations. The general syntax to declare an array is:

```cpp
type name [elements];
```

### Initializing Arrays

- **Uninitialized arrays**: By default, local arrays (declared within functions) are uninitialized, leaving their elements with undetermined values.
- **Initialized arrays**: Static arrays and those declared in global scope are automatically initialized. If not explicitly initialized, fundamental types default to zero.

```cpp
int foo[5] = {};                 // Array of five ints, each initialized to zero
int foo[5] = {16, 2, 77, 40, 12}; // Initializes with specific values
int foo[5] = {16, 2};            // Remaining elements are set to zero
int foo[] = {16, 2, 77, 40, 12};  // Size inferred from initializer
int foo[] {10, 20, 30};          // Equal sign is optional with uniform initialization
foo[2] = 75;                     // Accessing or modifying an element
```

### Multidimensional Arrays

Multidimensional arrays are essentially arrays of arrays, useful for representing data in matrices or tables.

```cpp
int matrix[4][5];  // 4x5 matrix (array of 4 arrays with 5 integers each)
```

### Arrays as Function Parameters

In C++, arrays are passed by reference, meaning a pointer to the array's first element is passed to the function. This avoids copying the array, which is more efficient.

```cpp
void procedure(int arg[]) {
    // Function accepting an array as a parameter
}
```

---

## Character Sequences

Character sequences, or C-strings, are arrays of characters ending with a null character (`'\0'`). They offer a low-level way to handle strings, unlike the `string` class in C++.

```cpp
char foo[20];  // Can store up to 20 characters
```

### Null-Terminated Character Arrays

Character sequences are often null-terminated, which means they end with `'\0'`. This is essential for the array to be recognized as a valid string.

```cpp
char word[] = {'H', 'e', 'l', 'l', 'o', '\0'};  // Null-terminated character array
char word[] = "Hello";  // Equivalent to the above, automatically null-terminated
```

### Converting between `string` and C-Strings

The `string` class can be converted to and from null-terminated character arrays using the `c_str()` and `data()` methods.

```cpp
char myNtcs[] = "some text";
std::string myString = myNtcs;   // Convert C-string to string
std::cout << myString;           // Printed as a C++ string
std::cout << myString.c_str();   // Printed as a C-string
```

### Dynamic Memory Allocation

Dynamic memory allocation can be used to create arrays whose size is determined at runtime.

Dynamic memory is allocated using operator new. new is followed by a data type specifier and, if a sequence of more than one element is required, the number of these within brackets []. It returns a pointer to the beginning of the new block of memory allocated. Its syntax is:

```cpp
pointer = new type; // allocate memory to contain one single element of type `type`
pointer = new type [number_of_elements]; // allocate a block (an array) of elements of type `type`

// Example

int * foo;
foo = new int [5];
```

```cpp
int* foo = new int[5];  // Allocates an array of five integers
delete[] foo;           // Deallocates the array
```
