# Project Structure

In larger C++ projects, a well-organized folder and file structure helps improve readability, maintainability, and collaboration. By structuring files according to their roles and using consistent naming conventions, developers can manage complex projects more efficiently. Below is an explanation of typical categories in a C++ project structure:

## Source Files (`src/`, `main.cpp`)

Contains the primary implementation of the program's functionality. These files include the main logic and definitions for functions and classes. Typically, C++ source files have a `.cpp` extension.

- All `.cpp` files are placed within the `src/` folder.
- The entry point of the program, `main.cpp`, usually resides in this folder as well.

```bash
src/
├── main.cpp
├── utils.cpp
└── module.cpp
```

## Header Files (`include/`, `utils.h`)

Declare functions, classes, and constants that are defined in source files. Header files provide an interface for other files to use these declarations without needing to know the implementation. Header files commonly use a `.h` or `.hpp` extension. Header files are stored in the `include/` folder, often mirroring the organization of `src/` to maintain clarity between declaration and implementation files.

```bash
include/
├── utils.h
└── module.h
```

## Libraries (`libs/`)

Holds third-party or custom libraries used by the project, promoting reusability and separation of external code from your main codebase. Libraries may be stored in `libs/`, and often include their own set of headers and source files. Subfolders are used if there are multiple libraries.

### Types of Libraries

- **Static Libraries** (`.a`, `.lib`): Linked at compile time and produce a larger executable file.
- **Dynamic Libraries** (`.so`, `.dll`): Linked at runtime, allowing shared use across programs.

```bash
libs/
├── my_library/
│   ├── my_library.h
│   ├── my_library.cpp
│   └── libmy_library.so
└── another_library/
    ├── another_library.h
    ├── another_library.cpp
    └── libanother_library.a
```

## Build Files (`build/` or `bin/`)

Stores compiled output, object files (`.o`), and executables, keeping the main codebase clean from temporary or build-specific files. This folder is typically empty in the source repository and populated by the build process.

- **`build/`**: Stores intermediate files and executables created during the build.
- **`bin/`**: Often used specifically for compiled executable files if separate from intermediate files.
- **Tool Integration**: The `build/` folder is often specified in build tools like **CMake** or **Makefiles** to define where output should be directed.

```bash
build/
├── main.o
├── utils.o
└── project_executable
```

## Typical Project Directory Structure

Here's a sample layout for a larger C++ project that brings together these organizational principles:

```bash
my_cpp_project/
├── src/                   # Source files with main application logic
│   ├── main.cpp
│   ├── utils.cpp
│   └── module.cpp
├── include/               # Header files
│   ├── utils.h
│   └── module.h
├── libs/                  # External libraries
│   └── my_library/
│       ├── my_library.h
│       ├── my_library.cpp
│       └── libmy_library.so
├── build/                 # Build output (object files, binaries)
│   ├── main.o
│   ├── utils.o
│   └── my_project_executable
├── CMakeLists.txt         # Build configuration for CMake
└── README.md              # Project documentation
```

### Additional Tips for File Organization

- **Use Include Guards**: Ensure header files have include guards (`#ifndef`, `#define`, `#endif`) to prevent multiple inclusions.
- **Group Related Code**: Group files by modules or functionality to simplify navigation and dependency management.
- **Consider Separate Folders for Tests**: If the project includes unit tests, you may want to add a `tests/` folder containing test source and header files.
