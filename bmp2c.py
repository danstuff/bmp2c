from PIL import Image
import sys, os

# black-and-white mode, each pixel is a single bit
def mode_bw(file, byte, pixel):
    byte += "1" if pixel[0] + pixel[1] + pixel[2] else "0"
    if len(byte) == 8:
        file.write(f"{int(byte, 2)},")
        byte = ""
    return byte

# rgb mode, each pixel is 3 bytes
def mode_rgb(file, byte, pixel):
    file.write(f"{pixel[0]},{pixel[1]},{pixel[2]},")

# rgba mode, each pixel is 4 bytes
def mode_rgba(file, byte, pixel):
    file.write(f"{pixel[0]},{pixel[1]},{pixel[2]},")
    if len(pixel) >= 4:
        file.write(f"{pixel[3]},")
    else:
        file.write("255,")

color_modes = {
    "bw" : mode_bw,
    "rgb" : mode_rgb,
    "rgba" : mode_rgba,
}

if len(sys.argv) < 3 or not sys.argv[1] in color_modes:
    print("Usage: python3 bmp2c.py <bw|rgb|rgba> <image file path>")
    exit(0)

image_name = os.path.splitext(sys.argv[2])[0]
color_mode = color_modes[sys.argv[1]]

with open(f"{image_name}.c", "w") as file:
    file.write(f"const uint8_t {image_name} = {{")

    with Image.open(sys.argv[2]) as image:
        byte = ""
        for pixel in image.getdata():
            byte = color_mode(file, byte, pixel)

    file.write("};\n")

print(f"Wrote converted image to {image_name}.c")
