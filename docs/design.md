# Design & Architecture

## Overview

The program is a simple easy to use app that allows users to upload footage of the vehicles. It then allows for
processing of that video to find and label vehicle on the incoming/outgoing lane.

## Architecture

The program is divided into:

### Interface Module:

That are the video file I/O, loading and saving video files to a file path.

**1. vidIO:**
This module is a wrapper for OpenCV reading and writing methods.

### Core Solution:

Most of the program is in here. It is made of data types for storage of vehicle information, methods and criteria for
counting different types of vehicles, and the main tracker class.

**1. vehicles:**
This module contains the vehicle datatype which keeps track of important information about vehicles that will be used in
later processing. Storing the first and last position the vehicle was observed in, number of frames a vehicle was
classified as what type (e.g. the vehicle has been classified as a car for 100 frames but as a truck for 3, so it will
classified as a car). That is used to determine the most likely type of vehicle it is. That is because if you determine
the first/last frame, the model might misclassify it due to it being cropped or noise, etc... Taking the most occurring
type is a much more accurate method for finding how it has been seen throughout the video. And is more stable since
misclassified frames have the same weight as the rest of the correctly classified frames in determining the type. It
also stores whether the vehicle should be counted or not.

**2. counting:**
With the assumption that different vehicle types would have different criteria for choosing whether they would be
counted or not, a state design pattern was used for the counting types. The base class for them was an abstract class. A
factory pattern was used to build the instances of the counting types, allowing for abstracting away details of how a
vehicle type is assigned to its respective counting type.
The counting type implemented in our solution is a Directional Movement Threshold Counter, this means that depending on
the direction of the vector and the amount of movement a vehicle has moved the decision for whether the vehicle should
be counted or not is made. Two vectors can be chosen, an incoming and an outgoing vector. The vector of the vehicle
movement is compared with each by using a dot product of each of them. And if the direction that it aligns with is a
direction to be counted and the magnitude of the movement vector passed the movement threshold, it is counted. If not,
it is not counted.

**3. tracking:**
This is the main module for the solution. Its main job is to extract and store relevant data from the YOLO model's
outputs. At each frame, using the bounding box and classification information from the model, it iterates over each
vehicle/bounding box. With that it can update the vehicle dictionary, adding the vehicle if it is not present which sets
the first position, and updating the last position. Then, it can update the frame count for the type for the current
classification for that vehicle. And finally, with the factory for the counting types it can determine whether it
actually draws the bounding box and increments the label counter or not.

![Tracking Process Flowchart](/docs/tracking_process_flowchart.png)

 
