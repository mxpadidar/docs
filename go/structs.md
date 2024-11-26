# **Struct in Go**

## **Basic Syntax**

To define and use a struct in Go:

```go
// Define a struct
type Person struct {
    Name string
    Age  int
}

// Create a new instance using a struct literal
p := Person{
    Name: "Alice",
    Age:  30,
}

// Create a new instance using the 'new' keyword
p := new(Person) // Returns a pointer to a Person
p.Name = "Alice"
p.Age = 30

// Create a new instance using a struct literal and take its address
p := &Person{
    Name: "Alice",
    Age:  30,
}

// Access and modify fields using dot notation
fmt.Println(p.Name) // Output: Alice
p.Age = 31          // Modify the Age field
```

## **Struct Composition**

Composition allows you to create new types by embedding existing structs. It is Go’s way of achieving a form of inheritance.

```go
type Address struct {
    City    string
    ZipCode string
}

type Employee struct {
    Person
    Address
    EmployeeID int
}

e := Employee{
    Person: Person{
        Name: "Bob",
        Age:  25,
    },
    Address: Address{
        City:    "New York",
        ZipCode: "10001",
    },
    EmployeeID: 12345,
}

// Access embedded struct fields directly
fmt.Println(e.Name)    // Output: Bob
fmt.Println(e.City)    // Output: New York
fmt.Println(e.Address) // Output: {New York 10001}
```

## **Struct Constructors**

Go does not have explicit constructors, but you can create factory functions to initialize structs:

```go
func NewPerson(name string, age int) *Person {
    return &Person{
        Name: name,
        Age:  age,
    }
}

p := NewPerson("Alice", 30)
fmt.Println(p.Name) // Output: Alice
```

---

## **Struct Methods**

Methods in Go are functions with a receiver, which is a reference to the struct. Receivers can be either by value or by pointer:

- **Pointer receiver**: Use this when you want to modify the original struct or avoid copying large structs.
- **Value receiver**: Use this for small structs when you don't need to modify the original.

```go
// Method with a pointer receiver
func (p *Person) Greet() string {
    return "Hello, my name is " + p.Name
}

// Method with a value receiver
func (p Person) IsAdult() bool {
    return p.Age >= 18
}

p := Person{Name: "Alice", Age: 30}
fmt.Println(p.Greet())   // Output: Hello, my name is Alice
fmt.Println(p.IsAdult()) // Output: true
```

## **Tags in Struct Fields**

Struct fields can have tags, which are string metadata often used in tasks like encoding/decoding (e.g., JSON, XML). Tags are accessed via reflection.

```go
type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

u := User{
    ID:    1,
    Name:  "John Doe",
    Email: "john@example.com",
}

// Encode struct to JSON
data, _ := json.Marshal(u)
fmt.Println(string(data)) // Output: {"id":1,"name":"John Doe","email":"john@example.com"}
```

## **Anonymous Structs**

Go supports anonymous structs, useful for one-off data structures:

```go
p := struct {
    Name string
    Age  int
}{
    Name: "Alice",
    Age:  30,
}

fmt.Println(p.Name) // Output: Alice
```

## **Comparing Structs**

Structs in Go can be compared using the `==` and `!=` operators. Two structs are equal if all their fields are equal:

```go
p1 := Person{Name: "Alice", Age: 30}
p2 := Person{Name: "Alice", Age: 30}

fmt.Println(p1 == p2) // Output: true
```

### Note

- Only comparable fields (e.g., numbers, strings, or other comparable structs) can be compared.
- Structs with slice, map, or function fields cannot be directly compared.

## **Copying Structs**

Assigning a struct creates a copy. Modifications to the new struct do not affect the original:

```go
p1 := Person{Name: "Alice", Age: 30}
p2 := p1

p2.Age = 31
fmt.Println(p1.Age) // Output: 30
fmt.Println(p2.Age) // Output: 31
```

Use pointers to share data between structs:

```go
p1 := &Person{Name: "Alice", Age: 30}
p2 := p1
p2.Age = 31

fmt.Println(p1.Age) // Output: 31
```

## **Embedding Interfaces in Structs**

Structs can implement interfaces implicitly, allowing for polymorphism:

```go
type Greeter interface {
    Greet() string
}

type Person struct {
    Name string
}

func (p Person) Greet() string {
    return "Hello, " + p.Name
}

var g Greeter = Person{Name: "Alice"}
fmt.Println(g.Greet()) // Output: Hello, Alice
```

## **Zero Value of Structs**

The zero value of a struct is a struct with all its fields set to their zero values:

```go
type Person struct {
    Name string
    Age  int
}

var p Person
fmt.Println(p) // Output: { 0}
```

## **Best Practices**

1. **Use pointers** when you need to modify struct fields or avoid copying large structs.
2. **Avoid embedding large structs**; use pointers instead for better performance.
3. **Leverage tags** for encoding, validation, or metadata.
4. **Prefer constructors** for initializing complex structs.
5. **Use composition** to share common fields across structs without resorting to inheritance.
