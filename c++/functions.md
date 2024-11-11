# Functions

## Function Definition

The general syntax for defining a function in C++ is:

```cpp
type name(parameter1, parameter2, ...) {
    // statements
}
```

- **type**: Specifies the return type of the function (use `void` if it returns nothing).
- **name**: The function’s identifier.
- **parameters**: The list of input arguments.
- **statements**: The body of the function.

## Function Declaration (Prototype)

A function prototype declares a function's return type and parameters without defining its body. This allows the function to be called before it’s defined.

The parameter names are optional in the declaration. They can be omitted, as they are not needed to specify the function's prototype, but they it is common to include them for documentation purposes.

```cpp
int add(int a, int b); // Function prototype
int add(int, int);     // Prototype without parameter names
```

## Default Arguments

Specify default values for parameters, allowing them to be omitted in function calls.

```cpp
int add(int a, int b = 0) {
    return a + b;
}
```

## Argument Passing: By Value vs. By Reference

### Pass by Value

When passing arguments by value, a copy of the argument is made and passed to the function.
This means that changes made to the argument within the function do not affect the original value.

```cpp
void increment(int x) { x++; }

```

### Pass by Reference

When passing arguments by reference, the function receives the actual argument, not a copy.

```cpp
void increment(int& x) { x++; }
```

## Efficiency considerations and const references

Passing by reference is more efficient than passing by value, especially for compound data types like arrays or objects.
If the function does not modify the argument, it is good practice to use a `const` reference to prevent accidental changes.
But for most fundamental types, there is no noticeable difference in efficiency, and in some cases, const references may even be less efficient!

```cpp
string concatenate(const string& a, const string& b) { code; }
```

## Inline Functions

The `inline` keyword suggests to the compiler that a function's code should be inserted directly into the calling code instead of being called as a separate function.

This is useful for small functions that are called frequently, as it can reduce the overhead of function calls.

```cpp
inline type name ( parameter1, parameter2, ...) { statements }
```

## Function Overloading

Function overloading allows multiple functions with the same name but different parameters. The compiler distinguishes them based on the argument types or numbers.

```cpp
int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
```

## Function Templates

Function templates allow you to define a function with generic types that are specified when the function is called.

```cpp
template <typename T>
T add(T a, T b) {
    T result; // T also can be used to declare variables inside the function
    result = a + b;
    return result;
 }
```
