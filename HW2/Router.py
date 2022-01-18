MAX_INT = 2*31 - 1


class Router():
    def __init__(self, neighboures) -> None:
        # neightboures : array of tuples in the form of (node number , node distance)
        self.neighboures = neighboures
        # init empty table
        self.table = [[MAX_INT, MAX_INT, MAX_INT]
                      for x in list(range(len(neighboures)))]
