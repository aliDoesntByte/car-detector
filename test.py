import cv2
import streamlit as st

from src.counting import Direction
from src.vidIO import load_video, save_video
from src.tracker import VehicleTracker

count_direction = [Direction.INCOMING]

# Streamlit App (Slow)
# Uncomment cv2 lines for real-time processing window

st.title("Car Detection and Counting!")

uploaded_video = st.file_uploader("Upload Footage", type=[".mp4"])
dir_path = "data/"

if uploaded_video:
    uploaded_filename = uploaded_video.name
    uploaded_file_path = f"{dir_path}{uploaded_filename}"
    with open(uploaded_file_path, "wb") as uploaded_file:
        uploaded_file.write(uploaded_video.getbuffer())

    frame_list = load_video(uploaded_file_path)

    if st.button("Process"):
        tracker = VehicleTracker(frame_list)
        while not tracker.is_done():
            tracker.track_frame(count_direction)
            # cv2.imshow("Title", tracker.get_frame())
            # cv2.waitKey(10)
            tracker.increment()

        # cv2.destroyAllWindows()

        processed_filename = uploaded_filename + "_processed"
        processed_file_path = f"{dir_path}{processed_filename}.mp4"
        save_video(processed_file_path, frame_list)

        st.video(processed_file_path)


# # OpenCV Window (Faster)
#
# frame_list = load_video("data/cars.mp4")
#
# tracker = VehicleTracker(frame_list)
#
# while not tracker.is_done():
#     tracker.track_frame(count_direction)
#     cv2.imshow("Title", tracker.get_frame())
#     cv2.waitKey(10)
#     tracker.increment()
#
# cv2.destroyAllWindows()
