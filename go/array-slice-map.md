# **Arrays, Slices, and Maps in Go**

## **1. Arrays**

An **array** in Go is a fixed-size collection of elements of the same type. The size is part of the array's type, so `[5]int` and `[10]int` are different types.

- Fixed size.
- Default value for numeric arrays: `0`.
- Comparisons: Arrays are comparable if their elements are comparable (e.g., `[3]int == [3]int`).

```go
// Declare an array of size 3
var arr [3]int

// Initialize an array
arr = [3]int{1, 2, 3}

// Short declaration
arr := [3]int{4, 5, 6}

// Automatic length determination
arr := [...]int{7, 8, 9}

// Accessing elements (zero-based indexing)
fmt.Println(arr[0]) // Output: 7

// Updating elements
arr[2] = 10

// Iterating Over Arrays
arr := [3]int{1, 2, 3}

for i, val := range arr {
    fmt.Printf("Index %d: Value %d\n", i, val)
}
```

## **2. Slices**

An array without a specified size is a slice. A slice is a dynamic, flexible view into an underlying array.

- Backed by an array.
- Length (`len(slice)`) and capacity (`cap(slice)`) can differ.
- Default value for numeric slices: `nil` (not the same as an empty slice).

```go
// Declare a slice
var slice []int // like arrays but without a size

// Initialize with values
slice = []int{1, 2, 3}

// Short declaration
slice := []int{4, 5, 6}

// Create a slice from an array
arr := [5]int{1, 2, 3, 4, 5}
slice := arr[1:4] // Elements from index 1 to 3 (4 is excluded)

// Create a slice using `make`
slice := make([]int, 5)       // Length: 5, Capacity: 5
slice := make([]int, 5, 10)   // Length: 5, Capacity: 10


// slicing and copying
slice := []int{1, 2, 3, 4, 5}

// Sub-slicing
subSlice := slice[1:4] // [2, 3, 4]

// Copying slices
copySlice := make([]int, len(slice))
copy(copySlice, slice)
fmt.Println(copySlice) // [1, 2, 3, 4, 5]

// iterating over slices
for i, val := range slice {
    fmt.Printf("Index %d: Value %d\n", i, val)
}

// appending elements
slice := []int{1, 2, 3}

// Append single or multiple elements
slice = append(slice, 4)           // [1, 2, 3, 4]
slice = append(slice, 5, 6, 7)     // [1, 2, 3, 4, 5, 6, 7]

// Append another slice
slice2 := []int{8, 9}
slice = append(slice, slice2...)   // [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Slice capacity and length

Slices have two important properties: length and capacity. These properties can differ.

**Length (len(slice))**
The length of a slice is the number of elements it currently holds.
It is determined by the number of elements between the start of the slice and its end.

**Capacity (cap(slice))**
The capacity of a slice is the number of elements the slice can hold before needing to allocate more memory.
It is determined by the number of elements between the start of the slice and the end of the underlying array.

When you append elements to a slice and the capacity is exceeded, Go allocates a new array with a larger capacity. Usually, the new capacity is double the old capacity. The existing elements are copied to the new array. The new elements are appended to the new array. The slice now references the new array. This automatic resizing makes slices flexible and convenient to use, as you don't need to manually manage the underlying array's size.

```go
slice := []int{1, 2, 3}
fmt.Println(len(slice)) // Output: 3
fmt.Println(cap(slice)) // Output: 3

// Append an element
slice = append(slice, 4)
fmt.Println(len(slice)) // Output: 4
fmt.Println(cap(slice)) // Output: 6 >> capacity doubled
```

## **3. Maps**

A **map** is a collection of key-value pairs, where each key is unique. Maps in Go are implemented as hash tables.

- Keys must be of a comparable type (e.g., `int`, `string`, `bool`).
- Values can be of any type.
- Default value for a non-existent key: Zero value of the value type.

```go
// Declare a map
var m map[string]int // key: string, value: int

// Initialize a map using `make`
m = make(map[string]int)

// Short declaration
m := map[string]int{
    "Alice": 25,
    "Bob":   30,
}

// Add or update key-value pairs
m["Charlie"] = 35
m["Alice"] = 28

// Accessing a value
age := m["Alice"]
fmt.Println(age) // Output: 28

// Check if a key exists
age, exists := m["Unknown"]
if exists {
    fmt.Println("Found:", age)
} else {
    fmt.Println("Key not found")
}

// Delete a key-value pair
delete(m, "Bob")

// iterating over maps
m := map[string]int{"Alice": 25, "Bob": 30}

for key, value := range m {
    fmt.Printf("Key: %s, Value: %d\n", key, value)
}
```

### **Maps Are Reference Types**

```go
m1 := map[string]int{"Alice": 25}
m2 := m1

m2["Alice"] = 30
fmt.Println(m1["Alice"]) // Output: 30 (m1 and m2 point to the same map)
```

## **Comparison of Arrays, Slices, and Maps**

| Feature           | Arrays                | Slices                        | Maps               |
| ----------------- | --------------------- | ----------------------------- | ------------------ |
| **Size**          | Fixed                 | Dynamic                       | Dynamic            |
| **Default Value** | Zero value elements   | `nil`                         | `nil`              |
| **Indexing**      | Yes                   | Yes                           | No (use keys)      |
| **Capacity**      | Fixed                 | Can grow dynamically          | Not applicable     |
| **Iteration**     | `for` or `range`      | `for` or `range`              | `range`            |
| **Key-Value**     | No                    | No                            | Yes                |
| **Usage**         | Low-level, fixed data | Dynamic, flexible collections | Associative arrays |
