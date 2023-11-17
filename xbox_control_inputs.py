import asyncio
import evdev

def find_controller():
    # Gets the path to the XBox controller
    # Looks through all the devices found using the evdev path, and finds the one containing "Xbox"
    # Returns that path to use in the loop
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:
        name = device.name
        output = "Himal this is you speaking. Controller not found"
        found = name.find("Xbox")
        if found != -1:
            output = device.path
            break

    return output

class controller:
    def __init__(self, path_str):
	# Define the controller based on the path found by the function above
        self.path = path_str

	# Set the key values to 0 (for unpressed), the joystick values to 32767
	# (since they range from 0 to 2^16-1) as the middle value, and the trigger values to 0 (up to 1023)
        self.A_key = 0
        self.B_key = 0
        self.X_key = 0
        self.Y_key = 0
        self.L_x_axis = 32767
        self.L_y_axis = 32767
        self.R_x_axis = 32767
        self.R_y_axis = 32767
        self.L_bumper = 0
        self.L_trigger = 0
        self.R_bumper = 0
        self.R_trigger = 0
        self.D_up = 0
        self.D_down = 0
        self.D_left = 0
        self.D_right = 0

    def update(self):
        dev = evdev.InputDevice(self.path)
        for event in dev.read():
            # Set the hoystick variable values equal to the event values (0 to 65535)
            if event.code == 0:
                self.L_x_axis = event.value
            elif event.code == 1:
                self.L_y_axis = event.value
            elif event.code == 2:
                self.R_x_axis = event.value
            elif event.code == 5:
                self.R_y_axis = event.value
            
            # Set the button values to the event values (0 or 1)
            elif event.code == 304:
                self.A_key = event.value
            elif event.code == 305:
                self.B_key = event.value
            elif event.code == 307:
                self.X_key = event.value
            elif event.code == 308:
                self.Y_key = event.value
            elif event.code == 311:
                self.L_bumper = event.value
            elif event.code == 310:
                self.R_bumper = event.value
            
            # Set the trigger values equal to the event values (0 to 1023)
            elif event.code == 9:
                self.L_trigger = event.value
            elif event.code == 10:
                self.R_trigger = event.value
            
            # Set the appropriate D-pad value to 1 depending on the event value, otherwise reset to 0 if the event value is zero
            elif event.code == 17:
                if event.value == -1:
                    self.D_up = 1
                elif event.value == 1:
                    self.D_down = 1
                elif event.value == 0:
                    self.D_up = 0
                    self.D_down = 0
            
            elif event.code == 16:
                if event.value == -1:
                    self.D_left = 1
                elif event.value == 1:
                    self.D_right = 1
                elif event.value == 0:
                    self.D_left = 0
                    self.D_right = 0
                

async def controller_inputs (controller_path):
    dev = evdev.InputDevice(controller_path)

    async for ev in dev.async_read_loop():
        if ev.code == 1:
            fraction = 1 - ev.value/65535
            print(fraction)
            return fraction

    asyncio.sleep(0.01)