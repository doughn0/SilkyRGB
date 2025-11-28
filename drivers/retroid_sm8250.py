import os

class RGBDriver:
    def __init__(self, extra: dict = None) -> None:
        """
        Initializes the RGB Driver for Retroid devices using standard Linux LED class paths.
        It pre-opens file descriptors for all LED channels to ensure high-performance writing.
        """
        self.led_fds = []
        
        # Base path for Linux LED controls
        base_path = '/sys/class/leds'

        # Define the physical mapping of the LEDs.
        # Based on the ls output provided: l:r1, l:g1, l:b1, etc.
        # We assume the logical order for incoming data is:
        # Left LEDs (1-4) then Right LEDs (1-4).
        # Each LED has 3 channels: Red, Green, Blue.
        sides = ['l', 'r']           # Left side, Right side
        led_indices = [1, 2, 3, 4]   # 4 LEDs per side
        colors = ['r', 'g', 'b']     # Red, Green, Blue components
        
        # We iterate to create a flat list of file descriptors that matches 
        # the expected structure of the incoming RGB list: [R, G, B, R, G, B, ...]
        for side in sides:
            for index in led_indices:
                for color in colors:
                    # Construct the folder name found in /sys/class/leds (e.g., "l:r1")
                    led_dir = f"{side}:{color}{index}"
                    
                    # The standard Linux control file is 'brightness' inside that directory
                    full_path = os.path.join(base_path, led_dir, 'brightness')
                    
                    try:
                        # Open file in Write Only mode. 
                        # We keep the File Descriptor (fd) open for the lifespan of the driver.
                        fd = os.open(full_path, os.O_WRONLY)
                        self.led_fds.append(fd)
                    except FileNotFoundError:
                        # Handle case where hardware might differ slightly
                        print(f"RGBDriver Warning: LED path not found: {full_path}")
                        self.led_fds.append(None)
                    except Exception as e:
                        print(f"RGBDriver Error opening {full_path}: {e}")
                        self.led_fds.append(None)

    def render(self, rgb_data: list[int]) -> list[int]:
        """
        Prepares the data for writing. 
        In the new system, we don't need to pack bytes or apply hex patches.
        We simply pass the integer list through, potentially truncating if it's too long.
        """
        # Ensure we don't exceed the number of available physical LEDs
        return rgb_data[:len(self.led_fds)]

    def write(self, led_data: list[int]) -> None:
        """
        Writes the brightness values to the individual LED files.
        Expects a flat list of integers [0-255].
        """
        if not led_data:
            return

        for i, value in enumerate(led_data):
            # Safety check to ensure we have a file descriptor for this data point
            if i < len(self.led_fds) and self.led_fds[i] is not None:
                try:
                    # Convert integer (0-255) to string bytes (e.g., b'255')
                    # This is required by the Linux file system interface
                    payload = str(value).encode('utf-8')
                    
                    # Write directly to the file descriptor
                    os.write(self.led_fds[i], payload)
                except OSError:
                    # If an IO error occurs (device busy/disconnected), fail silently to prevent crash
                    pass

    def close(self) -> None:
        """
        Closes all open file descriptors to prevent resource leaks.
        """
        for fd in self.led_fds:
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self.led_fds = []