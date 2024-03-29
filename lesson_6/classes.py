from enum import Enum


class Garage:
    '''
    This class represents a Garage. The garage
    is able to replace the tires of Vehicles but
    can only do this if it is supplied with tires.
    '''

    def __init__(self):
        '''
        Creates a new Garage with an empty stock.
        '''
        self._stock = []

    def add_tire(self, tire):
        '''
        Add a tire to the stock. The garage will accept
        used tires but not tires which are to worn out.
        '''
        if tire.needs_replacement():
            raise RuntimeError("This tire is already too worn out")
        else:
            self._stock.append(tire)

    def service_vehicle(self, vehicle):
        '''
        Replace any tires which need to be replaced.
        This function will return the number of
        tires which where actually replaced.
        '''
        tires_replaced = 0

        while vehicle.has_worn_tires():
            new_tire = self._stock.pop()
            vehicle.replace_tire(new_tire)
            tires_replaced = tires_replaced + 1
        return tires_replaced


class FuelType(Enum):
    '''
    The enum represents the different types
    of fuel a vehicle can have.
    '''
    PETROL = 1
    DIESEL = 2


class FuelStation:
    '''
    This class represents a Fuel Station.
    It can fill the fuel tank of any
    vehicle.
    '''

    def __init__(self):
        '''
        Creates a new FuelStation with an empty fuel supply.
        '''
        self._fuel = {}

    def has_fuel(self, fuel_type):
        '''
        Indicates if this station has any fuel of the
        given fuel type.
        '''
        return fuel_type in self._fuel

    def _retrieve(self, fuel_type, amount):
        '''
        Retrieve a certain amount of fuel from
        this station. This function should
        only be used by functions who are part of
        this class.
        '''
        if self.has_fuel(fuel_type):
            amount_stored = self._fuel[fuel_type]
            if amount_stored - amount < 0:
                raise RuntimeError("Not enough fuel in station")
            else:
                self._fuel[fuel_type] = amount_stored - amount
        else:
            raise RuntimeError("No fuel of this type")

    def add_fuel(self, fuel_type, amount):
        '''
        Add a certain amount of fuel to this station.
        '''
        if amount <= 0:
            raise ValueError("You can only add fuel and not take it")

        stored_amount = self._fuel.get(fuel_type, 0)
        self._fuel[fuel_type] = stored_amount + amount

    def fill_tank(self, fuel_type, vehicle):
        '''
        Fill the tank of the given vehicle with the given type of fuel.
        '''
        if vehicle.needs_fuel():
            fuel_needed = vehicle.amount_needed()
            self._retrieve(fuel_type, fuel_needed)
            vehicle.add_fuel(fuel_type, fuel_needed)
        else:
            raise RuntimeError("This vehicle has a full tank")


class Door:
    '''
    The class represents a door which can be closed of opened.
    '''

    def __init__(self):
        '''
        Create a new door which is closed by default.
        '''
        self._is_closed = True

    def open(self):
        '''
        Open the door.
        '''
        if self.is_closed():
            self._is_closed = False
        else:
            raise RuntimeError("Door is already open")

    def is_open(self):
        '''
        Indicates whenever the door is open.
        '''
        return not self._is_closed

    def close(self):
        '''
        Close the door.
        '''
        if self.is_open():
            self._is_closed = True
        else:
            raise RuntimeError("Door is already closed")

    def is_closed(self):
        '''
        Indicates whenever the door is closed.
        '''
        return self._is_closed


class Tire:
    '''
    This class represents a vehicle tire.
    '''

    def __init__(self, wear_level=46000):
        '''
        Create a new tire. You can optionally
        configure a wear level.
        '''
        if wear_level <= 0:
            raise ValueError("Wear level must be a positive value")
        self._wear_level = wear_level

    def distance_before_worn(self):
        '''
        Returns the distance which this
        tire can travel before it is totally
        worn out.
        '''
        return self._wear_level

    def needs_replacement(self):
        '''
        Indicates if this tire need to be
        replaced. A tire needs to be
        replaced when it's wear level is
        lower than 500.
        '''
        return self._wear_level < 500

    def will_be_worn_out(self, distance):
        '''
        Indicates whenever this tire will be worn out
        after traveling the given amount of distance.
        '''
        return self._wear_level - distance < 0

    def register_wear(self, distance):
        '''
        Register wear on this tire. The given distance
        will be subtracted from the wear level.
        '''
        if distance < 0:
            raise ValueError("Your can't travel negative distances")
        elif self.will_be_worn_out(distance):
            raise RuntimeError("Tire blown!")
        else:
            self._wear_level = self._wear_level - distance


