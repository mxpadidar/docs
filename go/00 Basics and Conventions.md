# Getting Started with Go: Project Setup and Basics

This guide introduces the essential steps for setting up a Go project, organizing code, and understanding key concepts like exported names and module management.

---

## Table of Contents

1. [Creating a New Go Project](#creating-a-new-go-project)
2. [Exported and Unexported Names in Go](#exported-and-unexported-names-in-go)
3. [Cleaning Up Dependencies with `go mod tidy`](#cleaning-up-dependencies-with-go-mod-tidy)

---

## Creating a New Go Project

```bash
mkdir project_name
cd project_name

# Initialize a Go module
go mod init project_name
```

This command creates a `go.mod` file, which defines the project’s module name and manages dependencies. A Go module is a collection of Go packages, organized by a `go.mod` file at the root.

The `go.mod` file is updated whenever dependencies change. Additionally, Go uses `go.sum` to store checksums for all dependencies, ensuring consistency.

The entry point for a Go application is typically a `main.go` file in the root directory.

```go
// main.go
package main

import "fmt"

func main() {
    fmt.Println("Welcome to the Go project!")
}
```

To run the program, use:

```bash
go run main.go
```

### Organizing Code with Packages

Go organizes code into **packages**. Each directory within a project can represent a package. By convention:

- **Package Naming**: The package name should match the directory name. For example, code inside the `utils` directory should use `package utils`.
- **The `main` Package**: The `main` package is special because it defines the entry point of the application.

Here’s an example structure for a Go project:

```bash
project_name/       # Project root directory
├── go.mod          # Go module file
├── go.sum          # Dependency checksums
├── main.go         # Main application file
└── utils/          # Utility package
    └── helper.go   # Source file for utils package
```

To use one package within another, import it by referencing the module path:

```go
// utils/helper.go
package utils

import "fmt"

// PrintMessage is an exported function that prints a message
func PrintMessage(msg string) {
    fmt.Println(msg)
}

// main.go
package main

import (
    "project_name/utils"
)

func main() {
    utils.PrintMessage("Hello from the utils package!")
}
```

## Exported and Unexported Names in Go

Go uses naming conventions to control the visibility of functions, variables, and constants within and outside of a package:

- **Exported Names**: Identifiers that start with an uppercase letter are exported and accessible outside the package (e.g., `PrintMessage`).
- **Unexported Names**: Identifiers that start with a lowercase letter are unexported, meaning they are private to the package (e.g., `printMessage`).

```go
// utils/helper.go
package utils

import "fmt"

// printMessage is an unexported (private) function
func printMessage(msg string) {
    fmt.Println(msg)
}

// PrintMessage is an exported (public) function
func PrintMessage(msg string) {
    printMessage(msg)
}
```

## Cleaning Up Dependencies with `go mod tidy`

As a project evolves, dependencies may be added or removed. The `go mod tidy` command helps maintain a clean dependency set by performing the following tasks:

- **Remove Unused Dependencies**: Deletes entries in `go.mod` that are no longer used in the code.
- **Add Missing Dependencies**: Ensures any libraries referenced in the code but missing from `go.mod` are added.
- **Update `go.sum`**: Refreshes all checksums, ensuring they match the current dependency versions.

This command helps keep `go.mod` and `go.sum` organized and accurate.

## Naming Conventions in Go

**Package Names:** Should be short and lowercase. Avoid underscores and camel case (e.g., httpclient or utils).

**Function and Variable Names:** Use mixed case (camel case) but start with lowercase for unexported names and uppercase for exported names.

**Constants:** Should be in all uppercase letters, with underscores separating words (e.g., MAX_RETRIES).

**File Names:** Should be lowercase and use underscores to separate words (e.g., http_server.go).

**Directory Names:** Should be lowercase and use underscores to separate words (e.g., http_utils).
