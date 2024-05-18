import cv2


def load_video(filename):
    video = cv2.VideoCapture(filename)
    frame_list = []

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        frame_list.append(frame)

    video.release()
    return frame_list


def save_video(filename, frame_list, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'MPV4')
    height, width, _ = frame_list[0].shape
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    for frame in frame_list:
        out.write(frame)
    out.release()
