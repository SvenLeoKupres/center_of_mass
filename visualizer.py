import tkinter as tk
from enum import Enum
from queue import PriorityQueue

from center_of_mass import RPlanCenterOfMass, CenterMassCalculator
from colision_detection import check_within_bounds
from dataset import RPlanDataset, Dataset


class RoomCategory (Enum):
    LIVING_ROOM=0,
    BEDROOM=1,
    KITCHEN=2,
    BATHROOM=3,
    BALCONY=4,
    STORAGE=5

    @staticmethod
    def categorize(num:int) -> "RoomCategory":
        if num==0:
            return RoomCategory.LIVING_ROOM
        elif num==1:
            return RoomCategory.BEDROOM
        elif num==2:
            return RoomCategory.KITCHEN
        elif num==3:
            return RoomCategory.BATHROOM
        elif num==4:
            return RoomCategory.BALCONY
        elif num==5:
            return RoomCategory.STORAGE
        else:
            raise ValueError

    def color(self):
        if self.name == "LIVING_ROOM":
            return "green"
        elif self.name == "BEDROOM":
            return "yellow"
        elif self.name == "KITCHEN":
            return "red"
        elif self.name == "BATHROOM":
            return "blue"
        elif self.name == "BALCONY":
            return "purple"
        elif self.name == "STORAGE":
            return "orange"
        return None


class Window(tk.Tk):
    def __init__(self, dataset:Dataset, calculator:CenterMassCalculator, index=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.geometry("300x300")

        self.dataset = dataset
        self.index = index
        self.data = self.dataset.data[index]

        self.canvas = tk.Canvas(self)

        boundaries = self.data["boundary"]
        boundaries.append(boundaries[0])
        x_top = x_bottom = boundaries[0][0]
        y_top = y_bottom = boundaries[0][1]
        for k in range(1, len(boundaries)):
            x0, y0 = boundaries[k - 1][0], boundaries[k - 1][1]
            x1, y1 = boundaries[k][0], boundaries[k][1]
            # self.canvas.create_line(x0, y0, x1, y1, width=3)
            if x0 < x_top:
                x_top = x0
            if y0 < y_top:
                y_top = y0
            if x1 > x_bottom:
                x_bottom = x1
            if y1 > y_bottom:
                y_bottom = y1
        # x0, y0 = boundaries[-1][0], boundaries[-1][1]
        # x1, y1 = boundaries[0][0], boundaries[0][1]
        # self.canvas.create_line(x0, y0, x1, y1, width=3)
        # self.canvas.create_rectangle(x_top, y_top, x_bottom, y_bottom)
        geometric_x = (x_top+x_bottom)/2
        geometric_y = (y_top+y_bottom)/2

        priority_queue = PriorityQueue()
        for k in range(len(self.data["rooms"])):
            room = self.data["rooms"][k]
            check_within_bounds(boundaries, room)
            priority_queue.put((room["order"], room))

        while not priority_queue.empty():
            room = priority_queue.get()[1]
            room_category = RoomCategory.categorize(room["category"])
            self.canvas.create_rectangle(room["box"][0], room["box"][1], room["box"][2], room["box"][3], fill=room_category.color(), outline=room_category.color())
            # center = room["location"]
            # self.canvas.create_oval(center[0], center[1], center[0], center[1], fill="black")
            boundary = room["r_boundary"]
            for k in range(1, len(boundary)):
                p1 = boundary[k - 1]
                p2 = boundary[k]
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2)
                # room = self.data["rooms"][k]
            p1 = boundary[0]
            p2 = boundary[-1]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2)

        self.canvas.create_oval(calculator.x, calculator.y, calculator.x, calculator.y)
        self.canvas.create_oval(geometric_x, geometric_y, geometric_x, geometric_y, fill="orange", outline="orange")
        distance = ((geometric_x-calculator.x)**2+(geometric_y-calculator.y)**2)**0.5
        print("Euclidean distance between center of mass and bounding box center:", distance)

        self.canvas.pack()

if __name__=="__main__":
    path = "./rplan/dataset_json/data_test.json"
    dataset = RPlanDataset(path)

    index = 46

    calculator = RPlanCenterOfMass(dataset.data[index])
    window = Window(dataset, calculator, index)
    window.mainloop()