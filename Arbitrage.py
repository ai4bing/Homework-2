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
    return amountOut if (reserveOut > amountOut) else reserveOut


# def backAmountIn(betterAmountIn, out, reserveIn, reserveOut, length):
#     for k in range(length - 1, 0, -1):
#         a = getAmountIn(out[k], reserveIn[k], reserveOut[k])
#         reserveIn[k] += a - betterAmountIn[k]
#         reserveOut[k - 1] -= a - betterAmountIn[k]
#         betterAmountIn[k] = a
#         out[k - 1] = a


def swap(liquidity, path, amountIn):
    newliquidity = {}
    newliquidity.update(liquidity)
    tokenIn = path[:-1]
    tokenOut = path[1:]
    betterAmountIn = [amountIn] + [0] * (len(path) - 1)
    out, reserveIn, reserveOut = (
        [0] * (len(path) - 1),
        [0] * (len(path) - 1),
        [0] * (len(path) - 1),
    )
    for i in range(len(path) - 1):
        newliquidity.update(liquidity)
        for j in range(i):
            newliquidity[(tokenOut[j], tokenIn[j])] = (
                newliquidity[(tokenOut[j], tokenIn[j])][0] - out[j],
                newliquidity[(tokenOut[j], tokenIn[j])][1] + betterAmountIn[j],
            )
            newliquidity[(tokenIn[j], tokenOut[j])] = (
                newliquidity[(tokenOut[j], tokenIn[j])][1],
                newliquidity[(tokenOut[j], tokenIn[j])][0],
            )

            # print(
            #     newliquidity[(tokenIn[j], tokenOut[j])], (reserveIn[j], reserveOut[j])
            # )

            (reserveIn[j], reserveOut[j]) = getReserves(
                newliquidity, tokenIn[j], tokenOut[j]
            )

        (reserveIn[i], reserveOut[i]) = getReserves(
            newliquidity, tokenIn[i], tokenOut[i]
        )

        out[i] = getAmountOut(betterAmountIn[i], reserveIn[i], reserveOut[i])

        if reserveOut[i] * reserveIn[i] * 1000**2 > (
            reserveOut[i] - out[i]
        ) * 1000 * (reserveIn[i] * 1000 + betterAmountIn[i] * 997):
            out[i] = reserveOut[i] - int(
                (
                    reserveOut[i]
                    * reserveIn[i]
                    * 1000**2
                    / (reserveIn[i] * 1000 + betterAmountIn[i] * 997)
                    / 1000
                )
                + 1
            )

        # print(out[i], reserveOut[i])
        betterAmountIn[i] = getAmountIn(out[i], reserveIn[i], reserveOut[i])
        # backAmountIn(betterAmountIn, out, reserveIn, reserveOut, i)

        betterAmountIn[i + 1] = out[i]

        newliquidity[(tokenOut[i], tokenIn[i])] = (
            newliquidity[(tokenOut[i], tokenIn[i])][0] - out[i],
            newliquidity[(tokenOut[i], tokenIn[i])][1] + betterAmountIn[i],
        )
        newliquidity[(tokenIn[i], tokenOut[i])] = (
            newliquidity[(tokenOut[i], tokenIn[i])][1],
            newliquidity[(tokenOut[i], tokenIn[i])][0],
        )

    return betterAmountIn


def after_path(token_path, liquidity={}):
    liquidity.update(_liquidity)
    j = swap(liquidity, token_path, 5000000000000000000)
    return j


paths_list = []


def recursive_append_path(loop_depth, loop_ranges, token_path=["tokenB"]):
    if loop_depth == 0:
        if token_path[-1] != "tokenB":
            token_path += ["tokenB"]
        paths_list.append(token_path)
    else:
        for i in range(loop_ranges[loop_depth - 1]):
            if token_path[-1] != tokens[i]:
                recursive_append_path(
                    loop_depth - 1, loop_ranges, token_path + [tokens[i]]
                )


loop_ranges = []
for length in range(9):  # modify this for longer loops
    loop_ranges += [5]
    recursive_append_path(len(loop_ranges), loop_ranges)

max = 5000000000000000000
optimal_path = []
betterIn = []

for path in paths_list:
    betterAmountIn = after_path(path)
    if 5000000000000000000 + betterAmountIn[-1] - betterAmountIn[0] > max:
        max = 5000000000000000000 + betterAmountIn[-1] - betterAmountIn[0]
        optimal_path = path
        betterIn = betterAmountIn


def string_for_print(path):
    output = path[0]
    for i in range(1, len(path)):
        output += "->" + path[i]
    output += ", tokenB balance="
    return output


# for report 1
b = [int(x / 10**12) / 1000000 for x in betterIn]
for c in b:
    print(f"{c:.6f}")

print(
    "path:",
    string_for_print(optimal_path) + f"{int(max / 10**12) / 1000000:.6f}" + ".",
)
