import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from process_videos import process_videos

# Set up the font
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not os.path.exists(font_path):  # If the path doesn't exist, try an alternative
    font_path = "/Library/Fonts/Arial.ttf"  # or any other valid font path on macOS
font = ImageFont.truetype(font_path, 12)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

process_videos()

videos = {
    'Yüzme Havuzu': {'path': 'video_01.mp4', 'capacity': 25, 'start': 12, 'end': 20, "icon": "Files/pool.png"},
    'Basketbol Sahası': {'path': 'video_01.mp4', 'capacity': 10, 'start': 12, 'end': 23, "icon": "Files/basketball.png"},
    'Tenis kortu': {'path': 'video_01.mp4', 'capacity': 4, "start": 12, "end": 24, "icon": "Files/tennis_racket.png"},
}

hourly_data = {}
capacities = {}
start_end_times = {}

for place in videos:
    with open(f'{place}_crowd_data.json', 'r') as f:
        crowd_data = json.load(f)
    capacity = videos[place]['capacity']
    hourly_data[place] = [min(count, capacity) for count in crowd_data]
    capacities[place] = capacity
    start_end_times[place] = (videos[place]["start"], videos[place]['end'])


class Apsiyon(QWidget):
    def __init__(self, time_index):
        super().__init__()
        self.initUI(time_index)

    def initUI(self, time_index):
        self.setWindowTitle('Crowd Monitoring System')
        self.layout = QHBoxLayout(self)

        self.places = {place: sum(data) / len(data) for place, data in hourly_data.items()}

        self.buttons_frame = QFrame(self)
        self.buttons_layout = QGridLayout(self.buttons_frame)
        self.layout.addWidget(self.buttons_frame)

        self.graph_frame = QFrame(self)
        self.graph_layout = QHBoxLayout(self.graph_frame)
        self.layout.addWidget(self.graph_frame, alignment=Qt.AlignCenter)

        self.current_chart = None
        self.current_graph = None
        self.current_button = None

        for place, info in videos.items():
            button_frame = QFrame(self.buttons_frame)
            button_layout = QHBoxLayout(button_frame)

            button = QPushButton(place, self)
            button.setFixedSize(150, 50)  # Set the button size
            button.clicked.connect(lambda checked, p=place: self.show_donut_chart(p, time_index))
            button_layout.addWidget(button)

            if info['icon']:
                icon_label = QLabel(self)
                icon = QPixmap(info['icon']).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(icon)
                button_layout.addWidget(icon_label)

            self.buttons_layout.addWidget(button_frame)

        self.logo = QPixmap("Files/apsiyon.webp").scaled(650, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(self.logo)
        self.layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

    def show_donut_chart(self, place, time_index):
        # Clear any existing charts or graphs
        self.clear_existing_widgets()

        self.current_chart = QLabel(self)
        self.graph_layout.addWidget(self.current_chart, alignment=Qt.AlignCenter)

        time_index_adjusted = time_index - videos[place]["start"]

        try:
            current_count = hourly_data[place][time_index_adjusted]
        except IndexError:
            print(f"Error: time_index {time_index_adjusted} is out of range for {place}")
            return

        capacity = capacities[place]
        percentage = (current_count / capacity) * 100
        angle_extent = (percentage / 100) * 360

        arc_color = self.get_gradient_color(percentage)

        image = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(image)

        image_draw.pieslice([50, 50, 250, 250], start=-90, end=359.99, fill=(211, 211, 211))
        # Draw the filled arc (gradient color for the percentage part)
        if percentage > 0:
            if angle_extent >= 360: angle_extent = 359.999
            image_draw.pieslice([50, 50, 250, 250], start=-90, end=angle_extent-90, fill=arc_color)

        # Draw the inner circle to create the donut shape
        image_draw.ellipse([100, 100, 200, 200], fill='white')

        # Add text
        image_draw.text((150, 130), "Aktif", fill='black', font=font, anchor="mm")
        image_draw.text((150, 150), "Doluluk Oranı", fill='black', font=font, anchor="mm")
        image_draw.text((150, 170), f"{percentage:.2f}%", fill='brown', font=font, anchor="mm")
        image_draw.text((150, 270), f"Mevcut İnsan Sayısı: {current_count}", fill='black', font=font, anchor="mm")
        image_draw.text((150, 290), f"Kapasite: {capacity}", fill='black', font=font, anchor="mm")

        image_qt = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(image_qt)

        self.current_chart.setPixmap(pixmap)

        self.current_button = QPushButton("Detayları Göster", self)
        self.current_button.clicked.connect(lambda: self.toggle_graph(place, time_index))
        self.graph_layout.addWidget(self.current_button, alignment=Qt.AlignCenter)

    def clear_existing_widgets(self):
        if self.current_chart:
            self.current_chart.setParent(None)
            self.current_chart = None
        if self.current_graph:
            self.current_graph.setParent(None)
            self.current_graph = None
        if self.current_button:
            self.current_button.setParent(None)
            self.current_button = None
        if self.logo_label:
            self.logo_label.setParent(None)
            self.logo_label = None

    def toggle_graph(self, place, time_index):
        if self.current_graph:
            self.current_graph.setParent(None)
            self.current_graph = None
            self.current_button.setText("Detayları Göster")
        else:
            self.show_graph(place, time_index)
            self.current_button.setText("Detayları Gizle")

    def get_gradient_color(self, percentage):
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        red = (255, 0, 0)

        if percentage < 50:
            ratio = percentage / 50
            color = tuple(int(green[i] * (1 - ratio) + yellow[i] * ratio) for i in range(3))
        else:
            ratio = (percentage - 50) / 50
            color = tuple(int(yellow[i] * (1 - ratio) + red[i] * ratio) for i in range(3))

        return '#{:02x}{:02x}{:02x}'.format(*color)

    def show_graph(self, place, time_index):
        hourly = hourly_data.get(place, [])
        time_index_adjusted = time_index - videos[place]["start"]
        hourly = hourly[:time_index_adjusted + 1]
        start_time, end_time = start_end_times[place]
        hours = np.arange(start_time, end_time + 1)
        crowdedness = np.array(hourly[:len(hours)])  # Adjust data length if needed

        if len(crowdedness) < len(hours):
            crowdedness = np.append(crowdedness, [None] * (len(hours) - len(crowdedness)))

        self.figure = Figure(figsize=(12, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.graph_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        self.ax.clear()
        self.ax.plot(hours, crowdedness, marker='o')
        self.ax.set_title(f'{place} için doluluk oranı')
        self.ax.set_xlabel('Saat')
        self.ax.set_ylabel('Yoğunluk')
        self.ax.grid(True)
        self.ax.set_xticks(hours)
        self.ax.set_xticklabels([f'{hour}:00' for hour in hours])
        self.canvas.draw()

        self.current_graph = self.canvas


if __name__ == '__main__':
    app = QApplication(sys.argv)
    time = datetime.now()
    time_index = int(str(time)[11:13])


    main_app = Apsiyon(time_index)
    main_app.show()
    sys.exit(app.exec())
