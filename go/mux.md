# What Is a Mux?

## Understanding "Mux"

Mux is short for **multiplexer**. While the term may not be familiar to many, its concept is simple:

**Multiplexer**  
_A device that enables the simultaneous transmission of several messages or signals over one communications channel._ – _Dictionary.com_

In the context of Go programming, a **mux** refers to an **HTTP request multiplexer**. Its job is to match incoming request URLs to pre-defined routes and execute the appropriate handler when a match is found. Think of it as a gateway into your application, directing requests to the right destination.

---

## Creating a Custom Mux

Here's an example of a simple Go web application using a custom mux:

```go
package main

import (
    "log"
    "net/http"
)

func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("This is the home page."))
}

func aboutHandler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("This is the about page."))
}

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("/", homeHandler)
    mux.HandleFunc("/about", aboutHandler)

    log.Fatal(http.ListenAndServe(":8080", mux))
}
```

---

### Step-by-Step Breakdown

#### **1. Creating a ServeMux**

```go
mux := http.NewServeMux()
```

This initializes a new instance of `ServeMux`. A `ServeMux` is Go's implementation of an HTTP request multiplexer.

#### **2. Registering Routes**

```go
mux.HandleFunc("/", homeHandler)
mux.HandleFunc("/about", aboutHandler)
```

`HandleFunc` registers a handler function for a specific route. Here, we map:

- `/` to `homeHandler`
- `/about` to `aboutHandler`

Whenever a request matches one of these routes, the corresponding handler function will be called.

#### **3. Writing Handlers**

```go
func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("This is the home page."))
}
```

Handlers process incoming requests and generate responses. Each handler receives:

- **`w`** (`http.ResponseWriter`): Used to write data back to the client.
- **`r`** (`*http.Request`): Provides access to request details like headers, body, and method.

#### **4. Starting the Server**

```go
log.Fatal(http.ListenAndServe(":8080", mux))
```

This starts the HTTP server on port `8080`, using our `mux` for request handling. If you pass `nil` instead of `mux`, the server uses the `DefaultServeMux`, which is a global variable. Avoid relying on `DefaultServeMux` to prevent unexpected behavior caused by external packages.

---

## How Does a Mux Work Internally?

Under the hood, a `ServeMux` works as follows:

```go
type ServeMux struct {
    mu    sync.RWMutex
    m     map[string]muxEntry
    es    []muxEntry
    hosts bool
}

type muxEntry struct {
    h       Handler
    pattern string
}
```

### Key Fields

1. **`m`**: A map of URL patterns to `muxEntry`. Each entry pairs a URL pattern with its handler.
2. **`es`**: An ordered list of `muxEntry` objects, used for pattern matching.
3. **`hosts`**: Determines if host-based URL matching is enabled.

### URL Matching

- When a request arrives, `ServeMux` iterates through registered patterns to find the most specific match.
- A match is determined by comparing the request's URL with each registered pattern.
- If a matching pattern is found, its associated handler is executed.

---

## Conclusion

This guide introduced the concept of an HTTP multiplexer (mux) and demonstrated how to use Go's `http.NewServeMux` to create one.

Muxes are essential for routing requests in Go web applications, providing a robust and extensible mechanism to define and manage routes.

Stay tuned for the next post in the series, where we’ll explore **handlers** in more detail!
