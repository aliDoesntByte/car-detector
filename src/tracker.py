from ultralytics import YOLO
import cv2
import torch

from src.counting import VehicleCountingFactory
from src.vehicles import Vehicle, VehicleTypes
from src.config import (YOLO_MODEL_PATH,

                    INCOMING_DIRECTION,
                    OUTGOING_DIRECTION,
                    MOVEMENT_THRESHOLD,

                    COLOR_COUNTED_VEHICLE_BOX,
                    COLOR_NOT_COUNTED_VEHICLE_BOX,
                    COLOR_TEXT,
                    COLOR_COUNTER_BOX,

                    TEXT_FONT_SIZE,
                    TEXT_THICKNESS,
                    BOUNDING_BOX_THICKNESS)


class VehicleTracker:

    def __init__(self, frame_list):
        self.model = YOLO(YOLO_MODEL_PATH)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(device)
        self.frame_list = frame_list
        self.frame_counter = 0
        self.vehicles = {}

    def is_done(self):
        return not self.frame_counter < len(self.frame_list)

    def increment(self):
        if self.is_done():
            # No more frames left
            return None

        # Select the next in line frame and increment the counter
        self.frame_counter += 1

    def get_frame(self):
        if not self.is_done():
            return self.frame_list[self.frame_counter]
        return None

    def calculate_labels_count(self):
        labels_count = {}
        for vehicle in self.vehicles.values():
            if vehicle.should_be_counted:

                vehicle_type = vehicle.get_type()
                count = labels_count.get(vehicle_type)
                if not count:
                    count = 0
                count += 1
                labels_count.update({vehicle_type: count})

        return labels_count

    def annotate_labels_count(self, frame):

        labels_count = self.calculate_labels_count()
        start_pos = (0, 0)

        for labels_enum, count in labels_count.items():
            color = COLOR_COUNTER_BOX

            # Determine size of the text box
            label = f"{labels_enum.value} {count}"
            (width, height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SIZE, TEXT_THICKNESS)

            # Draw text background box
            cv2.rectangle(frame, start_pos, (start_pos[0] + 10 + width, start_pos[1] + height + 5), color, -1)
            # Write text
            cv2.putText(frame, label, (start_pos[0] + 10, start_pos[1] + 15), cv2.FONT_HERSHEY_SIMPLEX,
                        TEXT_FONT_SIZE, COLOR_TEXT, TEXT_THICKNESS)

            start_pos = (0, start_pos[1] + height + 5)

    def annotate_box(self, frame, label, color, start_box, end_box):
        # Determine size of the text box
        (width, height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SIZE, TEXT_THICKNESS)

        # Draw text background box
        cv2.rectangle(frame, (start_box[0], start_box[1] - 20), (start_box[0] + width, start_box[1]), color, -1)
        # Write text
        cv2.putText(frame, label, (start_box[0], start_box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    TEXT_FONT_SIZE, COLOR_TEXT, TEXT_THICKNESS)

        # Draw bounding box
        cv2.rectangle(frame, start_box, end_box, color, BOUNDING_BOX_THICKNESS)

    def draw_box(self, frame, label, vehicle, bounding_box_xyxy, draw_uncounted):

        start_box = (int(bounding_box_xyxy[0]), int(bounding_box_xyxy[1]))
        end_box = (int(bounding_box_xyxy[2]), int(bounding_box_xyxy[3]))

        # Annotate for counted vehicles or objects
        if vehicle.should_be_counted:
            color = COLOR_COUNTED_VEHICLE_BOX
            self.annotate_box(frame, label, color, start_box, end_box)

        # Annotate for uncounted vehicles or objects
        if not vehicle.should_be_counted and draw_uncounted:
            color = COLOR_NOT_COUNTED_VEHICLE_BOX
            self.annotate_box(frame, label, color, start_box, end_box)

    def update_vehicle_dictionary(self, vehicle_id, bounding_box_xyxy):
        # Adds to vehicle dictionary / updates its last position
        vehicle = self.vehicles.get(vehicle_id)
        current_pos = (bounding_box_xyxy[0:2] + bounding_box_xyxy[2:4]) / 2  # current pos is center of bounding box
        if vehicle:
            vehicle.last_pos = current_pos
        else:
            self.vehicles.update({vehicle_id: Vehicle(current_pos)})
            vehicle = self.vehicles.get(vehicle_id)

        return vehicle

    def create_vehicle_counting_factory(self, directions_to_count, incoming_direction,
                                        outgoing_direction, movement_threshold):
        vehicle_counting_factory = VehicleCountingFactory()
        vehicle_counting_factory.set_directional_moving_counting_type(directions_to_count, incoming_direction,
                                                                      outgoing_direction, movement_threshold)
        return vehicle_counting_factory

    def track_frame(self, directions_to_count, incoming_direction=INCOMING_DIRECTION,
                    outgoing_direction=OUTGOING_DIRECTION, movement_threshold=MOVEMENT_THRESHOLD, draw_uncounted=False):

        if self.is_done():
            return

        # Get the current frame
        frame = self.get_frame()

        # YOLO pretrained model tracks the objects
        tracks = self.model.track(frame, persist=True, show=False, verbose=False)

        # Creates a vehicle counting factory
        vehicle_counting_factory = self.create_vehicle_counting_factory(directions_to_count, incoming_direction,
                                                                        outgoing_direction, movement_threshold)

        # Iterate over every object in the scene
        for box in tracks[0].boxes:
            # Bounding Box  & Vehicle Information
            bounding_box_xyxy = box.xyxy[0]
            vehicle_id = int(box.id[0])
            vehicle_type_id = int(box.cls[0])
            vehicle_type_name = tracks[0].names[vehicle_type_id]
            vehicle_type = VehicleTypes(vehicle_type_name)

            # Update vehicle dictionary => change the last pos
            # Set first & last pos if the vehicle doesn't exist
            vehicle = self.update_vehicle_dictionary(vehicle_id, bounding_box_xyxy)

            # Increment current frame's vehicle type
            vehicle.increment_frame_vehicle_type(vehicle_type)

            # Build the vehicle counting type from the vehicle counting type factory
            # Vehicle counting type determines if the vehicle should be counted or not
            vehicle_counting_type = vehicle_counting_factory.build_vehicle_counting_type(vehicle_type, vehicle)
            vehicle.should_be_counted = vehicle_counting_type.should_count(vehicle)

            # Draw annotated bounding boxes
            label = f"{vehicle.get_type().value} {round(float(box.conf), 2)}"
            self.draw_box(frame, label, vehicle, bounding_box_xyxy, draw_uncounted)

        # draws the labels counter
        self.annotate_labels_count(frame)
