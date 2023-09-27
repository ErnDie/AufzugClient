import requests

ipArduino = "192.168.2.199"


class FloorModel:
    def __init__(self, name, currentFloor, floor):
        self.Name = name
        self.IsCurrentFloor = currentFloor
        self.Floor = floor


class Elevator:
    def __init__(self) -> None:
        self.FloorZero = FloorModel("FloorZero", True, 0)
        self.FloorOne = FloorModel("FloorOne", False, 1)
        self.FloorTwo = FloorModel("FloorTwo", False, 2)
        self.FloorThree = FloorModel("FloorThree", False, 3)
        self.FloorFour = FloorModel("FloorFour", False, 4)
        self.FloorFive = FloorModel("FloorFive", False, 5)
        self.FloorSix = FloorModel("FloorSix", False, 6)
        self.FloorSeven = FloorModel("FloorSeven", False, 7)
        self.FloorEight = FloorModel("FloorEight", False, 8)
        self.FloorNine = FloorModel("FloorNine", False, 9)
        self.FloorTen = FloorModel("FloorTen", False, 10)
        self.FloorEleven = FloorModel("FloorEleven", False, 11)
        self.CurrentFloor = self.FloorZero

    def GetFloorObject(self, name):
        if self.FloorZero.Name == name:
            return self.FloorZero
        if self.FloorOne.Name == name:
            return self.FloorOne
        if self.FloorTwo.Name == name:
            return self.FloorTwo
        if self.FloorThree.Name == name:
            return self.FloorThree
        if self.FloorFour.Name == name:
            return self.FloorFour
        if self.FloorFive.Name == name:
            return self.FloorFive
        if self.FloorSix.Name == name:
            return self.FloorSix
        if self.FloorSeven.Name == name:
            return self.FloorSeven
        if self.FloorEight.Name == name:
            return self.FloorEight
        if self.FloorNine.Name == name:
            return self.FloorNine
        if self.FloorTen.Name == name:
            return self.FloorTen
        if self.FloorEleven.Name == name:
            return self.FloorEleven

    def driveTofloor(self, floor: FloorModel):
        print(f"Driving to floor {floor.Floor}")
        requests.get(f"http://{ipArduino}/goToEtage?params=1&{floor.Floor}")


elevator: Elevator = None
