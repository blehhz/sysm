import os
import psutil
import platform
import socket
from pathlib import Path


def get_dmi_info(key):
    path = Path("/sys/class/dmi/id") / key
    
    return path.read_text().strip()


platformInfo = platform.freedesktop_os_release()
osName = f"{platformInfo["PRETTY_NAME"]} {platform.machine()}"
host = f"{get_dmi_info("product_name")} ({get_dmi_info("product_version")})" 
kernel = f"{platform.system()} {platform.release()}"

print(f"OS: {osName}")
print(f"Host: {host}")
print(f"Kernel: {kernel}")