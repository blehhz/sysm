import os
import psutil
import platform
import socket
from pathlib import Path

# desktop management interface info like computer's hardware and system manufacturer through firmware (BIOS/UEFI)
def get_dmi_info(key):
    path = Path("/sys/class/dmi/id") / key

    try:
        data = path.read_text().strip()
        return data if data else None
    except(FileNotFoundError, PermissionError, OSError):
        return None

def get_dmi_system_info():
    return {
        'manufacturer' : get_dmi_info("sys_vendor"),
        'product_name' : get_dmi_info("product_name"),
        'version' : get_dmi_info("product_version"),
        'serial_number' : get_dmi_info("product_serial") 
    }

def get_dmi_bios_info():
    return {
        'vendor' : get_dmi_info("bios_vendor"),
        'version' : get_dmi_info("bios_version"),
        'release_date' : get_dmi_info("bios_date"),
    }

def get_dmi_chassis_info():
    return {
        'vendor' : get_dmi_info("chassis_vendor"),
        'version' : get_dmi_info("chassis_version"),
        'serial_number' : get_dmi_info("chassis_serial")
    }

def get_kernel_info():
    return {
        "name": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "processor": platform.processor()
    }

def get_os_info():
    return {
        key.lower(): value
        for key, value in platform.freedesktop_os_release().items()
    }

def get_cpu_info():
    cpu_details = {}

    try:
        with open("/proc/cpuinfo", "r") as file:
            for line in file:
                if ":" in line:
                    key, value = line.split(":", 1)
                    cpu_details[key.strip()] = value.strip()

                if not line.strip():
                    break
    except OSError:
        pass

    freq = psutil.cpu_freq()

    return {
        "vendor_id": cpu_details.get("vendor_id"),
        "model_name": cpu_details.get("model name"),
        "architecture": platform.machine(),
        "cache_size": cpu_details.get("cache size"),
        "flags": cpu_details.get("flags", "").split(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "frequency": {
            "current_mhz": freq.current if freq else None,
            "min_mhz": freq.min if freq else None,
            "max_mhz": freq.max if freq else None,
        }
    }

def get_memory_devices():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "free": memory.free,
        "usage_percent": memory.percent,
        "swap": {
            "total": swap.total,
            "used": swap.used,
            "free": swap.free,
            "usage_percent": swap.percent
        }
    }

def get_storage_devices():
    devices = []

    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            devices.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "usage_percent": usage.percent
            })
        except (PermissionError, OSError):
            continue

    return devices

def get_system_info():
    return {
        'cpu_info' : get_cpu_info(),
        'kernel_info' : get_kernel_info(),
        'os_info' : get_os_info(),
        'memory_devices' : get_memory_devices(),
        'storage_devices' : get_storage_devices(),
        'dmi' : {
            'system_info' : get_dmi_system_info(),
            'bios_info' : get_dmi_bios_info(),
            'chassis_info' : get_dmi_chassis_info()
        }
    }