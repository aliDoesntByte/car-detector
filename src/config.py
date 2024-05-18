import torch

YOLO_MODEL_PATH = "../models/yolov8m.pt"
MOVEMENT_THRESHOLD = 2
INCOMING_DIRECTION = torch.tensor([0, 1], dtype=torch.float)
OUTGOING_DIRECTION = torch.tensor([0, -1], dtype=torch.float)

COLOR_COUNTED_VEHICLE_BOX = (255, 0, 255)
COLOR_NOT_COUNTED_VEHICLE_BOX = (255, 0, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_COUNTER_BOX = (0, 0, 0)

TEXT_FONT_SIZE = 0.6
TEXT_THICKNESS = 1
BOUNDING_BOX_THICKNESS = 2