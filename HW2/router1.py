from Router import MAX_INT, Router


NEIGHBORS = {(0, 1), (2, 1), (3, MAX_INT)}  # (node , cost)


def rtinit0():
    router = Router(neighboures=NEIGHBORS)


def rtupdate0(rcvdpkt):
    pass
