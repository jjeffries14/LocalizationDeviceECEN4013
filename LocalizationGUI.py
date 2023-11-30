import tkinter as tk
import serial
import threading

class SerialDataApp:
    def __init__(self, root, port, baud):
        self.root = root
        self.port = port
        self.baud = baud
        self.running = True

        self.root.title("Localization Device Interface")
        self.root.configure(bg='light grey')
        self.create_widgets()
        
        self.serial_thread = threading.Thread(target=self.read_from_port)
        self.serial_thread.start()

    def create_widgets(self):
        title = tk.Label(self.root, text="Localization Device Interface", font=("Arial", 24), bg='light grey')
        title.grid(row=0, column=0, columnspan=6, pady=10)

        names = "Aatir Cheema, Abdulrahman Alkandari, Jax Jeffries, Scot Sigler"
        names_label = tk.Label(self.root, text=names, bg='light grey', font=("Arial", 14))
        names_label.grid(row=1, column=0, columnspan=6)

        gps_label = tk.Label(self.root, text="GPS Data:", font=("Arial", 16), bg='light grey')
        gps_label.grid(row=2, column=0, columnspan=6, pady=(5,0))

        self.gps_values = {}
        gps_points = ["Latitude", "Longitude", "Elevation", "Satellites Connected"]
        for i, point in enumerate(gps_points):
            label = tk.Label(self.root, text=f"{point}:", bg='light grey')
            label.grid(row=3+i, column=2, sticky='e')
            value = tk.Label(self.root, text="0", bg='light grey')
            value.grid(row=3+i, column=3, sticky='w')

            self.gps_values[point] = value

        imu_label = tk.Label(self.root, text="IMU Data:", font=("Arial", 16), bg='light grey')
        imu_label.grid(row=7, column=0, columnspan=6, pady=(5,0))

        categories = ["Acceleration", "Angular Velocity", "Magnetic Field"]
        data_points = ["X", "Y", "Z"]

        self.imu_values = {}
        for i, category in enumerate(categories):
            cat_label = tk.Label(self.root, text=f"{category}:", font=("Arial", 14), bg='light grey')
            cat_label.grid(row=8, column=i*2, columnspan=2, pady=(5,0))

            for j, point in enumerate(data_points):
                row = j + 9
                label = tk.Label(self.root, text=f"{point}:", bg='light grey')
                label.grid(row=row, column=i*2, sticky='e')
                value = tk.Label(self.root, text="0", bg='light grey')
                value.grid(row=row, column=i*2+1, sticky='e')

                self.imu_values[f"{category}_{point}"] = value

            

    def read_from_port(self):
        ser = serial.Serial(self.port, self.baud)
        while self.running:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').rstrip()
                self.update_values(line)
        ser.close()

    def update_values(self, data):
        # Assuming data format: lat,long,elev,satellites,accX,accY,accZ,angVelX,angVelY,angVelZ,magX,magY,magZ
        #update once we get actual stream
        data_points = data.split(',')
        gps_points = ["Latitude", "Longitude", "Elevation", "Satellites Connected"]
        imu_categories = ["Acceleration", "Angular Velocity", "Magnetic Field"]
        imu_keys = [f"{category}_{point}" for category in imu_categories for point in ["X", "Y", "Z"]]
        
        for key, value in zip(gps_points, data_points[:4]):
            self.gps_values[key].config(text=value)

        for key, value in zip(imu_keys, data_points[4:]):
            self.imu_values[key].config(text=value)

    def on_closing(self):
        self.running = False
        self.root.destroy()

# Serial port settings
port_name = "/dev/ttyUSB0"  # change to correct port
baud_rate = 9600  # update to correct baud

root = tk.Tk()
root.geometry("600x400") 
root.configure(bg='light grey')
app = SerialDataApp(root, port_name, baud_rate)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
