from abc import abstractmethod
from enum import Enum
import torch

from src.vehicles import VehicleTypes
from src.config import (INCOMING_DIRECTION,
                        OUTGOING_DIRECTION,
                        MOVEMENT_THRESHOLD)


class Direction(Enum):
    INCOMING = 1
    OUTGOING = 2


# Vehicle counting type abstract class: (state design pattern)
# Different counting types will have different ways of figuring out if a vehicle should be counted or not
class VehicleCountingType:

    def __init__(self):
        pass

    @abstractmethod
    def should_count(self, vehicle):
        pass


# Vehicles that are of this counting type have to pass a movement threshold to be counted
# Movement has to be either incoming or outgoing
class DirectionalMovingVehicleCounting(VehicleCountingType):

    def __init__(self, directions_to_count, incoming_direction, outgoing_direction, movement_threshold):
        super().__init__()
        self.directions_to_count = directions_to_count
        self.incoming_direction = incoming_direction
        self.outgoing_direction = outgoing_direction
        self.movement_threshold = movement_threshold

    # Calculate movement direction
    def calculate_movement_direction(self, vehicle):
        movement = (vehicle.last_pos - vehicle.first_pos)

        incoming_dot = torch.dot(movement, self.incoming_direction)
        outgoing_dot = torch.dot(movement, self.outgoing_direction)

        if incoming_dot > outgoing_dot:
            return Direction.INCOMING
        else:
            return Direction.OUTGOING

    # If the vehicle has moved beyond a certain threshold
    def has_moved(self, vehicle):
        movement = (vehicle.last_pos - vehicle.first_pos)
        movement_size = movement.norm()
        return movement_size >= self.movement_threshold

    def should_count(self, vehicle):
        # Calculate movement direction
        # Declare vehicle to be counted if it is in wanted direction and has moved
        direction = self.calculate_movement_direction(vehicle)
        has_moved = self.has_moved(vehicle)
        if direction in self.directions_to_count and has_moved:
            return True
        return False


class NotVehicleCounting(VehicleCountingType):

    def __init__(self):
        super().__init__()

    def should_count(self, vehicle):
        return False


class VehicleCountingFactory:

    def __init__(self):
        self.directional_moving_vehicle_types = [VehicleTypes.CAR, VehicleTypes.MOTORCYCLE,
                                                 VehicleTypes.BUS, VehicleTypes.TRUCK]
        self.directions_to_count = []
        self.incoming_direction = INCOMING_DIRECTION
        self.outgoing_direction = OUTGOING_DIRECTION
        self.movement_threshold = 0

    # Setting up configurations for the directional moving class part of the factory
    def set_directional_moving_counting_type(self, directions_to_count, incoming_direction=INCOMING_DIRECTION,
                                             outgoing_direction=OUTGOING_DIRECTION,
                                             movement_threshold=MOVEMENT_THRESHOLD):
        self.directions_to_count = directions_to_count
        self.incoming_direction = incoming_direction
        self.outgoing_direction = outgoing_direction
        self.movement_threshold = movement_threshold

    def build_vehicle_counting_type(self, vehicle_type, vehicle):
        if vehicle_type in self.directional_moving_vehicle_types:
            return DirectionalMovingVehicleCounting(self.directions_to_count, self.incoming_direction,
                                                    self.outgoing_direction, self.movement_threshold)
        else:
            return NotVehicleCounting()
