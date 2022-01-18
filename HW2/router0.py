from Router import Router
MAX_INT = 2**31 - 1

NEIGHBORS = {(1, 1), (2, 3), (3, 7)}  # (node , cost)


def rtinit0():
    router = Router(NEIGHBORS, 0)
    print(f"table{router.node_num}", "initialized")
    router.print_table()
    return router
