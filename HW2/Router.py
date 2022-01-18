

MAX_INT = 2**31 - 1


class Router():
    def __init__(self, neighboures, node_num) -> None:
        self.node_num = node_num
        # neightboures : array of tuples in the form of (node number , node distance)
        self.neighboures = neighboures
        # init empty table
        self.table = [[MAX_INT, MAX_INT, MAX_INT, MAX_INT]
                      for _ in list(range(len(neighboures)+1))]
        self.updated = False
        self.table[node_num][node_num] = 0
        self.routers = []
        for i in neighboures:
            self.table[node_num][i[0]] = i[1]

    def __str__(self) -> str:
        print("neighboures:", self.neighboures, "\n", "table:", self.table)

    def print_table(self):
        for t in self.table:
            print(t)

    def receive_event(self, packet):
        print("event received", self.node_num)
        self.rtUpdate(packet)

    def rtUpdate(self, packet):
        self.changed = False
        received_packet = packet[1]
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if self.table[i][j] > received_packet[i][j]:
                    self.table[i][j] = received_packet[i][j]
                    self.changed = True
        for i in range(len(self.table)):
            dist = Router.get_min_dist(
                self.node_num, i, set(), self.table, self.neighboures)
            if(self.table[self.node_num][i] > dist):
                self.table[self.node_num][i] = dist
                self.changed = True

        if self.changed == True:
            self.toLayer2()

    def toLayer2(self):
        packet = (self.node_num, self.table)
        for n in self.neighboures:
            self.routers[n[0]].receive_event(packet)

    def get_min_dist(src, dest, seen_nodes, table, neighboures):
        if src == dest:
            return 0
        min_dist = MAX_INT
        for n in neighboures:
            if n[0] in seen_nodes:
                continue
            seen_nodes.add(src)
            new_neighbours = Router.get_neighbours(table, n[0])
            cost = table[src][n[0]] + Router.get_min_dist(
                n[0], dest, seen_nodes, table, new_neighbours)
            seen_nodes.remove(src)
            if cost < min_dist:
                min_dist = cost
        return min_dist

    def get_neighbours(table, src):
        n = []
        for i in range(len(table[src])):
            if table[src][i] == MAX_INT or i == src:
                continue
            neighbour = (i, table[src][i])
            n.append(neighbour)
        return n
