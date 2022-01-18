from Router import Router
MAX_INT = 2**31 - 1

NEIGHBORS = {(0, 1), (2, 1), (3, MAX_INT)}  # (node , cost)


def rtinit1():
    router = Router(NEIGHBORS, 1)
    print(f"table{router.node_num}", "initialized")
    router.print_table()
    return router
