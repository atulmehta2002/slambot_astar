import serial                                   # Import the serial library
import pygame

# port = '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4:1.0-port0'  # Replace with your actual serial port
port = 'COM3'  # Replace with your actual serial port
baudrate = 115200  # Adjust to match your device's baud rate
try:
    ser = serial.Serial(port, baudrate)
    print("Serial port opened successfully.")
except serial.SerialException as e:
    print("Error opening serial port:", e)
    # exit()

#movement commands
linear_x = 0
angular_z = 0

# Initialize Pygame (minimal initialization for event handling)
pygame.init()

screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
    
def constraints(linear_x, angular_z):
    
        
    print(f"linear_x: {linear_x}, angular_z: {angular_z}")
    return linear_x, angular_z

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
       
        # Check for WASD key presses and print to console
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            if event.key == pygame.K_i :
                data_to_send = f"{linear_x} |    0\n".encode() 
                linear_x = linear_x + 5
            if event.key == pygame.K_COMMA :
                data_to_send = f"-{linear_x} |    0\n".encode() 
                linear_x = linear_x - 5
            if event.key == pygame.K_j :
                data_to_send = f"   0 | {angular_z}\n".encode() 
                angular_z = angular_z + 5
            if event.key == pygame.K_l :
                data_to_send = f"   0 | -{angular_z}\n".encode()
                angular_z = angular_z - 5  
                
            if event.key == pygame.K_SPACE :
                linear_x = 0
                angular_z = 0
                data_to_send = f"{linear_x} | {angular_z}\n".encode() 
                
        # constrict values in the range
        if int(linear_x) >= 250:
            linear_x = 250
        if int(linear_x) <= 0:
            linear_x = 0
        if int(angular_z) >= 250:
            angular_z = 250
        if int(angular_z) <= 0:
            angular_z = 0

        if ((linear_x>0) & (linear_x < 10)):
            linear_x = f"   {linear_x}"
        elif ((linear_x>=10) & (linear_x < 100)):
            linear_x = f"  {linear_x}"
        elif (linear_x>=100):
            linear_x = f" {linear_x}"
        else:
            linear_x = f"   0"

        if ((angular_z>0) & (angular_z < 10)):
            angular_z = f"   {angular_z}"
        elif ((angular_z>=10) & (angular_z < 100)):
            angular_z = f"  {angular_z}"
        elif (angular_z>=100):
            angular_z = f" {angular_z}"
        else:
            angular_z = f"   0"
                
            # ser.write(data_to_send)
            # print(f"Data sent over serial:{data_to_send}")
            print(f"linear_x: {linear_x}, angular_z: {angular_z}")

# Quit Pygame even if the loop breaks (optional)
pygame.quit()

