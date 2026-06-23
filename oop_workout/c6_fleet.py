from c3_types import Car, Truck, Motorcycle
from c4_electric import ElectricCar
import c5_dunders


class Fleet:
    def __init__(self, name: str) -> None:
        self.name = name
        self._vehicles = []   #creating list

    def add(self, vehicle) -> None:
        if vehicle.plate in self._vehicles:
            raise ValueError("vehicle already exists.")

        self._vehicles.append(vehicle)

    def remove(self, plate) -> None:
        for vehicle in self._vehicles:
            if vehicle.plate == plate:
                self._vehicles.remove(vehicle)
                return

        raise KeyError("vehicle not found.")

    def find(self, plate):
        return self._vehicles.get(plate)
   

    def total_kilometres(self) -> int:
        return sum(vehicle.kilometres for vehicle in self._vehicles)

    def drive_all(self, km: int) -> tuple[list, list]:
    
        successes = []
        failures = []

        for vehicle in self._vehicles:
            try:
                vehicle.drive(km)
                successes.append(vehicle.plate)
            except Exception as error:
                failures.append((vehicle.plate, str(error)))

        return successes, failures

    def __len__(self) -> int:
        return len(self._vehicles)

    def __iter__(self):
        return iter(self._vehicles)

    def __contains__(self, plate: str) -> bool:
        return any(vehicle.plate == plate for vehicle in self._vehicles)

    def __str__(self) -> str:
        return f"Fleet '{self.name}': {len(self)} vehicle(s)"


def print_summary(fleet: Fleet) -> None: 
    print("*** FLEET REPORT ***")
    print(fleet)
    print(f"Total kilometres: {fleet.total_kilometres()}")
    print("--------------------")

    for vehicle in fleet:
        print(vehicle)

    print("=" * 20)