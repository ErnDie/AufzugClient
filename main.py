#! /usr/bin/env python3

import json
import os
import subprocess
import sys
from asyncio import run
from datetime import datetime
from functools import partial
from typing import Dict
from elevator import Elevator, elevator
from model_logic import evaluateActuators
from crosslab.soa_services.electrical import ElectricalConnectionService
from crosslab.soa_services.electrical.messages import State
from crosslab.soa_services.electrical.signal_interfaces.gpio import ConstractableGPIOInterface, GPIOInterface, \
    GPIOSignalChangeEventData
from crosslab.soa_services.file import FileService__Consumer, FileServiceEvent, FileService__Producer
from crosslab.soa_services.webcam import WebcamService__Producer, GstTrack

import asyncio

from crosslab.api_client import APIClient
from crosslab.soa_client.device_handler import DeviceHandler
from crosslab.soa_services.message import MessageService__Producer, MessageService__Consumer

interfaces: Dict[str, GPIOInterface] = dict()

actuators_names = [
    "FloorZero",
    "FloorOne",
    "FloorTwo",
    "FloorThree",
    "FloorFour",
    "FloorFive",
    "FloorSix",
    "FloorSeven",
    "FloorEight",
    "FloorNine",
    "FloorTen",
    "FloorEleven"
]


def tmp(name):
    print(name)
    interfaces[name].changeDriver("strongH")


async def main_async():
    # read config from file
    with open("config.json", "r") as configfile:
        conf = json.load(configfile)

    # debug; delete for prod
    print(conf)
    elevator = Elevator()
    deviceHandler = DeviceHandler()

    # Webcam Service
    # pipeline = (" ! ").join(
    #    [
    #        "v4l2src device=/dev/video0",
    #        "'image/jpeg,width=640,height=480,framerate=30/1'",
    #        "v4l2jpegdec",
    #        "v4l2h264enc",
    #        "'video/x-h264,level=(string)4'",
    #    ])
    # webcamService = WebcamService__Producer(GstTrack(pipeline), "webcam")
    # deviceHandler.add_service(webcamService)

    def newInterface(interface):
        if isinstance(interface, GPIOInterface):
            name: str = interface.configuration["signals"]["gpio"]
            interfaces[name] = interface
            interface.on(
                "signalChange",
                lambda event: (
                    handleAnswer(name)
                )
            )

    def handleAnswer(name):
        print(f"Handling answer for {name}")
        if name != "FloorEleven":
            evaluateActuators(interfaces, elevator, name)
            print(interfaces["FloorEleven"].signalState)
            interfaces["FloorEleven"].changeDriver("strongH")


    # E Service
    actuators_service = ElectricalConnectionService("actuators")
    actuators_interface = ConstractableGPIOInterface(actuators_names, "inout")
    actuators_service.addInterface(actuators_interface)
    actuators_service.on("newInterface", newInterface)
    deviceHandler.add_service(actuators_service)

    url = conf["auth"]["deviceURL"]

    async with APIClient(url) as client:
        client.set_auth_token(conf["auth"]["deviceAuthToken"])
        deviceHandlerTask = asyncio.create_task(
            deviceHandler.connect("{url}/devices/{did}".format(
                url=conf["auth"]["deviceURL"],
                did=conf["auth"]["deviceID"]
            ), client)
        )

        await deviceHandlerTask


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
