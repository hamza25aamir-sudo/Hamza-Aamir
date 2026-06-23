
from c1_vehicle import Vehicle
from c3_types import FuelledVehicle

class ElectricCar(Vehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, battery_kwh: float, range_km: float) -> None:

        super().__init__(plate, make, model, year)
        self._battery_kwh: float = battery_kwh
        self._range_km: float = range_km
        self._charge: float = 0.0

    def get_charge(self) -> float:
       
        return self._charge

    def charge(self, kwh: float) -> None:
        
        if kwh <= 0:
            raise ValueError("Charge amount must be positive.")
        if self._charge + kwh > self._battery_kwh:
            raise ValueError("Battery capacity exceeded.")
        self._charge += kwh

    def drive(self, km: int) -> float:
        
        if self._range_km == 0:
            raise ValueError("Invalid configuration: range cannot be zero.")
        kwh_needed = self._battery_kwh * (km / self._range_km)
        
        if self._charge - kwh_needed < 0:
            raise ValueError("Insufficient battery charge.")
            
        self._charge -= kwh_needed
        super().drive(km)
        return kwh_needed

    def describe(self) -> str:
        return f"{super().describe()}, electric car"


class HybridCar(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, capacity: float, consumption: float, battery_kwh: float, range_km: float) -> None:
        
        super().__init__(plate, make, model, year, capacity, consumption)
        self._battery_kwh: float = battery_kwh
        self._range_km: float = range_km
        self._charge: float = 0.0

    def get_charge(self) -> float:
        return self._charge

    def charge(self, kwh: float) -> None:
        if kwh <= 0:
            raise ValueError("Charge amount must be positive.")
        if self._charge + kwh > self._battery_kwh:
            raise ValueError("Battery capacity exceeded.")
        self._charge += kwh

    def drive(self, km: int) -> float:
        
        if self._range_km == 0:
            raise ValueError("Invalid configuration: range cannot be zero.")
            
        max_electric_km = (self._charge / self._battery_kwh) * self._range_km
        
        if max_electric_km >= km:
            
            kwh_used = self._battery_kwh * (km / self._range_km)
            self._charge -= kwh_used
            Vehicle.drive(self, km)
            return kwh_used
        else:
           
            electric_share_km = int(max_electric_km)
            combustion_share_km = km - electric_share_km
            
            fuel_needed = (combustion_share_km / 100.0) * self.consumption
            
            
            if self.tank.get_level() < fuel_needed:
                raise ValueError("Insufficient hybrid storage across both components.")
                
            kwh_used = self._charge
            self._charge = 0.0
            self.tank.consume(fuel_needed)
            Vehicle.drive(self, km)
            return kwh_used + fuel_needed


def drive_all(vehicles: list[Vehicle], km: int) -> list[float]:

    return [v.drive(km) for v in vehicles]