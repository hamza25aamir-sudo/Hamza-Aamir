class Vehicle:
    fleet_size = 0
    def __init__(self, plate, make, model, year):
        self.plate = plate
        self.make = make
        self.model = model 
        self.year = year
        self.kilometers = 0 

        Vehicle.fleet_size += 1
        
        pass
    def drive(self, km: int) -> None:
        if km <= 0:
            raise ValueError("driving distance should be greater than zero.")
        self.kilometers += km
   
    def describe(self) -> str:
        return f"{self.year} {self.make} {self.model} ({self.plate})"
    
    def service_due(self) -> bool:
        return self.kilometers > 15000

v= Vehicle("B-AB-1234", "Volkswagen", "Golf", 2022)
v.drive(50)
print(v.describe())
print(v.kilometers)