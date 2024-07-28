import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
from process_videos import process_videos



os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

process_videos()

videos = {
    'Yüzme Havuzu': {'path': 'video_01.mp4', 'capacity': 25, 'start':12,'end': 20,"icon":"Files/pool.png"},
    'Basketbol Sahası': {'path': 'video_01.mp4', 'capacity': 10, 'start':12,'end': 23,"icon":"Files/basketball.png"},
    'Tenis kortu': {'path': 'video_01.mp4', 'capacity': 4,"start":6 , "end":18,"icon":"Files/tennis_racket.png" },
}

hourly_data = {}
capacities = {}
start_end_times={}


for place in videos:
    with open(f'{place}_crowd_data.json', 'r') as f:
        crowd_data = json.load(f)
    capacity = videos[place]['capacity']
    hourly_data[place] = [min(count, capacity) for count in crowd_data]
    capacities[place] = capacity
    start_end_times[place] = (videos[place]["start"], videos[place]['end'])


class Apsiyon:
    def __init__(self, root,time_index):
        self.root = root
        self.root.title("Crowd Monitoring System")

        self.places = {place: sum(data) / len(data) for place, data in hourly_data.items()}

        self.buttons_frame = ttk.Frame(root)
        self.buttons_frame.pack(pady=20)

        self.graph_frame = ttk.Frame(root)
        self.graph_frame.pack(pady=20)

        self.current_chart = None
        self.current_graph = None  # To keep track of the current graph canvas
        self.current_button = None  # To keep track of the current graph button



        for place, info in videos.items():
            frame = ttk.Frame(self.buttons_frame)
            frame.pack(side=tk.LEFT, padx=30)

            button = ttk.Button(frame, text=place, command=lambda p=place: self.show_donut_chart(p, time_index))
            button.pack(side=tk.LEFT)

            if info['icon']:
                # Add icon image next to the button
                icon = ImageTk.PhotoImage(Image.open(info['icon']).resize((20, 20), Image.LANCZOS))
                label = ttk.Label(frame, image=icon)
                label.image = icon  # Keep a reference to avoid garbage collection
                label.pack(side=tk.LEFT)

        # Update with your logo path
        self.logo = ImageTk.PhotoImage(
            Image.open("Files/apsiyon.webp").resize((650,450), Image.LANCZOS))  # Resize to fit better
        self.logo_label = ttk.Label(root, image=self.logo)
        self.logo_label.pack(pady=(50, 50))  # Adjust the padding as needed
        self.logo_label.pack(anchor=tk.CENTER)

    def show_donut_chart(self, place, time_index):
        # Clear any existing charts or graphs
        self.logo_label.destroy()

        if self.current_chart:
            self.current_chart.destroy()
            self.current_chart = None
        if self.current_graph:
            self.current_graph.destroy()
            self.current_graph = None
        if self.current_button:
            self.current_button.pack_forget()
            self.current_button = None

        self.current_chart = tk.Canvas(self.graph_frame, width=300, height=300, bg='white')
        self.current_chart.pack(pady=10)

        # Calculate percentage and corresponding arc angle
        time_index-=videos[place]["start"]
        current_count = hourly_data[place][time_index]
        capacity = capacities[place]
        percentage = (current_count / capacity) * 100
        angle_extent = (percentage / 100) * 360

        # Determine color based on whether capacity is exceeded
        arc_color = self.get_gradient_color(percentage)

        # Draw the background arc (full circle) with gray color
        self.current_chart.create_arc((50, 50, 250, 250), start=90, extent=359.99, fill="light gray", outline="")  # Gray background

        # Draw the filled arc (clockwise)
        if percentage > 0:
            if angle_extent >= 360: angle_extent = 359.999
            self.current_chart.create_arc((50, 50, 250, 250), start=90, extent=-angle_extent, fill=arc_color, outline="")

        # Draw the inner circle to create the donut shape
        self.current_chart.create_oval(100, 100, 200, 200, fill='white', outline='white')

        # Display labels and percentage in the center
        self.current_chart.create_text(150, 130, text="Aktif", font=('Arial', 10), fill='black')
        self.current_chart.create_text(150, 150, text="Doluluk Oranı", font=('Arial', 10), fill='black')
        self.current_chart.create_text(150, 170, text=f"{percentage:.2f}%", font=('Arial', 16, 'bold'), fill='brown')

        # Display Capacity and Current People Count below the chart
        self.current_chart.create_text(150, 270, text=f"Mevcut İnsan Sayısı: {current_count}", font=('Arial', 12), fill='black')
        self.current_chart.create_text(150, 290, text=f"Kapasite: {capacity}", font=('Arial', 12), fill='black')

        # Add button to show/hide the graph
        self.current_button = ttk.Button(self.graph_frame, text="Detayları Göster", command=lambda: self.toggle_graph(place,time_index))
        self.current_button.pack(pady=10)


    def toggle_graph(self, place,time_index):
        if self.current_graph:
            # Hide the graph if it's currently visible
            self.current_graph.destroy()
            self.current_graph = None
            self.current_button.config(text="Detayları Göster")  # Update button text to "Show Graph"
        else:
            # Display the graph
            self.show_graph(place,time_index)
            self.current_button.config(text="Detayları Gizle")  # Update button text to "Hide Graph"

    def get_gradient_color(self, percentage):
        # Calculate the gradient color from green to red based on percentage
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        red = (255, 0, 0)

        if percentage < 50:
            ratio = percentage / 50
            color = tuple(int(green[i] * (1 - ratio) + yellow[i] * ratio) for i in range(3))
        else:
            ratio = (percentage - 50) / 50
            color = tuple(int(yellow[i] * (1 - ratio) + red[i] * ratio) for i in range(3))

        return f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

    def show_graph(self, place,time_index):
        # Extract the hourly data for the selected place

        hourly = hourly_data.get(place, [])
        hourly=hourly[:time_index+1]
        start_time, end_time = start_end_times[place]
        hours = np.arange(start_time, end_time + 1)
        crowdedness = np.array(hourly[:len(hours)])  # Adjust data length if needed

        if len(crowdedness) < len(hours):
            crowdedness = np.append(crowdedness, [None] * (len(hours) - len(crowdedness)))

        # Create and display the graph
        self.figure = Figure(figsize=(12, 5), dpi=100)  # Adjust size for better fitting
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()

        self.ax.clear()
        self.ax.plot(hours, crowdedness, marker='o')
        self.ax.set_title(f'{place} için doluluk oranı')
        self.ax.set_xlabel('Saat')
        self.ax.set_ylabel('Yoğunluk'
                           '')
        self.ax.grid(True)
        self.ax.set_xticks(hours)  # Set the x-ticks to the time frames
        self.ax.set_xticklabels([f'{hour}:00' for hour in hours])  # Label x-ticks as time frames
        self.canvas.draw()

        # Set the current graph
        self.current_graph = self.canvas.get_tk_widget()

# Create the main window
root = tk.Tk()
time = datetime.now()
time_index = int(str(time)[11:13])
print(time_index)

app = Apsiyon(root,time_index)
root.mainloop()
