class FuelTank:
    def __init__(self, capacity: float) -> None:
        if capacity <= 0:
            raise ValueError("Tank capacity must be positive.")
        self._capacity: float = capacity
        self._level: float = 0.0

    def get_level(self) -> float:
        return round(self._level, 2)

    def get_capacity(self) -> float:
        return self._capacity

    def fill(self, litres: float) -> None:
        if litres <= 0:
            raise ValueError("Litres to fill must be positive.")
        if self._level + litres > self._capacity:
            raise ValueError("Tank overflow error.")
        self._level += litres

    def consume(self, litres: float) -> None:
        if litres <= 0:
            raise ValueError("Litres to consume must be positive.")
        if self._level - litres < 0:
            raise ValueError("Not enough fuel in the tank.")
        self._level -= litres

    def fill_to_full(self) -> float:
        added = self._capacity - self._level
        self._level = self._capacity
        return added

    def percent_full(self) -> float:
        if self._capacity == 0:
            return 0.0
        return round((self._level / self._capacity) * 100, 1)

t = FuelTank(30.0)
t.fill(30)
print(t.get_level())