# OOP Fleet Management System

This project is a vehicle fleet management system written in Python to practice Object-Oriented Programming (OOP).

## Challenges Completed

I completed all 6 challenges and their stretch goals:
- **Challenge 1 (`cl_vehicle.py`)**: Created the base Vehicle class to track plates, make, model, and year.
- **Challenge 2 (`c2_tank.py`)**: Built a FuelTank class with strict rules to prevent fuel overflow or empty tank errors.
- **Challenge 3 (`c3_types.py`)**: Added specific vehicle types like Car, Truck, Motorcycle, and Van using inheritance.
- **Challenge 4 (`c4_electric.py`)**: Added an ElectricCar class and a HybridCar class that uses both electric power and gas.
- **Challenge 5 (`c5_dunders.py`)**: Added magic methods (`__str__`, `__repr__`, `__eq__`, `__lt__`) so vehicles can be printed, compared, and sorted easily.
- **Challenge 6 (`c6_fleet.py`)**: Created a Fleet manager class to add, remove, search, save, and load vehicles using JSON files.


## Difficulties Encountered & Solutions

1. **Circular Import Error (`ImportError`)**
   - *Problem*: The code crashed saying it could not import `FuelTank` inside `c2_tank.py`.
   - *Solution*: I realized `c2_tank.py` was accidentally trying to import from itself. Removing that line fixed the problem.

2. **Constructor Argument Error (`TypeError`)**
   - *Problem*: Python threw an error saying `Vehicle.__init__() missing 1 required positional argument: 'kilometres'`.
   - *Solution*: I accidentally included `kilometres` in the setup parameters. I removed it from the brackets and set `self.kilometres = 0` inside the function instead.

3. **Subclass Names in `__repr__`**
   - *Problem*: I wanted the `__repr__` method to print the exact type of vehicle (like `Truck` or `Car`) without writing separate code for every single class.
   - *Solution*: I used `type(self).__name__` in the base class, which automatically finds and prints the correct type for every vehicle.