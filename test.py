def read_pgm_header(filename):
    with open(filename, "rb") as f:
        f.readline()  # Skip magic number
        width, height = map(int, f.readline().split())
        depth = int(f.readline())
        return width, height, depth

# Read the header information
width, height, depth = read_pgm_header("room.pgm")

# Calculate pixel coordinates of origin based on resolution
origin_x = int(abs(-2.78) / 0.05)  # Assuming positive X is to the right
origin_y = int(abs(-2.01) / 0.05)  # Assuming positive Y is up

print(f"Image dimensions: {width}x{height}")
print(f"Origin in pixels: ({origin_x}, {origin_y})")
