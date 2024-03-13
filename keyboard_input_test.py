import serial                                   # Import the serial library
import pygame

# port = '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0'  # Replace with your actual serial port
port = 'COM3'  # Replace with your actual serial port
baudrate = 115200  # Adjust to match your device's baud rate
try:
    ser = serial.Serial(port, baudrate)
    print("Serial port opened successfully.")
except serial.SerialException as e:
    print("Error opening serial port:", e)
    exit()

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
                data_to_send = f" 100 |    0\n".encode() 
            if event.key == pygame.K_k :
                data_to_send = f"-100 |    0\n".encode()  
            if event.key == pygame.K_j :
                data_to_send = f"   0 |  100\n".encode() 
            if event.key == pygame.K_l :
                data_to_send = f"   0 | -100\n".encode()
                
            if event.key == pygame.K_SPACE :
                data_to_send = f"   0 |    0\n".encode()  
                
            ser.write(data_to_send)
            print(f"Data sent over serial:{data_to_send}")

# Quit Pygame even if the loop breaks (optional)
pygame.quit()