class Engine:
    '''
    Represents an engine which can be
    placed into a vehicle.
    '''

    def __init__(self, fuel_type, capacity):
        '''
        Creates a new engine with a
        certain fuel type and maximum
        fuel capacity. The engine
        starts of with an empty tank so
        you will have to add fuel to it
        to make it work.
        '''
        if capacity < 1:
            raise ValueError(
                "You can't create an engine with zero or negative fuel capacity")

        self.fuel_type = fuel_type
        self._fuel_amount = 0
        self._fuel_capacity = capacity

    def add_fuel(self, type, amount):
        '''
        Add certain amount of the given
        fuel type to the engine. The function will
        raise a RuntimeError when you either add the
        wrong type or too much fuel.
        '''
        if type is not self.fuel_type:
            raise RuntimeError("This engine does not take this type of fuel")
        elif amount <= 0:
            raise ValueError("You cannot remove fuel from the engine")
        elif (amount + self._fuel_amount) > self._fuel_capacity:
            raise RuntimeError("This engine cannot hold this amount of fuel")
        else:
            self._fuel_amount = self._fuel_amount + amount

    def amount_needed(self):
        '''
        Return the amount of fuel needed to
        fill the fuel tank to its maximum capacity.
        '''
        return self._fuel_capacity - self._fuel_amount

    def can_drive(self, distance):
        '''
        Indicates if the engine has enough
        fuel to drive the given distance.
        '''
        return self._fuel_amount - distance > 0

    def drive(self, distance):
        '''
        Drive the given distance. Raises a
        RuntimeError when the engine doesn't
        have enough fuel to drive the given
        distance. The function will also raise
        a ValueError if you supply it with a negative
        distance.
        '''
        if distance < 0:
            raise ValueError("You can't drive a negative distance")
        elif self.can_drive(distance):
            self._fuel_amount = self._fuel_amount - distance
        else:
            raise RuntimeError("Not enough fuel to drive this distance")


class Vehicle:
    '''
    Represents a Vehicle which has an
    engine and tires. It needs fuel to
    drive.
    '''

    def __init__(self, tire_count, fuel_type, fuel_cap):
        '''
        Creates a new Vehicle. A vehicle
        needs to have a minimum of one tire.
        It also runs on a certain fuel type
        and maximum fuel capacity.
        '''
        self._engine = Engine(fuel_type, fuel_cap)
        self._tires = []

        if tire_count < 1:
            raise ValueError("A Vehicle must at least have 1 tire")

        for count in range(tire_count):
            self._tires.append(Tire())

    def has_worn_tires(self):
        '''
        Checks if any of the tires on this
        vehicle is worn out and needs to be
        replaced.
        '''
        for tire in self._tires:
            if tire.needs_replacement():
                return True
        return False

    def repace_tire(self, new_tire):
        '''
        Replaces one of the worn out tires
        with the newly supplied tire. The
        function will raise a RuntimeError if
        none of the tires are worn out.
        '''
        tire_index = 0
        # We use a while loop here since we are
        # making changes to the collection we are
        # iterating over. For loops don't like this.
        while tire_index < len(self._tires):
            if self._tires[tire_index].needs_replacement():
                self._tires[tire_index] = new_tire
                return
            tire_index = tire_index + 1
        raise RuntimeError("Found no tire which need replacement")

    def get_fuel_type(self):
        '''
        Returns the fuel type of the engine.
        '''
        return self._engine.fuel_type

    def add_fuel(self, type, amount):
        '''
        Add fuel to the engine of this vehicle.
        '''
        self._engine.add_fuel(type, amount)

    def needs_fuel(self):
        '''
        Check if this vehicle needs fuel in
        order to drive.
        '''
        return self._engine.amount_needed() > 0

    def amount_needed(self):
        '''
        Tells you how much fuel this
        vehicle needs to completely
        fill up the tank.
        '''
        return self._engine.amount_needed()

    def drive(self, distance):
        '''
        Drive a certain distance. This
        function will raise a RuntimeError when
        the vehicle is not able to drive the given
        distance.
        '''
        if not self._engine.can_drive(distance):
            raise RuntimeError("Cannot drive this distance: not enough fuel")

        for tire in self._tires:
            if tire.will_be_worn_out(distance):
                raise RuntimeError(
                    "Cannot drive this distance: tire will blow out")

        self._engine.drive(distance)
        for tire in self._tires:
            tire.register_wear(distance)


