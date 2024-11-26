# **Functions in Go**

## **Basics**

Functions in Go are declared using the `func` keyword. Parameters and return types are optional.

```go
// Syntax
func functionName(param1 param1Type, param2 param2Type, ...) returnType {
  return result
}

// Example: Simple function with parameters and a single return value
func sum(a int, b int) int { return a + b }
func sum(a, b int) int {} // Parameters of the same type can be grouped


// Function with multiple return values (commonly used for error handling)
func divide(a, b int) (int, error) {
  if b == 0 { return 0, fmt.Errorf("cannot divide by zero") } // 0, error
  return a / b, nil // a/b, nil
}

// Named Return Values
func rectangleArea(length, width int) (area int) { // area initialized to 0 value
  area = length * width
  return // Returns the named variable 'area'
}

// Variadic Functions
func sumAll(nums ...int) int { // nums is a slice of int
  total := 0
  for _, n := range nums { total += n }
  return total
}

// Anonymous Functions
func(params) { function body }() // Inline execution

// Assign an anonymous function to a variable
greet := func(name string) { fmt.Println("Hello,", name) }
greet("Alice") // Output: Hello, Alice
```

## **Closures**

Closures are functions that capture and use variables from their surrounding scope.

```go
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

increment := counter()
fmt.Println(increment()) // Output: 1
fmt.Println(increment()) // Output: 2
```

## **Higher-Order Functions**

Functions in Go can accept other functions as arguments or return them.

```go
func apply(f func(int) int, value int) int {
    return f(value)
}

double := func(x int) int {
    return x * 2
}

fmt.Println(apply(double, 5)) // Output: 10
```

## **Methods**

Methods are functions with a receiver, allowing them to operate on a struct or a pointer to a struct.

```go
type Person struct {
    Name string
}

// Method with a value receiver
func (p Person) Greet() string {
    return "Hello, " + p.Name
}

// Method with a pointer receiver
func (p *Person) ChangeName(newName string) {
    p.Name = newName
}

p := Person{Name: "Alice"}
fmt.Println(p.Greet()) // Output: Hello, Alice

p.ChangeName("Bob")
fmt.Println(p.Greet()) // Output: Hello, Bob
```

## **Defer in Functions**

The `defer` keyword schedules a function call to execute after the surrounding function completes. Deferred calls are executed in **LIFO** order.

Defer is commonly used for resource cleanup, like closing files or releasing locks.

```go
func example() {
    defer fmt.Println("Deferred message 1")
    defer fmt.Println("Deferred message 2")
    fmt.Println("Normal message")
}

example()
// Output:
// Normal message
// Deferred message 2
// Deferred message 1
```

## **Error Handling with `Panic` and `Recover`**

- **Panic**: Used to stop program execution for severe errors.
- **Recover**: Used within deferred functions to regain control after a panic.

```go
func safeDivide(a, b int) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from panic:", r)
        }
    }()

    if b == 0 {
        panic("division by zero")
    }

    fmt.Println(a / b)
}

safeDivide(10, 2) // Output: 5
safeDivide(10, 0) // Output: Recovered from panic: division by zero
```

## **Key Points**

1. Functions are first-class citizens in Go.
2. Go's error handling philosophy uses multiple return values (`value, error`) instead of exceptions.
3. The use of `defer`, `panic`, and `recover` provides basic control for resource cleanup and error recovery.
4. Closures and higher-order functions make Go flexible for functional programming patterns.

## **Best Practices**

1. **Use meaningful names** for functions and parameters to improve readability.
2. **Keep functions small** and focused on a single responsibility.
3. **Return errors** explicitly rather than using panic, except for truly exceptional cases.
4. **Use variadic functions** sparingly to avoid misuse or confusion.
5. **Leverage defer** for resource cleanup like closing files or releasing locks.
