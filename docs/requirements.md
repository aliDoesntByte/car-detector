# Requirements Analysis

The task was to create a car counter program based on a pre-trained [YOLO](https://github.com/ultralytics/ultralytics)
model and to have an interface built with [Streamlit](https://streamlit.io/), to allow for easy upload of video files
and processing to count the number of vehicles in the video.

Some requirements were also given:

- **Accepts video file upload as an input:**
  That can be done with the Streamlit's input widgets.
- **Uses any YOLO pre-trained model to detect the cars moving in the video:**
  The ultralytics library contains a number of pre-trained models, which can be used for the task of detection and
  classification.
- **Draws bounding boxes on the cars, and annotate each box with the object name (e.g. "Car" "Truck", "Motorbike")**
  YOLO models also provide bounding boxes along with the tracking and detection feature. It also classifies each object.
  Drawing and annotating those boxes can be done using [OpenCV](https://github.com/opencv/opencv).
- **Extra: Count the cars only in the incoming lane (check image below)**
  Isolating the incoming lane can be done in a number of ways: the method used in here makes the assumption that the
  incoming/outgoing lane would generally align to a specific direction. With that we can compare the direction of the
  vector movement of an object with the vector direction of both lanes to figure out if it is on the outgoing and
  incoming lane. For example, an up vector can represent the direction of an incoming lane.
- **Extra: Keep separate count for cars, trucks, motorbikes...**
  The YOLO model tracking also provides details about the objects detected, including the class of the object. With that
  information, separate counters can be created for each label.