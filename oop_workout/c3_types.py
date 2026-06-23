
from c1_vehicle import Vehicle
from c2_tank import FuelTank

class FuelledVehicle(Vehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, capacity: float, consumption: float) -> None:
        
        super().__init__(plate, make, model, year)
        self.tank: FuelTank = FuelTank(capacity)
        self.consumption: float = consumption  # Litres per 100km

    def refuel(self, litres: float) -> None:

        self.tank.fill(litres)

    def drive(self, km: int) -> float:

        fuel_needed = (km / 100.0) * self.consumption
        self.tank.consume(fuel_needed)
        super().drive(km)
        return fuel_needed

    def range_remaining(self) -> float:

        if self.consumption == 0:
            return 0.0
        return (self.tank.get_level() / self.consumption) * 100.0


class Car(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, seats: int = 5) -> None:
        super().__init__(plate, make, model, year, capacity=50.0, consumption=6.0)
        self.seats: int = seats

    def describe(self) -> str:
        return f"{super().describe()}, car, {self.seats} seats"


class Truck(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, payload_kg: int) -> None:
        super().__init__(plate, make, model, year, capacity=200.0, consumption=18.0)
        self.payload_kg: int = payload_kg

    def describe(self) -> str:
        return f"{super().describe()}, truck, {self.payload_kg} kg payload"


class Motorcycle(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int) -> None:
        super().__init__(plate, make, model, year, capacity=15.0, consumption=3.5)

    def describe(self) -> str:
        return f"{super().describe()}, motorcycle"


class Van(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, volume_m3: float) -> None:
        super().__init__(plate, make, model, year, capacity=75.0, consumption=9.0)
        self.volume_m3: float = volume_m3

    def describe(self) -> str:
        return f"{super().describe()}, van, {self.volume_m3} m3 volume"