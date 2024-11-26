# **Flow Control in Go**

## **1. If Statements**

The `if` statement is used for conditional execution.

```go
// Basic if-else structure
if condition {
    // Code block
} else if anotherCondition {
    // Code block
} else {
    // Code block
}

// If with initialization (variable is scoped to the block)
if val := getValue(); val > 10 {
    // Code block
}
```

## **2. Switch Statements**

The `switch` statement simplifies multi-way branching.

```go
// Basic switch
switch expression {
case value1:
    // Code for value1
case value2:
    // Code for value2
default:
    // Code if no case matches
}

// Switch with initialization
switch variable := getValue(); variable {
case value1:
    // Code for value1
case value2:
    // Code for value2
default:
    // Code if no case matches
}

// Switch without an expression (like switch true)
switch {
case condition1:
    // Code for condition1
case condition2:
    // Code for condition2
default:
    // Code if no case matches
}

// Using fallthrough
// By default, Go's `switch` does not fall through to the next case.
// Use `fallthrough` explicitly when needed.
switch variable {
case value1:
    // Code for value1
    fallthrough // Proceed to the next case
case value2:
    // Code for value2
default:
    // Default case
}
```

## **3. For Loops**

Go's `for` loop is versatile and covers `while` and `do-while` use cases.

```go
// Basic for loop
for initialization; condition; post {
    if someCondition {
        continue // Skip to the next iteration
    } else if anotherCondition {
        break // Exit the loop
    }
}

// Iterating with an index
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

// While-like loop
x := 0
for x < 5 {
    fmt.Println(x)
    x++
}

// Infinite loop
for {
    fmt.Println("Running forever")
    break // Optional, to prevent infinite execution
}
```

## **4. Defer**

The `defer` statement postpones the execution of a function until the enclosing function returns. Deferred calls are executed in **LIFO (Last In, First Out)** order.

### **Examples**

```go
// Basic defer usage
func main() {
    defer fmt.Println("World")
    fmt.Println("Hello")
}
// Output:
// Hello
// World

// Closing resources
func readFile() {
    file, _ := os.Open("example.txt")
    defer file.Close()
    // Perform operations on the file
}

// Unlocking a mutex
mutex.Lock()
defer mutex.Unlock()
// Perform critical section operations
```

## **5. Panic and Recover**

- **`panic`**: Stops execution and begins unwinding the stack. Use for unrecoverable errors.
- **`recover`**: Regains control after a `panic`. Typically called in a deferred function.

```go
// Triggering a panic
func main() {
    panic("Something went wrong!")
}

// Handling a panic with recover
func main() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from panic:", r)
        }
    }()
    panic("Oops!") // Will be caught by recover
}
```

## **6. Select Statements**

The `select` statement allows for communication across multiple channels. It waits for one of its cases to proceed.

### **Syntax and Examples**

```go
// Basic select
select {
case val := <-ch1:
    fmt.Println("Received from ch1:", val)
case ch2 <- value:
    fmt.Println("Sent to ch2")
default:
    fmt.Println("No communication")
}

// Example with goroutines and channels
func main() {
    ch1 := make(chan int)
    ch2 := make(chan int)

    go func() { ch1 <- 42 }()
    go func() { ch2 <- 7 }()

    select {
    case val := <-ch1:
        fmt.Println("Received:", val)
    case ch2 <- 99:
        fmt.Println("Sent 99 to ch2")
    default:
        fmt.Println("No communication")
    }
}
```

---

## **Key Takeaways**

1. **`if`, `switch`, and `for`**: These fundamental constructs cover most control flow scenarios in Go.
2. **`defer`**: Ideal for resource management (e.g., closing files or releasing locks).
3. **`panic` and `recover`**: Use sparingly for handling critical, non-recoverable errors.
4. **`select`**: Essential for managing concurrent operations with channels.
