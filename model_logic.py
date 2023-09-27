from typing import Dict
from elevator import Elevator
from crosslab.soa_services.electrical.signal_interfaces.gpio import GPIOInterface
from crosslab.soa_services.electrical.messages import State


def isHigh(value: State):
    return value in ["strongH", "weakH"]


def evaluateActuators(
        interfaces: Dict[str, GPIOInterface],
        elevator: Elevator,
        name
):
    print("evaluating actuators")
    print(elevator.CurrentFloor.Name)
    print(elevator.CurrentFloor.IsCurrentFloor)

    if elevator.CurrentFloor.Name != name:
        newFloorInterface = interfaces.get(name, None)
        if isHigh(newFloorInterface.signalState):
            oldElevatorName = elevator.CurrentFloor.Name
            elevator.CurrentFloor.IsCurrentFloor = False
            elevator.CurrentFloor = elevator.GetFloorObject(name)
            elevator.CurrentFloor.IsCurrentFloor = True
            elevator.driveTofloor(elevator.CurrentFloor)
            interfaces[oldElevatorName].signalState = "strongL"
    else:
        print(f"Elevator is already on {name}")

