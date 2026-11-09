import numpy as np

from ship_floor_plan.dataset import RPlanDataset


def balance_index(arr):
    cumsum = np.cumsum(arr)
    total = cumsum[-1]

    # For each index i: left = sum(arr[:i]), right = sum(arr[i+1:])
    left = cumsum - arr
    right = total - cumsum

    return int(np.argmin(np.abs(left - right)))


class CenterMassCalculator:
    def __init__(self):
        pass


class RPlanCenterOfMass(CenterMassCalculator):
    def __init__(self, data, wall_mass=1.0, door_mass=0.5, door_length=4, floor_mass=0.5):
        super().__init__()

        self.data = data

        boundaries = self.data["boundary"]
        boundaries.append(boundaries[0])
        x_top = x_bottom = boundaries[0][0]
        y_top = y_bottom = boundaries[0][1]
        for k in range(1, len(boundaries)):
            x0, y0 = boundaries[k-1][0], boundaries[k-1][1]
            x0, y0 = boundaries[k][0], boundaries[k][1]
            if x0 < x_top:
                x_top = x0
            if y0 < y_top:
                y_top = y0
            if x0 > x_bottom:
                x_bottom = x0
            if y0 > y_bottom:
                y_bottom = y0
        # bounding_box = [x_top, y_top, x_bottom, y_bottom]

        masses = [[0 for _ in range(x_bottom+1)] for _ in range(y_bottom+1)] # a list where each list is a row, and each number within that list is a column, sizes defined by the bounding box

        for room in data["rooms"]:
            # print(room["id"])

            # set weight of floors
            box = room["box"]
            for k in range(box[0], box[2]):
                for i in range(box[1], box[3]):
                    try:
                        masses[i][k] = floor_mass
                    except IndexError:
                        print("i=", i, "k=", k)
                        raise IndexError

            for k in range(1, len(room["r_boundary"])):
                x0 = room["r_boundary"][k-1][0]
                y0 = room["r_boundary"][k-1][1]
                x1 = room["r_boundary"][k][0]
                y1 = room["r_boundary"][k][1]
                if x0 > x1:
                    x0, x1 = x1, x0
                if y0 > y1:
                    y0, y1 = y1, y0
                for y in range(y0, y1+1):
                    for x in range(x0, x1+1):
                        masses[y][x] = wall_mass
            x0 = room["r_boundary"][-1][0]
            y0 = room["r_boundary"][-1][1]
            x1 = room["r_boundary"][0][0]
            y1 = room["r_boundary"][0][1]
            if x0 > x1:
                x0, x1 = x1, x0
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1+1):
                for x in range(x0, x1+1):
                    masses[y][x] = wall_mass

        # for k in masses:
        #     for i in k:
        #         print(i, end="")
        #     print()

        masses = np.array(masses)
        y_average = np.average(masses, axis=0) # average weight across all rows for each column
        x_average = np.average(masses, axis=1) # average weight across all columns for each row

        self.x = balance_index(y_average) # x coordinate gained from the average weight per column
        self.y = balance_index(x_average) # y coordinate gained from the average weight per row


if __name__ == "__main__":
    path = "./rplan/dataset_json/data_test.json"
    dataset = RPlanDataset(path)

    index = 5
    calculator = RPlanCenterOfMass(dataset.data[index])
    print(calculator.x, calculator.y)