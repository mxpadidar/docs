# Variables

**Variables** are symbolic names assigned to memory locations to store data that can be modified during program execution. Variables have a **type** that determines the size, layout, range of values, and operations applicable to the stored data.

## Data Types

C++ supports various data types:

### Primitive Types

- **Integer Types:**

  - `char`: At least 8 bits (signed or unsigned)
  - `short int`: At least 16 bits (signed or unsigned)
  - `int`: At least 16 bits (signed or unsigned)
  - `long int`: At least 32 bits (signed or unsigned)
  - `long long int`: At least 64 bits (signed or unsigned)

- **Floating-Point Types:**

  - `float`: Single-precision floating-point number
  - `double`: Double-precision floating-point number
  - `long double`: Extended precision floating-point number

- **Boolean Type:**

  - `bool`: Represents true or false

- **Character Type:**
  - `char`: Represents a single character

### Derived Types

- **Arrays:** Collections of elements of the same type.
- **Pointers:** Variables that store memory addresses.
- **References:** Aliases to existing variables.

### User-Defined Types

- **Structs:** User-defined data structures.
- **Classes:** Encapsulated data and functions.
- **Enums:** User-defined integer constants.

## Identifiers and Scope

- **Identifiers:** Names given to variables, functions, and other entities.
- **Scope:** The region of a program where a variable is accessible.

### Variable Scope

- **Global variable:** Retained throughout the program's execution.
- **Local variable:** Exists only within the function's scope and is reinitialized each time the function is called.
- **Static local variable:** Retains its value between function calls, acting like a global variable within the function's scope.

```cpp
#include <iostream>

int main() {
    // Global variable
    int globalVar = 0;

    // Function to demonstrate variable scope
    void display() {
        // Local variable
        int localVar = 10;

        // Static local variable
        static int staticVar = 0;

        std::cout << "Global: " << globalVar << ", Local: " << localVar << ", Static: " << staticVar << std::endl;

        globalVar++;
        localVar++;
        staticVar++;
    }

    // Call the function multiple times
    display(); // Output: Global: 0, Local: 10, Static: 0
    display(); // Output: Global: 1, Local: 10, Static: 1
    display(); // Output: Global: 2, Local: 10, Static: 2

    return 0;
}
```

## Namespaces

**Namespace:** A declarative region that provides a scope for identifiers to prevent naming conflicts.

```cpp
// Define a namespace
namespace MyNamespace {
    int number = 10;
    int add(int a, int b) {
        return a + b;
    }
}

int main() {
    int number = 5; // Local variable
    std::cout << MyNamespace::number << std::endl; // output: 10
    std::cout << number << std::endl; // output: 5
    return 0;
}
```

**using** simplifies access to elements within a namespace:

```cpp
using MyNamespace::add;

int main() {
    std::cout << add(3, 4) << std::endl; // output: 7
    return 0;
}
```

## Constants

- **Literal Constants:** Fixed values like numbers, characters, or strings.
- **Defined Constants:** Declared using the `#define` preprocessor directive.
- **`const` Variables:** Declared using the `const` keyword to prevent modification.
- **`constexpr` Variables:** Declared using the `constexpr` keyword for compile-time constants.

```cpp
// Preprocessor constant using #define directive
#define MAX_LIMIT 100 // replaced by 100 before compilation

// Typed constant using const keyword
const double PI = 3.14159;
const int SECONDS_IN_MINUTE = 60;


// Literal constants
int year = 2024; // 2024 is an integer literal
unsigned long population = 7800000000UL; // 7800000000UL is an unsigned long integer literal
float gravity = 9.8f; // 9.8f is a float literal
double avogadro = 6.022e23; // 6.022e23 is a double literal
char initial = 'A'; // 'A' is a character literal
string greeting = "Hello"; // "Hello" is a string literal
bool isReady = true; // true is a boolean literal
int* ptr = nullptr; // nullptr is a null pointer literal
```

## Strings

Fundamental types are the simplest types that a computer can handle directly, like numbers and characters. These basic types serve as the foundation of all other types in the language.

However, one of C++'s strengths is its ability to create **compound types** by combining these fundamental types. A common example of a compound type is the **string** class, which allows you to store and work with sequences of characters, such as words or sentences—making it incredibly useful for handling text.

Unlike fundamental types, which you can use directly, **compound types like strings** require including their library in the code. For strings, this means adding the `<string>` header to give the program access to the standard string class:

```cpp
#include <string>  // Include this to use std::string

std::string greeting = "Hello, world!";
```

The `<string>` header provides all the functionality needed to declare, modify, and manipulate string objects in your program. This includes features like concatenation, comparison, and searching, making it easy to work with text data in C++.

### Type Conversions (Casting)

### Implicit Conversions (Automatic)

- Occur when converting between compatible types, such as from `int` to `float` or `double`.
- Generally safe but can sometimes lead to precision loss or unexpected behavior (e.g., converting `double` to `int` truncates the decimal).

  ```cpp
  int a = 10;
  double b = a; // Implicitly converts 'int' to 'double'
  ```

### Explicit Conversions (Casting)

- Used when more control is needed, especially between incompatible types.
- C++ offers four types of casts for explicit conversions:

  - **static_cast**: Converts between compatible types safely (e.g., `int` to `float`).
  - **const_cast**: Adds or removes the `const` qualifier.
  - **dynamic_cast**: Safe casting for pointers/references within an inheritance hierarchy.
  - **reinterpret_cast**: Forces a conversion between incompatible types (use with caution).

  ```cpp
  int a = 10;
  double b = static_cast<double>(a); // Explicitly converts 'int' to 'double'
  ```

Explicit conversions provide more control over data transformation, while implicit conversions offer convenience but should be used carefully to avoid unintended effects.

## Type Modifiers

- **`const`:** Indicates that a variable's value cannot be changed.
- **`volatile`:** Informs the compiler that a variable's value can be changed by external sources.
- **`mutable`:** Allows modification of a class member even if the containing object is declared as `const`.
- **`static`:** Modifies the lifetime and visibility of variables and functions.
- **`extern`:** Declares a variable or function as defined elsewhere.
- **`register`:** Suggests to the compiler that a variable should be stored in a CPU register for faster access.
- **`auto`:** Automatically deduces the data type of a variable at compile time.
- **`decltype`:** Deduces the type of an expression at compile time.
- **`typedef`:** Creates an alias for a data type.
- **`using`:** Introduces a type alias or simplifies template syntax.

**Additional Considerations:**

- **Memory Management:** Understand how memory is allocated and deallocated for variables.
- **Operator Precedence and Associativity:** Follow operator precedence rules to ensure correct evaluation of expressions.
