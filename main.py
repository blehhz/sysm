from modules import system_info
import json

print(json.dumps(system_info.get_system_info(), indent=2))