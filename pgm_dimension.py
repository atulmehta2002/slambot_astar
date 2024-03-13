import io

def get_pgm_pixel_dimensions(pgm_file):
    try:
        with open(pgm_file, "rb") as f:
            # Read the header
            header = f.readline().decode("ascii").strip()
            if header != "P5":  # Check for valid PGM format
                print(f"Invalid PGM format: {pgm_file}")
                return None

            # Read the width and height
            width, height = map(int, f.readline().decode("ascii").strip().split())
            _ = f.readline()  # Skip the maximum gray value line

            return width, height

    except FileNotFoundError:
        print(f"Error: PGM file not found: {pgm_file}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
pgm_file_path = "room.pgm"  # Replace with your actual file path
width, height = get_pgm_pixel_dimensions(pgm_file_path)

if width is not None and height is not None:
    print(f"PGM image dimensions: {width} pixels (width) x {height} pixels (height)")
else:
    print("Failed to read PGM dimensions.")
