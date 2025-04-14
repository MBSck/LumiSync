import json
import socket
import sys
import time
from typing import Any, Dict, List

import colorama

from .config.options import CONNECTION


def start() -> Dict[str, Any]:
    request()
    print(f"{colorama.Fore.YELLOW}Trying to find device...")
    data = listen()
    print(f"{colorama.Fore.GREEN}Device found!")
    settings = parseMessages(data)
    writeJSON(settings)
    return settings


def request() -> None:
    """Requests data from the devices in the network."""
    data = {"msg": {"cmd": "scan", "data": {"account_topic": "reserve"}}}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(
        bytes(json.dumps(data), "utf-8"),
        (CONNECTION.default.multicast, CONNECTION.default.port),
    )


def listen() -> List[str]:
    """Listens in the network to find devices."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    sock.bind(("", CONNECTION.default.listen_port))
    messages = []
    try:
        while True:
            message, address = sock.recvfrom(1024)
            print(f"{colorama.Fore.LIGHTGREEN_EX}Received message from: ", address)
            messages.append(message)
    except socket.timeout:
        if len(messages) == 0:
            print(f"{colorama.Fore.RED}Error: No device found!")
            sys.exit()
    return messages


def parseMessages(messages: List[str]) -> Dict[str, Any]:
    """Parses messages received from the devices."""
    try:
        with open("Settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"time": time.time(), "devices": [], "selectedDevice": 0}

    # NOTE: Ensure the settings dictionary has the 'devices' and 'selectedDevice' keys
    if "devices" not in settings:
        settings["devices"] = []
    if "selectedDevice" not in settings:
        settings["selectedDevice"] = 0

    for deviceJson in messages:
        device = json.loads(deviceJson)
        existingDevice = next(
            (
                x
                for x in settings["devices"]
                if x["MAC"] == device["msg"]["data"]["device"]
            ),
            None,
        )
        if existingDevice is None:
            data = {
                "MAC": device["msg"]["data"]["device"],
                "Model": device["msg"]["data"]["sku"],
                "Device_IP": device["msg"]["data"]["ip"],
                "Device_Port": 4003,
            }
            settings["devices"].append(data)
        else:
            existingDevice["Device_IP"] = device["msg"]["data"]["ip"]
    settings["time"] = time.time()
    return settings


def writeJSON(settings: Dict[str, Any]) -> None:
    """Writes a .json file."""
    with open("settings.json", "w") as f:
        json.dump(settings, f)
    print(f"{colorama.Fore.LIGHTGREEN_EX}Data written to Settings.json")
