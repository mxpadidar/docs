# Object-Oriented Programming in Python

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects." Objects are instances of classes that encapsulate data and behaviors, making code reusable, scalable, and organized.

## Key Concepts

### **1. Classes and Objects**

- **Class**: A blueprint for creating objects, defining shared attributes and behaviors.
- **Object**: An instance of a class, containing unique data while adhering to the class's structure.

```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def display_info(self):
        print(f"{self.brand} {self.model}")

# Creating an object
my_car = Car("Toyota", "Corolla")
my_car.display_info()  # Output: Toyota Corolla
```

### **2. Encapsulation**

Encapsulation bundles data and methods within a class and restricts direct access to certain components, ensuring controlled interaction.

#### **Access Modifiers**

- **Public**: Accessible from anywhere.
- **Protected** (`_`): Accessible within the class and subclasses.
- **Private** (`__`): Accessible only within the class.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner      # Public attribute
        self._balance = balance # Protected attribute

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance

# Accessing attributes and methods
account = BankAccount("Alice", 1000)
print(account.owner)  # Output: Alice
print(account.get_balance())  # Output: 1000
```

### **3. Inheritance**

Inheritance enables a class (subclass) to derive properties and behaviors from another class (superclass).

#### **Types of Inheritance**

- **Single Inheritance**: One subclass inherits from one superclass.
- **Multiple Inheritance**: One subclass inherits from multiple superclasses.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

# Using Inheritance
dog = Dog("Buddy")
print(dog.name)  # Output: Buddy
dog.speak()      # Output: Dog barks
```

### **4. Polymorphism**

Polymorphism allows objects of different classes to be treated uniformly, enabling flexible and reusable code.

#### **Example**

```python
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

class Cat(Animal):
    def speak(self):
        print("Cat meows")

# Demonstrating polymorphism
animals = [Dog(), Cat()]
for animal in animals:
    animal.speak()
```

### **5. Abstraction**

Abstraction hides implementation details and exposes only essential features, reducing complexity.

#### **Abstract Classes and Methods**

- **Abstract Class**: Cannot be instantiated and serves as a base for other classes.
- **Abstract Method**: Declared but not implemented in the abstract class.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

circle = Circle(5)
print(circle.area())  # Output: 78.5
```

### **6. Association, Aggregation, and Composition**

#### **Association**: A relationship between two independent classes

#### **Aggregation**: A "has-a" relationship where the parent can exist independently of its child

#### **Composition**: A "contains-a" relationship where the child depends entirely on the parent

s

```python
# Association
class Driver:
    def __init__(self, name):
        self.name = name

class Car:
    def __init__(self, brand, driver):
        self.brand = brand
        self.driver = driver

driver = Driver("Alice")
car = Car("Toyota", driver)

# Aggregation
class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members

# Composition
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

class Car:
    def __init__(self, engine):
        self.engine = engine

engine = Engine(200)
car = Car(engine)
```

### **7. Overloading and Overriding**

#### **Overloading**: Methods with the same name but different arguments. Python supports it using default arguments

#### **Overriding**: Subclasses redefine a superclass method to provide specific behavior

```python
class Calculator:
    def add(self, a, b=0):
        return a + b

calc = Calculator()
print(calc.add(2))       # Output: 2
print(calc.add(2, 3))    # Output: 5
```

### **8. Design Patterns**

Design patterns are reusable solutions for common problems. Examples include:

- **Singleton**: Ensures only one instance of a class exists.
- **Factory**: Creates objects without exposing instantiation logic.
- **Observer**: Implements a subscription mechanism for object changes.

### **9. SOLID Principles**

- **S**: Single Responsibility Principle (SRP): Each class has one purpose.
- **O**: Open/Closed Principle (OCP): Classes are open for extension but closed for modification.
- **L**: Liskov Substitution Principle (LSP): Subclasses can replace their parent classes.
- **I**: Interface Segregation Principle (ISP): No class should depend on methods it doesn't use.
- **D**: Dependency Inversion Principle (DIP): High-level modules should not depend on low-level modules.
