from Router import Router
from router0 import rtinit0
from router1 import rtinit1
from router2 import rtinit2
from router3 import rtinit3
routers = []

if __name__ == "__main__":

    routers.append(rtinit0())
    routers.append(rtinit1())
    routers.append(rtinit2())
    routers.append(rtinit3())
    for r in routers:
        r.routers = routers
    r0 = routers[0]
    r0.toLayer2()
    r0.print_table()
