from Router import Router
MAX_INT = 2**31 - 1

NEIGHBORS = {(0, 3), (1, 1), (3, 2)}  # (node , cost)


def rtinit2():
    router = Router(NEIGHBORS, 2)
    print(f"table{router.node_num}", "initialized")
    router.print_table()
    return router
