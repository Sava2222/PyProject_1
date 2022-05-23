import Room


class Area:
    room_coordinates = [(43, 350), (43, 36), (821, 36), (821, 350)]

    def __init__(self, area_type):
        self.area_type = area_type
        self.rooms = [Room.Room(self.room_coordinates[i]) for i in range(0, 4)]
