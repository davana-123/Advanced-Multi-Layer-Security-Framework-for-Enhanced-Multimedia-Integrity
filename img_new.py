import tkinter as tk
from tkinter import filedialog
from PIL import Image

def encode():
    input_path = filedialog.askopenfilename(title="Select Cover Image")
    output_path = filedialog.asksaveasfilename(title="Save Encoded Image", defaultextension=".png")

    if not input_path or not output_path:
        return

    # Open the cover image
    cover_image = Image.open(input_path)

    # Get the user input (message and password)
    message = message_entry.get()
    password = password_entry.get()

    # Simple password hashing (for educational purposes)
    hashed_password = hash(password)

    # Encoding logic (simple LSB method for demonstration)
    encoded_image = cover_image.copy()
    pixels = encoded_image.load()

    message_index = 0
    for i in range(cover_image.width):
        for j in range(cover_image.height):
            pixel = list(pixels[i, j])
            for channel in range(3):  # RGB channels
                if message_index < len(message):
                    pixel[channel] &= 0xFE  # Clear the least significant bit
                    pixel[channel] |= int(message[message_index])  # Set the least significant bit with message bit
                    message_index += 1
            pixels[i, j] = tuple(pixel)

    # Save the encoded image
    encoded_image.save(output_path)

    result_label.config(text="Image encoded successfully!")

def decode():
    input_path = filedialog.askopenfilename(title="Select Encoded Image")

    if not input_path:
        return

    # Open the encoded image
    encoded_image = Image.open(input_path)

    # Get the user input (password)
    password = password_entry.get()

    # Simple password hashing (for educational purposes)
    hashed_password = hash(password)

    # Decoding logic (simple LSB method for demonstration)
    decoded_message = ""
    pixels = encoded_image.load()

    for i in range(encoded_image.width):
        for j in range(encoded_image.height):
            pixel = list(pixels[i, j])
            for channel in range(3):  # RGB channels
                decoded_message += str(pixel[channel] & 1)  # Extract the least significant bit

    # Convert the binary message to ASCII
    decoded_message = "".join([chr(int(decoded_message[i:i+8], 2)) for i in range(0, len(decoded_message), 8)])

    result_label.config(text=f"Decoded Message: {decoded_message}")

# Create the main window
window = tk.Tk()
window.title("Image Steganography")

# Create GUI components
message_label = tk.Label(window, text="Message:")
message_entry = tk.Entry(window)

password_label = tk.Label(window, text="Password:")
password_entry = tk.Entry(window, show="*")

encode_button = tk.Button(window, text="Encode", command=encode)
decode_button = tk.Button(window, text="Decode", command=decode)

result_label = tk.Label(window, text="")

# Arrange GUI components
message_label.grid(row=0, column=0, pady=5)
message_entry.grid(row=0, column=1, pady=5)

password_label.grid(row=1, column=0, pady=5)
password_entry.grid(row=1, column=1, pady=5)

encode_button.grid(row=2, column=0, pady=10)
decode_button.grid(row=2, column=1, pady=10)

result_label.grid(row=3, columnspan=2, pady=10)

# Start the GUI application
window.mainloop()
