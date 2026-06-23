from c1_vehicle import Vehicle

def vehicle_str(self: Vehicle) -> str:
    return self.describe()

def vehicle_repr(self: Vehicle) -> str:
    return f"{type(self).__name__}('{self.plate}', '{self.make}', '{self.model}', {self.year})"

def vehicle_eq(self: Vehicle, other: object) -> bool:
    if not isinstance(other, Vehicle):
        return NotImplemented
    return self.plate == other.plate

def vehicle_hash(self: Vehicle) -> int:
    return hash(self.plate)

def vehicle_lt(self: Vehicle, other: Vehicle) -> bool:
    if not isinstance(other, Vehicle):
        return NotImplemented
    return self.plate < other.plate

Vehicle.__str__ = vehicle_str
Vehicle.__repr__ = vehicle_repr
Vehicle.__eq__ = vehicle_eq
Vehicle.__hash__ = vehicle_hash
Vehicle.__lt__ = vehicle_lt