from Router import Router


NEIGHBORS = {(1, 1), (2, 3), (3, 7)}  # (node , cost)


def rtinit0():
    router = Router(neighboures=NEIGHBORS)
    router.__str__()


def rtupdate0(rcvdpkt):
    pass
