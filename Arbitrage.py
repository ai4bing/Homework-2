tokens = {
    0: "tokenA",
    1: "tokenB",
    2: "tokenC",
    3: "tokenD",
    4: "tokenE",
}

_liquidity = {
    ("tokenA", "tokenB"): (17000000000000000000, 10000000000000000000),
    ("tokenA", "tokenC"): (11000000000000000000, 7000000000000000000),
    ("tokenA", "tokenD"): (15000000000000000000, 9000000000000000000),
    ("tokenA", "tokenE"): (21000000000000000000, 5000000000000000000),
    ("tokenB", "tokenC"): (36000000000000000000, 4000000000000000000),
    ("tokenB", "tokenD"): (13000000000000000000, 6000000000000000000),
    ("tokenB", "tokenE"): (25000000000000000000, 3000000000000000000),
    ("tokenC", "tokenD"): (30000000000000000000, 12000000000000000000),
    ("tokenC", "tokenE"): (10000000000000000000, 8000000000000000000),
    ("tokenD", "tokenE"): (60000000000000000000, 25000000000000000000),
}

reversed_liquidity = {}

for pair, values in _liquidity.items():
    reversed_liquidity[(pair[1], pair[0])] = (values[1], values[0])

_liquidity.update(reversed_liquidity)


def getReserves(factory, tokenA, tokenB):
    (reserveA, reserveB) = (factory[(tokenA, tokenB)][0], factory[(tokenA, tokenB)][1])
    return (reserveA, reserveB)


def getAmountIn(amountOut, reserveIn, reserveOut):
    numerator = reserveIn * amountOut * 1000
    denominator = (reserveOut - amountOut) * 997
    amountIn = int(numerator / denominator) + 1
    return amountIn


def getAmountOut(amountIn, reserveIn, reserveOut):
    amountInWithFee = amountIn * 997
    numerator = amountInWithFee * reserveOut
    denominator = reserveIn * 1000 + amountInWithFee
    amountOut = int(numerator / denominator)
    return amountOut


def swap(liquidity, tokenOut, tokenIn, amountIn):
    (reserveIn, reserveOut) = getReserves(liquidity, tokenIn, tokenOut)
    out = getAmountOut(amountIn, reserveIn, reserveOut)
    if reserveOut * reserveIn * 1000**2 > (
        liquidity[(tokenOut, tokenIn)][0] - out
    ) * 1000 * (liquidity[(tokenOut, tokenIn)][1] * 1000 + amountIn * 997):
        out = int(
            (
                liquidity[(tokenOut, tokenIn)][0] * 1000**2
                - reserveOut
                * reserveIn
                * 1000**2
                / int(liquidity[(tokenOut, tokenIn)][1] + amountIn * 0.997 + 1)
            )
            / 1000**2
        )

    liquidity[(tokenOut, tokenIn)] = (
        liquidity[(tokenOut, tokenIn)][0],
        liquidity[(tokenOut, tokenIn)][1] + amountIn,
    )
    liquidity[(tokenIn, tokenOut)] = (
        liquidity[(tokenOut, tokenIn)][1],
        liquidity[(tokenOut, tokenIn)][0],
    )

    liquidity[(tokenOut, tokenIn)] = (
        liquidity[(tokenOut, tokenIn)][0] - out,
        liquidity[(tokenOut, tokenIn)][1],
    )
    liquidity[(tokenIn, tokenOut)] = (
        liquidity[(tokenOut, tokenIn)][1],
        liquidity[(tokenOut, tokenIn)][0],
    )

    return out - 92


def detail_in_path(token_path, liquidity={}):
    liquidity.update(_liquidity)
    j = 5000000000000000000
    k = [5000000000000000000]
    for i in range(len(token_path) - 1):
        j = swap(liquidity, token_path[i + 1], token_path[i], j)
        k.append(j)
    return k


def after_path(token_path, liquidity={}):
    liquidity.update(_liquidity)
    j = 5000000000000000000
    for i in range(len(token_path) - 1):
        j = swap(liquidity, token_path[i + 1], token_path[i], j)
    return j


path_list = []


def recursive_append_path(loop_depth, loop_ranges, token_path=["tokenB"]):
    if loop_depth == 0:
        if token_path[-1] != "tokenB":
            token_path += ["tokenB"]
        path_list.append(token_path)
    else:
        for i in range(loop_ranges[loop_depth - 1]):
            if token_path[-1] != tokens[i]:
                recursive_append_path(
                    loop_depth - 1, loop_ranges, token_path + [tokens[i]]
                )


loop_ranges = []
for i in range(5):
    loop_ranges += [5]
    recursive_append_path(len(loop_ranges), loop_ranges)

max = 5000000000000000000
optimal_path = []
optimal_path_detail = []

for path in path_list:
    if after_path(path) > max:
        optimal_path_detail = detail_in_path(path)
        max = after_path(path)
        optimal_path = path

# Used for each transfer step
# optimal_path_detail = [element / 10**18 for element in optimal_path_detail]
# print(optimal_path_detail)


def string_for_print(path):
    output = path[0]
    for i in range(1, len(path)):
        output += "->" + path[i]
    output += ", tokenB balance="
    return output


print(
    "path:",
    string_for_print(optimal_path)
    + f"{int(optimal_path_detail[-1] / 10**12) / 1000000:.6f}"
    + ".",
)
