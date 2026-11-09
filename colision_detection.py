class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, p1:Point, p2:Point):
        self.p1 = p1
        self.p2 = p2

    def bounding_box(self):
        box = []
        if self.p1.x < self.p2.x:
            box.append(self.p1.x)
            x = self.p2.x
        else:
            box.append(self.p2.x)
            x = self.p1.x
        if self.p1.y < self.p2.y:
            box.append(self.p1.y)
            y = self.p2.y
        else:
            box.append(self.p2.y)
            y = self.p1.y
        box.append(x)
        box.append(y)

        return box

    def implicit_form(self) -> list:
        """
        :return: a list with 3 numbers: a, b and c, such that ax+by+c=0 for each point (x,y) on this line
        """
        a = self.p1.x - self.p2.x
        b = self.p2.y - self.p1.y
        c = -a * self.p1.y - b * self.p1.x

        return [a, b, c]

    def __str__(self):
        return str(self.p1) + ", " + str(self.p2)

    def __contains__(self, item):
        return item == self.p1 or item == self.p2


def check_crossing_edges(edge1:Line, edge2:Line) -> Point | None:
    """
    Check if two edges are intersecting
    :param edge1: a list of 2 points, each with 2 coordinates
    :param edge2: a list of 2 points, each with 2 coordinates
    :return: The point of intersection if it exists, otherwise None
    """
    form1 = edge1.implicit_form()
    form2 = edge2.implicit_form()

    denominator = form1[0]*form2[1]-form2[0]*form1[1]

    if denominator == 0: # if parallel
        return None

    y = (form1[1]*form2[2] - form2[1]*form1[2])/denominator
    x = (form2[0]*form1[2] - form1[0]*form2[2])/denominator

    box = edge1.bounding_box()
    if x<box[0] or x>box[2] or y<box[1] or y>box[3]:
        return None
    box = edge2.bounding_box()
    if x < box[0] or x > box[2] or y < box[1] or y > box[3]:
        return None

    point = Point(x, y)
    if point in edge1 or point in edge2:
        return None

    return Point(x, y)


def check_within_bounds(boundaries, room):
    room_bounds = []
    room_box = room["box"]
    point1 = [room_box[0], room_box[1]]
    point2 = [room_box[2], room_box[1]]
    point3 = [room_box[2], room_box[3]]
    point4 = [room_box[0], room_box[3]]
    room_bounds.append([point1, point2])
    room_bounds.append([point2, point3])
    room_bounds.append([point3, point4])
    room_bounds.append([point4, point1])
    print("Room id:", room["id"])
    for k in room_bounds:
        line = Line(Point(k[0][0], k[0][1]), Point(k[1][0], k[0][1]))
        for i in range(1, len(boundaries)):
            p1 = Point(boundaries[i-1][0], boundaries[i-1][1])
            p2 = Point(boundaries[i][0], boundaries[i][1])
            boundary = Line(p1, p2)
            res = check_crossing_edges(boundary, line)
            if res is not None:
                print("Lines ", line, "and", boundary, "meet at", res)
                # print(res)