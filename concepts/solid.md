# SOLID Principles in Python

The SOLID principles are a set of five design guidelines aimed at improving the maintainability, scalability, and flexibility of software systems. These principles help in creating clean and efficient code.

## 1. **Single Responsibility Principle (SRP)**

- **Definition**: A class should have only one reason to change. This means a class should have one responsibility or function.

**Bad Example**: A class handling both file operations and data parsing.

```python
class FileManager:
    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def parse_data(self, data):
        return data.split("\n")  # Parsing logic
```

**Improved Example**: Separate responsibilities into different classes.

```python
class FileManager:
    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

class DataParser:
    def parse_data(self, data):
        return data.split("\n")  # Parsing logic
```

## 2. **Open/Closed Principle (OCP)**

- **Definition**: Classes should be open for extension but closed for modification. New functionality should be added by extending the code, not altering existing code.

**Bad Example**: Modifying a class to add new functionality.

```python
class PaymentProcessor:
    def process_payment(self, payment_type):
        if payment_type == "credit_card":
            print("Processing credit card payment")
        elif payment_type == "paypal":
            print("Processing PayPal payment")
```

**Improved Example**: Use polymorphism to add new payment types without modifying the existing class.

```python
class PaymentProcessor:
    def process_payment(self):
        pass

class CreditCardPayment(PaymentProcessor):
    def process_payment(self):
        print("Processing credit card payment")

class PayPalPayment(PaymentProcessor):
    def process_payment(self):
        print("Processing PayPal payment")
```

## 3. **Liskov Substitution Principle (LSP)**

- **Definition**: Objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program.

**Bad Example**: Violating LSP by changing behavior in a subclass.

```python
class Bird:
    def fly(self):
        print("Bird is flying")

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly")
```

**Improved Example**: Use a proper hierarchy to avoid misuse.

```python
class Bird:
    pass

class FlyingBird(Bird):
    def fly(self):
        print("Bird is flying")

class Penguin(Bird):
    def swim(self):
        print("Penguin is swimming")
```

## 4. **Interface Segregation Principle (ISP)**

- **Definition**: A class should not be forced to implement methods it does not use. Instead, create smaller, more specific interfaces.

**Bad Example**: A class forced to implement unnecessary methods.

```python
class Machine:
    def print(self):
        pass

    def scan(self):
        pass

    def fax(self):
        pass

class Printer(Machine):
    def print(self):
        print("Printing document")

    def scan(self):
        raise NotImplementedError("Scanner not available")

    def fax(self):
        raise NotImplementedError("Fax not available")
```

**Improved Example**: Split interfaces into specific responsibilities.

```python
class PrinterInterface:
    def print(self):
        pass

class ScannerInterface:
    def scan(self):
        pass

class Printer(PrinterInterface):
    def print(self):
        print("Printing document")
```

## 5. **Dependency Inversion Principle (DIP)**

- **Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions.

**Bad Example**: High-level class depending on a low-level class.

```python
class MySQLDatabase:
    def connect(self):
        print("Connecting to MySQL database")

class DataHandler:
    def __init__(self):
        self.db = MySQLDatabase()

    def fetch_data(self):
        self.db.connect()
```

**Improved Example**: Depend on abstractions.

```python
class Database:
    def connect(self):
        pass

class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL database")

class DataHandler:
    def __init__(self, db: Database):
        self.db = db

    def fetch_data(self):
        self.db.connect()

db = MySQLDatabase()
handler = DataHandler(db)
handler.fetch_data()
```

### Summary of SOLID Principles

| Principle                 | Key Idea                                             |
| ------------------------- | ---------------------------------------------------- |
| **Single Responsibility** | A class should have one reason to change.            |
| **Open/Closed**           | Extend behavior without modifying existing code.     |
| **Liskov Substitution**   | Subtypes must be substitutable for their supertypes. |
| **Interface Segregation** | Prefer small, specific interfaces.                   |
| **Dependency Inversion**  | Depend on abstractions, not concretions.             |