class Car(Vehicle):
    '''
    Represents a Car which is a Vehicle.
    '''

    def __init__(
        self,
        fuel_type,
        fuel_cap,
        door_count
    ):
        '''
        Creates a new Car wit the given fuel type, fuel capacity
        and amount of doors.
        '''
        super().__init__(4, fuel_type, fuel_cap)  # Here we also initialize the Vehicle class.
        self._doors = []
        if door_count < 2:
            raise ValueError("A Car must at least have 2 doors")

        for count in range(door_count):
            self._doors.append(Door())

    def open_door(self, index):
        '''
        Open one of the car doors.
        '''
        self._doors[index].open()

    def close_door(self, index):
        '''
        Close one of the car doors.
        '''
        self._doors[index].close()

    def close_all_doors(self):
        '''
        Close all car doors.
        '''
        for door in self._doors:
            if door.is_open():
                door.close()

    def has_open_doors(self):
        '''
        Checks if any of the car doors
        are in an open position.
        '''
        for door in self._doors:
            if door.is_open():
                return True
        return False

    def drive(self, distance):
        '''
        Drive with the car. This function will
        raise a RuntimeError when the car is not able
        to drive for some reason.
        '''
        if self.has_open_doors():
            raise RuntimeError("Cannot drive with open doors")
        else:
            # We have overridden the drive function of the Vehicle
            # class by declaring a function with the same name in our
            # car class. We did this so we could check if any of the doors
            # where open before driving. We now call the drive function
            # of the Vehicle class so it will actually drive.
            super().drive(distance)


class Motorcycle(Vehicle):
    '''
    Represents a Motorcycle which is a type of Vehicle.
    '''

    def __init__(self, fuel_cap):
        '''
        Creates a new Motorcycle. With a given
        fuel capacity. All motorcycles run on
        petrol and have two tires.
        '''
        super().__init__(2, FuelType.PETROL, fuel_cap)

    def do_wheely(self):
        '''
        Do a wheely with the motorcycle.
        '''
        raise RuntimeError("The Motorcycle has crashed!")


def main():
    '''
    Main function. This is where the magic happens.
    '''
    station = FuelStation()
    station.add_fuel(FuelType.DIESEL, 100000)
    station.add_fuel(FuelType.PETROL, 100000)

    garage = Garage()
    for index in range(100):
        new_tire = Tire()
        garage.add_tire(new_tire)

    my_car = Car(FuelType.DIESEL, 800, 5)
    my_motor = Motorcycle(400)

    station.fill_tank(FuelType.DIESEL, my_car)
    print("I have filled the tank of my car. Ready to drive!")
    my_car.drive(355)
    print("I have driven a distance of 355 with my car")
    station.fill_tank(FuelType.PETROL, my_motor)
    print("I have filled the tank op my motorcycle. Ready to drive!")
    my_motor.drive(50)
    print("I have driven a distance of 50 with my motorcycle")
    try:
        station.fill_tank(FuelType.PETROL, my_car)
        print("I filled the tank of my car")
    except RuntimeError as error:
        print("Oops, I made a mistake: {}".format(error))

    print("I took my car to the garage for service")
    tires_replaced = garage.service_vehicle(my_car)
    print("They replaced {} of my tires".format(tires_replaced))


# We only want to execute the
# the main() function when the
# script is called directly.
if __name__ == "__main__":
    main()
