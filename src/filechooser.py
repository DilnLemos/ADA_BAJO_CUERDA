import tkinter as tk
from tkinter import filedialog

def select_file():
    # Create hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open file dialog
    file_path = filedialog.askopenfilename()

    # Destroy the hidden Tkinter window
    root.destroy()

    return file_path

if __name__ == "__main__":
    # Test the function if run directly
    selected = select_file()
    if selected:
        print("Selected file:", selected)
    else:
        print("No file selected")
