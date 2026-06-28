import os
import shutil
import keyboard
import pyautogui
import winsound  # Native Windows sound library
from PIL import Image
from datetime import datetime

# Folder configuration
IMAGE_FOLDER = "captured_images"
HISTORY_FOLDER = "history"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(HISTORY_FOLDER, exist_ok=True)

print("Program running...")
print("Press F10 to take a screenshot.")
print("Press F11 to create a PDF (archives previous PDF to history).")
print("Press ESC to exit the program.")

def play_sound_f10():
    # A short, higher-pitched beep for screenshots (Frequency, Duration in ms)
    winsound.Beep(2000, 100)

def play_sound_f11():
    # A two-tone success chime for PDF generation
    winsound.Beep(1500, 150)
    winsound.Beep(2500, 250)

def take_screenshot():
    # Generate a unique filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    filename = os.path.join(IMAGE_FOLDER, f"screenshot_{timestamp}.png")
    
    # Take and save the screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")
    
    # Play F10 sound
    play_sound_f10()

def create_pdf():
    # 1. Check if there are screenshots to process
    files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.png')]
    if not files:
        print("No screenshots found to make a PDF!")
        return
    
    # 2. Move any existing PDFs in the root folder to the history folder
    root_files = os.listdir('.')
    for file in root_files:
        if file.startswith('compiled_screenshots_') and file.endswith('.pdf'):
            old_pdf_path = os.path.join('.', file)
            new_pdf_path = os.path.join(HISTORY_FOLDER, file)
            try:
                shutil.move(old_pdf_path, new_pdf_path)
                print(f"Moved previous PDF '{file}' to history folder.")
            except Exception as e:
                print(f"Could not move existing PDF: {e}")

    # 3. Sort images to ensure chronological order
    files.sort() 
    
    # Open images and convert them to RGB
    image_list = []
    for file in files:
        img_path = os.path.join(IMAGE_FOLDER, file)
        img = Image.open(img_path).convert('RGB')
        image_list.append(img)
    
    # 4. Save as a single PDF at the root level
    pdf_filename = f"compiled_screenshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    image_list[0].save(pdf_filename, save_all=True, format="PDF", append_images=image_list[1:])
    print(f"\nSUCCESS: PDF created as './{pdf_filename}'")
    
    # 5. Clean up temporary images
    for img in image_list:
        img.close()
        
    for file in files:
        os.remove(os.path.join(IMAGE_FOLDER, file))
    print("Temporary images deleted clean.")
    
    # Play F11 success sound
    play_sound_f11()

# Set up the hotkeys
keyboard.add_hotkey('f10', take_screenshot)
keyboard.add_hotkey('f11', create_pdf)

# Keep the program running until you press ESC
keyboard.wait('esc')
