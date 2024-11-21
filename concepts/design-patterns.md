# Design Patterns in Software Development

Design patterns are reusable solutions to common problems in software design. They provide templates to structure your code effectively and make it easier to maintain and extend.

---

## Categories of Design Patterns

1. **Creational Patterns**: Deal with object creation mechanisms.

   - Factory Method
   - Abstract Factory
   - Singleton
   - Builder
   - Prototype

2. **Structural Patterns**: Focus on the composition of classes and objects.

   - Adapter
   - Bridge
   - Composite
   - Decorator
   - Facade
   - Flyweight
   - Proxy

3. **Behavioral Patterns**: Concerned with object collaboration and responsibility.
   - Chain of Responsibility
   - Command
   - Interpreter
   - Iterator
   - Mediator
   - Memento
   - Observer
   - State
   - Strategy
   - Template Method
   - Visitor

---

## 1. Creational Patterns

### **Factory Method**

**Intent**: Create objects without specifying their exact class.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Drawing a Circle")

class Square(Shape):
    def draw(self):
        print("Drawing a Square")

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            raise ValueError("Unknown shape type")

shape = ShapeFactory.create_shape("circle")
shape.draw()
```

---

### **Singleton**

**Intent**: Ensure a class has only one instance.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

singleton1 = Singleton()
singleton2 = Singleton()

print(singleton1 is singleton2)  # True
```

---

## 2. Structural Patterns

### **Adapter**

**Intent**: Allow incompatible interfaces to work together.

```python
class EuropeanPlug:
    def plug_in(self):
        print("European plug connected")

class USPlug:
    def connect(self):
        print("US plug connected")

class Adapter:
    def __init__(self, european_plug):
        self.european_plug = european_plug

    def connect(self):
        self.european_plug.plug_in()

european_plug = EuropeanPlug()
adapter = Adapter(european_plug)
adapter.connect()
```

---

### **Decorator**

**Intent**: Add new functionality to an object dynamically.

```python
class Coffee:
    def cost(self):
        return 5

    def description(self):
        return "Coffee"

class MilkDecorator:
    def __init__(self, coffee):
        self.coffee = coffee

    def cost(self):
        return self.coffee.cost() + 2

    def description(self):
        return self.coffee.description() + " with milk"

coffee = Coffee()
milk_coffee = MilkDecorator(coffee)

print(milk_coffee.description())  # Coffee with milk
print(milk_coffee.cost())         # 7
```

---

## 3. Behavioral Patterns

### **Observer**

**Intent**: Notify dependent objects when the state of an object changes.

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class ConcreteSubject(Subject):
    def __init__(self):
        super().__init__()
        self._state = None

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        self.notify()

class Observer:
    def update(self, subject):
        pass

class ConcreteObserver(Observer):
    def update(self, subject):
        print(f"Observer: Reacting to state {subject.get_state()}")

subject = ConcreteSubject()
observer = ConcreteObserver()

subject.attach(observer)
subject.set_state("New State")  # Observer: Reacting to state New State
```

---

### **Strategy**

**Intent**: Define a family of algorithms and make them interchangeable.

```python
class Strategy:
    def execute(self, a, b):
        pass

class AddStrategy(Strategy):
    def execute(self, a, b):
        return a + b

class MultiplyStrategy(Strategy):
    def execute(self, a, b):
        return a * b

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, a, b):
        return self.strategy.execute(a, b)

context = Context(AddStrategy())
print(context.execute_strategy(3, 4))  # 7

context.set_strategy(MultiplyStrategy())
print(context.execute_strategy(3, 4))  # 12
```

---

### Summary of Design Patterns

| **Category**   | **Pattern**    | **Purpose**                                        |
| -------------- | -------------- | -------------------------------------------------- |
| **Creational** | Factory Method | Create objects without specifying the exact class. |
|                | Singleton      | Ensure a class has only one instance.              |
| **Structural** | Adapter        | Allow incompatible interfaces to work together.    |
|                | Decorator      | Add functionality to an object dynamically.        |
| **Behavioral** | Observer       | Notify objects when the state changes.             |
|                | Strategy       | Define and switch between algorithms at runtime.   |

For more advanced patterns, feel free to ask!
