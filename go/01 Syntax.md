# Go Syntax

## Hello, World

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

- `package main`: Every Go program is made up of one or more packages. `main` is the entry point of a Go program.
- `import "fmt"`: Go includes a standard library that provides a set of basic functionalities like printing to the console.
- `func main()`: The `main` function is where the program starts executing.

---

## Basic Types

- **Boolean**:  
  `bool`

- **String**:  
  `string`

- **Integer Types**:  
  `int`, `int8`, `int16`, `int32`, `int64`,  
  `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`

- **Byte (alias for `uint8`)**:  
  Used to represent a raw byte.

- **Rune (alias for `int32`)**:  
  Represents a Unicode code point.

- **Floating-Point Types**:  
  `float32`, `float64`

- **Complex Types**:  
  `complex64`, `complex128`

- The `int`, `uint`, and `uintptr` types are platform-dependent. On 32-bit systems, they are usually 32 bits wide; on 64-bit systems, they are 64 bits wide.
- Use `int` by default when an integer is required unless you need a specific size or an unsigned integer type.

## Variables and Constants

In Go, variables are declared using the `var` keyword. Variables can be declared at the package level or within functions.

```go
var age int // Declares a variable 'age' of type int
age = 30    // Assigns a value to the variable 'age'


var a, b int = 1, 2  // Declares two variables 'a' and 'b' with initial values

name := "John"  // shorthand for 'var name string = "John"'
```

This shorthand can only be used inside functions and automatically infers the type based on the initializer.

Go allows multiple variables to be declared in a single statement:

```go
var c, java, age = true, false, "no!", 50
```

In this example, `c` is inferred to be a `bool`, `java` is a `bool`, and `age` is an `int`.

If a variable is declared but not initialized, it will automatically take its **zero value**. The zero values for basic types are:

- `0` for numeric types (e.g., `int`, `float64`)
- `false` for `bool`
- `""` (empty string) for `string`

```go
var i int       // Zero value is 0
var f float64   // Zero value is 0.0
var b bool      // Zero value is false
var s string    // Zero value is ""
```

Constants in Go are declared using the `const` keyword and their values cannot be changed.

Constants must be assigned values at the time of declaration, and their types are inferred based on the value. Constants cannot use the shorthand `:=` syntax.

```go
const PI = 3.14
```

## Type Conversion

In Go, you can convert between compatible types explicitly. For example:

```go
i := 42           // Declare an integer variable
f := float64(i)   // Convert 'i' to a float64
u := uint(f)      // Convert 'f' to a uint
```

## Functions

Functions in Go are declared using the `func` keyword. You can define a function with parameters and return types.

```go
// Simple function that returns a greeting message
func greet(name string) string {
    return "Hello, " + name
}

// Function returning multiple values: full name and an error
func getFullName(firstName, lastName string) (string, error) {
    if strings.TrimSpace(firstName) == "" || strings.TrimSpace(lastName) == "" {
        return "", fmt.Errorf("first and last name cannot be empty")
    }
    return fmt.Sprintf("%s %s", firstName, lastName), nil
}

// Omit the type for parameters with the same type
func greet(name, message string) string {
    return message + ", " + name
}
```

### Variadic Functions

**Variadic functions** allow passing a variable number of arguments. The syntax uses `...` before the type to define a variadic parameter.

```go
// Function summing a variable number of integers
func sum(numbers ...int) int {
    total := 0
    for _, number := range numbers {
        total += number
    }
    return total
}

// Call variadic function
result := sum(1, 2, 3, 4, 5) // result: 15
```

### Functions as First-Class Citizens

Functions in Go are **first-class citizens**, meaning they can be assigned to variables, passed as arguments, and returned from other functions.

```go
// Assigning a function to a variable
add := func(a, b int) int { return a + b }
result = add(3, 4) // result: 7

// Passing a function as an argument
func apply(f func(int, int) int, a, b int) int {
    return f(a, b)
}
result = apply(add, 5, 6) // result: 11

// Returning a function from another function
func multiplier(factor int) func(int) int {
    return func(x int) int { return x * factor }
}
double := multiplier(2)
result = double(5) // result: 10
```

### Defer, Panic, and Recover

Go provides **defer**, **panic**, and **recover** for managing function execution flow.

The `defer` keyword postpones execution of a function until the surrounding function returns. Deferred functions run in LIFO order.

```go
func example() {
    defer fmt.Println("This will be printed last")
    fmt.Println("This will be printed first")
}
example()
// Output:
// This will be printed first
// This will be printed last
```

`panic` stops the execution of a function, while `recover` helps handle panics and regain control.

```go
func divide(a, b int) int {
    if b == 0 { panic("division by zero") }
    return a / b
}

func main() {
    defer func() {
        if r := recover(); r != nil { fmt.Println("Recovered from panic:", r) }
    }()

    fmt.Println(divide(4, 2)) // Output: 2
    fmt.Println(divide(4, 0)) // Recovered from panic: division by zero
}
```

## Control Structures

Go includes the usual control structures like `if`, `else`, `for`, and `switch`.

### If/Else

```go
x := 10
if x > 5 {
    fmt.Println("Greater than 5")
} else {
    fmt.Println("Less than or equal to 5")
}
```

### Switch

Go’s `switch` is more flexible than most languages, with no need for `break`.

```go
day := 3
switch day {
case 1:
    fmt.Println("Monday")
case 2:
    fmt.Println("Tuesday")
case 3:
    fmt.Println("Wednesday")
default:
    fmt.Println("Other day")
}
```

### For Loop

The `for` loop in Go is the only loop. There are no `while` loops.

```go
for i := 0; i < 5; i++ {
    fmt.Println(i)
}
```

---

## Arrays and Slices

### Arrays

Arrays are fixed-size collections of elements of the same type.

```go
var numbers [3]int
numbers[0] = 1
numbers[1] = 2
numbers[2] = 3
fmt.Println(numbers)
```

### Slices

Slices are dynamic, flexible views into arrays.

```go
s := []int{1, 2, 3}
fmt.Println(s)
```

Slices can be expanded and contracted, unlike arrays.

---

## Structs

Structs are composite types that group together variables (fields) of different types.

```go
type Person struct {
    Name string
    Age  int
}

p := Person{"John", 30}
fmt.Println(p.Name)
```

---

## Pointers

Go supports pointers, but they are less common than in languages like C/C++.

```go
var x int = 58
var ptr *int = &x
fmt.Println(ptr)
fmt.Println(*ptr)
```

---

## Interfaces

Interfaces in Go are used to define a set of methods. A type is considered to implement an interface if it provides implementations for all the methods declared by the interface.

### Defining an Interface

```go
type Speaker interface {
    Speak() string
}

type Person struct {
    Name string
}

func (p Person) Speak() string {
    return "Hello, " + p.Name
}

var s Speaker = Person{"John"}
fmt.Println(s.Speak())
```

---

## Concurrency with Goroutines

One of Go's standout features is its easy-to-use concurrency model. Goroutines are lightweight threads that run concurrently.

### Starting a Goroutine

```go
go func() {
    fmt.Println("This runs concurrently")
}()
```

### Channels

Channels are used to communicate between goroutines.

```go
ch := make(chan string)

go func() {
    ch <- "Hello from goroutine"
}()

msg := <-ch
fmt.Println(msg)
```

---

## Packages

Go encourages modular programming by using packages. Packages help organize code into reusable components. The Go standard library includes many useful packages, and you can create your own.

### Importing a Package

```go
import "fmt"
```

Each Go file must declare its imports at the top, and you can have multiple imports, either grouped or on separate lines.
