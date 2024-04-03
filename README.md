# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1

Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

AmountIns:

```
4.999999 5.655321 2.458781 5.088927 20.129888 1.335903 3.034864 4.310946 2.404817
```

AmountOuts:

```
5.655321 2.458781 5.088927 20.129888 1.335903 3.034864 4.310946 2.404817 26.639970
```

## Problem 2

What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

Slippage refers to the difference between the expected price of a trade and the actual price at which the trade is executed. This discrepancy is primarily due to the impact of the trades in the pool.

Uniswap V2 addresses slippage by utilizing a constant product formula to maintain a balanced liquidity pool: $x\cdot y = k$.

## Problem 3

Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

## Problem 4

Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

## Problem 5

What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

In a sandwich attack, a malicious actor exploits the predictability of price movements at the expense of other traders. Here's how a sandwich attack typically works:

1. **Monitoring Transactions**: The attacker monitors the blockchain for pending transactions related to a specific trading pair.
2. **Front-Running**: When the attacker detects a large trade about to occur, they quickly execute two transactions:

- First, they place a large trade in the same direction as the impending large trade. This causes the price to move unfavorably for the victim.

- Then, they place another trade immediately after the victim's trade, profiting from the price movement caused by the victim's trade.
  Profit: The attacker profits from the price movement they caused by effectively "sandwiching" the victim's trade between their own trades.

3. Profit: The attacker profits from the price movement they caused by effectively "sandwiching" the victim's trade between their own trades.

The impact of a sandwich attack on an individual initiating a swap can be significant:

1. **Increased Slippage**: The victim experiences higher slippage, meaning they get a worse price for their trade due to the artificial price movement caused by the attacker's trades.

2. **Reduced Profit**: The victim's intended profit or loss may be affected due to the altered market conditions caused by the sandwich attack.

3. **Loss of Funds**: In extreme cases, the victim may lose a significant portion of their funds if the price movement caused by the attack is substantial.
