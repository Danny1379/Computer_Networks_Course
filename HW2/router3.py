from Router import Router
MAX_INT = 2**31 - 1

NEIGHBORS = {(0, 7), (1, MAX_INT), (2, 2)}  # (node , cost)


def rtinit3():
    router = Router(NEIGHBORS, 3)
    print(f"table{router.node_num}", "initialized")
    router.print_table()
    return router
