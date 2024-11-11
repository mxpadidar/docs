# Statements and Flow Control

## if and if-else Statements

```cpp
if (condition) { code; }

if (condition) { code; } else { code; }

if (condition1) { code; } else if (condition2) { code; } else { code; }
```

## Conditional Operator (Ternary Operator)

```cpp
// if condition is true, result = true_value, else result = false_value
int result = (condition) ? true_value : false_value;
```

## switch Statement

```cpp
switch (expression) {
    case constant1: code; break;
    case constant2: code; break;
    default: code;
}
```

## while and do-while Loops

```cpp
while (condition) { code; }

do { code; } while (condition);
```

## for Loop

```cpp
for (initialization; condition; update) { code; }
```

## Range-based for Loop

```cpp
for (type var : iterable) { code; }

// Example

int[] arr = {1, 2, 3};

for (int i : arr) { code; } // i takes on values 1, 2, 3
```

## Jump statements

**break**: Exits the loop or switch statement.

**continue**: Skips the current iteration of a loop.

**goto**: Transfers control to a labeled statement.

```cpp

// somewhere in the code
label: code;

for (initialization; condition; update) {
    if (condition) { break; } // Exit loop
    if (condition) { continue; } // Skip to next iteration
    if (condition) { goto label; } // Jump to label
}
```
