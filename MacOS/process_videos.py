import torch
import cv2
import json
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

videos = {
    'Yüzme Havuzu': {'path': 'video_01.mp4', 'capacity': 25, 'start': 8, 'end': 20, "icon": "Files/pool.png"},
    'Basketbol Sahası': {'path': 'video_01.mp4', 'capacity': 10, 'start': 9, 'end': 21, "icon": "Files/basketball.png"},
    'Tenis kortu': {'path': 'video_01.mp4', 'capacity': 4, "start": 10, "end": 23, "icon": "Files/tennis_racket.png"},
}

def process_videos():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    drawing = False
    ix, iy = -1, -1
    rect = (0, 0, 0, 0)
    current_count = 0

    def draw_rectangle(event, x, y, flags, param):
        nonlocal ix, iy, drawing, img, rect, img_copy
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_copy = img.copy()
                cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
                cv2.imshow('image', img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            rect = (min(ix, x), min(iy, y), max(ix, x), max(iy, y))
            cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
            cv2.imshow('image', img)

    def is_inside_rect(x, y, rect):
        (x1, y1, x2, y2) = rect
        return x1 <= x <= x2 and y1 <= y <= y2

    def process_video(video_path, rect, model, place_name):
        nonlocal current_count
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Failed to open video file: {video_path}")

        count_data = []
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_skip = int(frame_rate)  # Skip frames to process every second

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames
            for _ in range(frame_skip - 1):
                cap.grab()

            results = model(frame)
            inside_people_current = set()

            for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
                if int(cls) == 0:  # Class 0 is 'person' in COCO dataset
                    x_center = int((xyxy[0] + xyxy[2]) / 2)
                    y_center = int((xyxy[1] + xyxy[3]) / 2)
                    person_id = (x_center, y_center)

                    if is_inside_rect(x_center, y_center, rect):
                        inside_people_current.add(person_id)

            current_count = len(inside_people_current)
            count_data.append(current_count)

        cap.release()

        # Write the count data to a JSON file
        with open(f'{place_name}_crowd_data.json', 'w') as f:
            json.dump(count_data, f)

    # Process each video and draw rectangle for each place
    for place, info in videos.items():
        cap = cv2.VideoCapture(info['path'])
        ret, img = cap.read()
        if not ret:
            raise Exception(f"Failed to read the video: {info['path']}")
        img_copy = img.copy()
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', draw_rectangle)
        cv2.waitKey(0)  # Wait for a key press to proceed
        cv2.destroyAllWindows()

        # Make sure the rectangle has been set before processing the video
        if rect == (0, 0, 0, 0):
            raise Exception("No rectangle has been drawn. Please draw a rectangle before proceeding.")

        process_video(info['path'], rect, model, place)
