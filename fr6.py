import cv2
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Initialize the camera
cap = cv2.VideoCapture(1)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
width = 640
height = 480
min_brightness = 100
max_brightness = 100

#CALIBRATION TOOLS
CF = 1.00 # calibration factor multiplier factor
PD = 200 #PEAK DISTANCE ON CHART MIN-MAX VAL ie 200
WV = 650

CF1 = CF # calibration factor multiplier factor
PD1 = PD #PEAK DISTANCE ON CHART MIN-MAX VAL ie 200
WV1 = WV

# Set up the plot window
fig, ax = plt.subplots()
ax_reset = plt.axes([0.85, 0.05, 0.1, 0.075])
button_reset = plt.Button(ax_reset, 'New run')

# Initialize arrays to store brightness data and time data
brightness = []
times = []

# Initialize peak counter and distance variables
peaks = 0
peak_detected = True
distance = 0
last_brightness = None

def reset_plot(event):
    global brightness, times, peaks, peak_detected, distance, last_brightness, min_brightness, max_brightness
    brightness = []
    peak_detected = True
    times = []
    peaks = 0
    distance = 0
    last_brightness = None
    ax.clear()
    ax.set_title("Peak Detection")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Brightness")
    min_brightness = 100
    max_brightness = 100
    class Application(tk.Frame):
        def __init__(self, master=None):
            super().__init__(master)
            self.master = master
            self.pack()
            self.create_widgets()
        def create_widgets(self):
            # Create input fields
            self.master.geometry("480x200")
            self.master.title("OptiXs inter_FODL_meter")
            self.cf_label = tk.Label(self, text="CF:")
            self.cf_label.grid(row=0, column=0)
            self.cf_entry = tk.Entry(self, width=10)
            self.cf_entry.insert(tk.END, CF)
            self.cf_entry.grid(row=0, column=1)
            self.pd_label = tk.Label(self, text="PD:")
            self.pd_label.grid(row=1, column=0)
            self.pd_entry = tk.Entry(self, width=10)
            self.pd_entry.insert(tk.END, PD)
            self.pd_entry.grid(row=1, column=1)
            self.wv_label = tk.Label(self, text="WV:")
            self.wv_label.grid(row=2, column=0)
            self.wv_entry = tk.Entry(self, width=10)
            self.wv_entry.insert(tk.END, WV)
            self.wv_entry.grid(row=2, column=1)
        
        # Create output fields
            self.cf_output_label = tk.Label(self, text="CF:")
            self.cf_output_label.grid(row=0, column=2)
            self.cf_output = tk.Label(self, text=CF)
            self.cf_output.grid(row=0, column=3)
            self.pd_output_label = tk.Label(self, text="PD:")
            self.pd_output_label.grid(row=1, column=2)
            self.pd_output = tk.Label(self, text=PD)
            self.pd_output.grid(row=1, column=3)
            self.wv_output_label = tk.Label(self, text="WV:")
            self.wv_output_label.grid(row=2, column=2)
            self.wv_output = tk.Label(self, text=WV)
            self.wv_output.grid(row=2, column=3)
        
        # Create "Save Parameters" button
            self.save_button = tk.Button(self, text="Save and Start", command=self.save_parameters)
            self.save_button.grid(row=3, column=1)
    
        def save_parameters(self):
            # Get values from input fields and update output fields
            self.cf_output.config(text=cf_value)
            self.pd_output.config(text=pd_value)
            self.wv_output.config(text=wv_value)
            self.cf_output_label = tk.Label(self, text="CF:")
            self.cf_output_label.grid(row=0, column=2)
            self.cf_output = tk.Label(self, text=CF)
            self.cf_output.grid(row=0, column=3)  
            self.pd_output_label = tk.Label(self, text="PD:")
            self.pd_output_label.grid(row=1, column=2)
            self.pd_output = tk.Label(self, text=PD)
            self.pd_output.grid(row=1, column=3)  
            self.wv_output_label = tk.Label(self, text="WV:")
            self.wv_output_label.grid(row=2, column=2)
            self.wv_output = tk.Label(self, text=WV)
            self.wv_output.grid(row=2, column=3)
        def save_parameters(self):
    # Get values from input fields and update output fields
            global CF1, PD1, WV1
            CF1 = float(self.cf_entry.get())
            PD1 = int(self.pd_entry.get())
            WV1 = int(self.wv_entry.get())
            self.cf_output.config(text=CF1)
            self.pd_output.config(text=PD1)
            self.wv_output.config(text=WV1)
            PD = PD1
            CF = CF1
            WV = WV1
            self.master.destroy()

    root = tk.Tk()
    app = Application(master=root)  
    app.mainloop()

button_reset.on_clicked(reset_plot)


# Process each frame from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if ret:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Take the average brightness of a 5x5 area in the center of the frame
        center = gray.shape[0] // 2
        brightness.append(int(gray[center - 2:center + 3, center - 2:center + 3].mean()))

        # Store the current time
        times.append(len(times))
        rectangle_frame = frame.copy()

        # Calculate the coordinates for the center of the video
        center_x = int(width / 2)
        center_y = int(height / 2)

    # Calculate the coordinates for the top-left corner of the rectangle
        rect_x = int(center_x - 10)
        rect_y = int(center_y - 10)

    # Draw a 40x40 pixel rectangle in the center of the frame
        cv2.rectangle(rectangle_frame, (rect_x, rect_y), (rect_x+20, rect_y+20), (0, 0, 255), 2)

        if (brightness[-1]) < min_brightness:
            min_brightness = (brightness[-1])
        
        elif (brightness[-1]) > max_brightness:
            max_brightness = (brightness[-1])

        # Display the brightness value on the image
        text = f"Intensity: {brightness[-1]} ,{CF1},{PD1},{WV1}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 0), 2)

        mixed_frame = cv2.addWeighted(frame, 0.5, rectangle_frame, 0.5, 0)
       
        cv2.imshow('OptiXs inter_FODL_meter', mixed_frame)    

        # Clear the plot and replot the data
        ax.clear()
        ax.set_title("Peak Detection")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Brightness")
        ax.plot(times, brightness)
        
        # Check for peaks in the brightness data
        new_peaks, _ = find_peaks(-np.array(brightness), height=-80)

        # Check if a peak was detected on the way down
        if len(new_peaks) > peaks:
            if brightness[-1] > 200:
                peak_detected = True
            elif peak_detected and brightness[-1] < 100:
                peaks += 1
                distance = 0
                peak_detected = False
                print(f"Peak detected at time {len(times)}")
        else:
            peak_detected = False

        # Calculate the distance between peaks on both slopes
        if last_brightness is not None:
            if brightness[-1] - last_brightness >= PD1/20:
                distance += WV1/20*CF1/2
            elif last_brightness - brightness[-1] >= PD1/20:
                distance += WV1/20*CF1/2
        last_brightness = brightness[-1]
    
        # Display the peak count and distance value
        ax.set_title(f"Calib. factor: {CF1}, Peak height: {PD1}, WV: {WV}\nB_MIN: {min_brightness}, B_MAX: {max_brightness}, DIFF:{max_brightness - min_brightness},\nFringe count: {peaks}, Distance: {peaks*WV1/2} nm, {peaks*WV1/1000/2} um,\nAprox. between peak distance: {distance} nm")

        # Pause to allow the plot to update
        plt.pause(0.001)  

    # Check for key press to exit
    if cv2.waitKey(1) == ord('q'):
        break  
    
# Release the camera and close all windows

cap.release()
cv2.destroyAllWindows()
plt.close('all')
