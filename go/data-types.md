# **Variables and Constants in Go**

## **Basic Data Types**

1. **Integer (`int`)**:

   - Represents whole numbers (e.g., `1`, `42`).
   - Default size is platform-dependent (`int32` or `int64`).

2. **Floating-Point (`float64`)**:

   - Represents decimal numbers (e.g., `3.14`, `2.718`).

3. **String (`string`)**:

   - Represents text (e.g., `"hello"`, `"Go"`).
   - Immutable.

4. **Rune (`rune`)**:
   - Represents a Unicode code point (e.g., `'A'`, `'😊'`).

Other numeric types include `int8`, `int16`, `int32`, `int64`, `float32`, `complex64`, `complex128`, and unsigned integers (`uint8`, `uint16`, etc.).

---

## **Variables**

Variables in Go are defined using the `var` keyword or shorthand notation (`:=`).

```go
var x int // Declaration with default value (0 for int)
x = 10    // Assignment

// Short Declaration
y := 20 // Declaration and assignment (type inferred)

// Multiple Variable Declaration
var a, b, c int = 1, 2, 3 // Declare multiple variables of the same type
name, age := "Alice", 30  // Declare and initialize using shorthand
```

### **Variable Scope**

- **Local Scope**: Declared inside a function and are only accessible within that function.
- **Block Scope**: Variables declared inside a block are only accessible within that block.
- **Global Scope**: Declared outside of any function and are accessible throughout the package.

```go
var global = 100 // Global variable

func main() {
    var local = 10 // Local variable
    if true {
        var block = 20 // Block-scoped variable
        fmt.Println(local, block, global)
    }
    fmt
}
```

### **Default Values**

Uninitialized variables are assigned their **zero value**:

- `int`: `0`
- `float64`: `0.0`
- `string`: `""` (empty string)
- `bool`: `false`

### **Default values vs nil**

**Zero Value:** Default initialized values (e.g., 0 for numbers, "" for strings).
**nil:** Represents "no value" for reference types (e.g., pointers, slices, maps).

```go
var s []int // Default is `nil`
if s == nil {
fmt.Println("Slice is nil")
}
```

### **Type Conversion**

Go requires explicit type conversion between different types.

```go
var x int = 10
var y float64 = float64(x) // Convert int to float64
```

## **Constants**

Constants in Go are immutable values defined using the `const` keyword.

```go
const Pi = 3.14159

// Multiple Constant Declaration
const (
    Language = "Go"
    MaxValue = 100
)

// The `iota` keyword generates a sequence of constant values. It resets to 0 in each `const` block.

const (
    First  = iota // 0
    Second        // 1
    Third         // 2
)
```
