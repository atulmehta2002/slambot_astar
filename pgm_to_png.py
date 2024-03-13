from PIL import Image
import matplotlib.pyplot as plt

scale_factor = 5  # Scale up to 500%
pgm_file = "room.pgm"
png_file = "room.png"

    
def scale_and_save_png(pgm_file, scale_factor, png_file):
  try:
    raw_pgm = Image.open(pgm_file)                                                                                               # Open the PGM image
    scaled_pgm = raw_pgm.resize((int(raw_pgm.width * scale_factor), int(raw_pgm.height * scale_factor)), Image.NEAREST)          # Scale the image using resize
    
    # png_image = Image.open(scaled_pgm).convert('L')                                                                            # Open the PGM image in grayscale mode (L)
    scaled_pgm = scaled_pgm.convert('RGB')                                                                                       # Convert to RGB for compatibility with PNG format 
    scaled_pgm.save(png_file, format='PNG')                                                                                      # Save the image as a PNG file

    print(f"PGM file scaled and converted to PNG and saved as: {png_file}")

  except FileNotFoundError:
    print(f"Error: PGM file not found: {pgm_file}")
  except Exception as e:
    print(f"An error occurred: {e}")

def show_plots(pgm_file):

    image_1 = Image.open(pgm_file).convert('RGB')
    print(f"Displaying the Plot for original PGM file")

    plt.imshow(image_1)
    plt.title(f"PGM Image: {pgm_file}")
    plt.show()

scale_and_save_png(pgm_file, scale_factor, png_file)
# show_plots(pgm_file)