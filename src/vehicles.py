from enum import Enum


class VehicleTypes(Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    BUS = "bus"
    TRUCK = "truck"
    OTHER = "other"

    @classmethod
    def _missing_(cls, value):
        return cls.OTHER


# Data type to store important information about the vehicle that has been detected
class Vehicle:

    def __init__(self, first_pos):
        self.first_pos = first_pos
        self.last_pos = first_pos
        self.vehicle_types_count = {}
        self.should_be_counted = False

    def get_type(self):
        biggest_count = 0
        biggest_vehicle_type = None

        for vehicle_type, vehicle_type_count in self.vehicle_types_count.items():
            # Iterate over each vehicle to find the vehicle type with the biggest frame count
            if vehicle_type_count > biggest_count:
                biggest_count = vehicle_type_count
                biggest_vehicle_type = vehicle_type

        return biggest_vehicle_type

    # To increment the frame count of the vehicle type of the current frame
    def increment_frame_vehicle_type(self, vehicle_type):
        count = self.vehicle_types_count.get(vehicle_type)
        if not count:
            count = 0
        count += 1
        self.vehicle_types_count.update({vehicle_type: count})
