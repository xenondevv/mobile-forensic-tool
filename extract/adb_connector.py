import subprocess
import os

OUTPUT_DIR = "./output"

def check_device_connected():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    return "device" in result.stdout

def pull_photos():
    subprocess.run(["adb", "pull", "/sdcard/DCIM/Camera", f"{OUTPUT_DIR}/photos"])

def pull_whatsapp_media():
    subprocess.run(["adb", "pull", "/sdcard/WhatsApp/Media", f"{OUTPUT_DIR}/whatsapp"])
