# ⏳ Time & Space Complexity (Data Structures & Algorithms)

## 1\. Core Concept: Why Analyze Complexity?

Complexity analysis is a theoretical measure of how the **resource consumption** of an algorithm scales with the size of its input.

- **Time Complexity:** Measures the amount of **time** (number of elementary operations) an algorithm takes to complete.
- **Space Complexity:** Measures the amount of **memory** (temporary space) an algorithm needs to run to completion.

> **Goal:** The analysis ignores machine-specific factors (CPU speed, memory size) and focuses on the **growth rate** of operations relative to the input size, $n$.

---

## 2\. Asymptotic Notation (Big O)

We use **Asymptotic Notations** to describe the _upper bound_ (worst-case scenario) of an algorithm's performance. The most common notation is **Big O Notation**.

The Big O Notation (O) describes the **worst-case** performance of an algorithm as the input size (n) grows.

When calculating complexity, we focus on the **dominant term** (the term that grows fastest).

$$
\text{Example: } O(2n^2 + 5n + 10) \text{ simplifies to } O(n^2)
$$

- **$O(1)$ — Constant Time**
  - **Description:** The execution time is **constant**, meaning it does not change regardless of the input size $n$.
  - **Example:** Accessing an array element by its index.

- **$O(\log n)$ — Logarithmic Time**
  - **Description:** Time grows **very slowly** as n increases. This is typical when the algorithm cuts the problem space in half on each step.
  - **Example:** **Binary Search**.

- **$O(n)$ — Linear Time**
  - **Description:** Time grows **proportionally** to the input size $n$. If n doubles, the time roughly doubles.
  - **Example:** A simple loop that iterates over all elements of an array.

- **$O(n \log n)$ — Linearithmic Time**
  - **Description:** Time grows slightly faster than linear ($O(n)$). This is the **standard for efficient, comparison-based sorting** algorithms.
  - **Example:** **Merge Sort** and **Heap Sort**.

- **$O(n^2)$ — Quadratic Time**
  - **Description:** Time grows as the **square** of the input size $n$. This usually happens when you have nested loops that both iterate over the full input.
  - **Example:** **Bubble Sort** or comparing every pair of elements in a list.

- **$O(2^n)$ — Exponential Time**
  - **Description:** Time **doubles** with every single element added. This is **highly inefficient** and only practical for very small input sizes.
  - **Example:** Solving the Traveling Salesperson Problem using a brute-force approach.

---

## 3\. Calculating Complexity in Python Code

### A. Time Complexity

1.  **$O(1)$ Constant Time**

    ```python
    def get_first_item(arr):
        return arr[0]  # Accesses one element, regardless of arr size
    ```

2.  **$O(n)$ Linear Time**

    ```python
    def print_all(arr):
        for item in arr: # Loop runs n times
            print(item)
    ```

3.  **$O(n^2)$ Quadratic Time**

    ```python
    def print_pairs(arr):
        for i in arr:
            for j in arr: # Nested loop: n * n operations
                print(i, j)
    ```

4.  **$O(\log n)$ Logarithmic Time (Binary Search Example)**

    ```python
    def binary_search(arr, target):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1 # Problem space is halved
            else:
                high = mid - 1 # Problem space is halved
        return -1
    ```

    - The problem space is cut in half in each iteration, leading to $O(\log n)$.

### B. Space Complexity

Space complexity focuses on **auxiliary space**—the extra temporary memory used by the algorithm, not the space taken by the input itself.

1.  **$O(1)$ Constant Space**

    ```python
    def sum_array(arr):
        total = 0 # 'total' takes a constant amount of memory
        for num in arr:
            total += num
        return total
    ```

2.  **$O(n)$ Linear Space**

    ```python
    def create_copy(arr):
        new_arr = [] # Creates a new array whose size is proportional to the input size n
        for item in arr:
            new_arr.append(item)
        return new_arr
    ```
