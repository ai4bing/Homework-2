# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1

Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
>
> Output from Arbitrage.py:
> | path: | `tokenB->tokenA->tokenD->tokenC->tokenB->tokenE->tokenD->tokenC->tokenE->tokenB` |
> | - | - |
>
> | tokenB balance: | 26.639970 |
> | --------------- | --------- |
>
> | AmountIn  | AmountOut |
> | --------- | --------- |
> | 4.999999  | 5.655321  |
> | 5.655321  | 2.458781  |
> | 2.458781  | 5.088927  |
> | 5.088927  | 20.129888 |
> | 20.129888 | 1.335903  |
> | 1.335903  | 3.034864  |
> | 3.034864  | 4.310946  |
> | 4.310946  | 2.404817  |
> | 2.404817  | 26.639970 |

## Problem 2

What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution
>
> Slippage refers to the difference between the expected price of a trade and the actual price at which the trade is executed. This discrepancy is primarily due to the impact of the trades in the pool.
>
> Uniswap V2 addresses slippage by utilizing a constant product formula to maintain a balanced liquidity pool: $x\cdot y = k$.
>
> Let's take the question from midterm as an example. Say at the beginning, the pool has token pairs $(9,27000)$. Assuming no other fees are present, a $(3,0)$ amountIn can have $(0,27000-\frac{9\times 27000}{12})=(0,6750)$ as amountOut. But if someone else does this transaction in advance, the $(3,0)$ amountIn could only take $(0,20250-\frac{9\times 27000}{15})=(0,4050)$ as profit, the slippage is $(0,2700)$ in total.

## Problem 3

Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
>
> If the initial liquidity pairs were created with extremely small amounts of liquidity, slippage could possibly happen. \
> By imposing a minimum liquidity requirement during initial minting, Uniswap ensures that no single address (except possibly for `address(0)`) holds the share of the pool. And the liquidity ratio is thus bounded, which also prevents some malicious operations.

## Problem 4

Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
>
> This line of code basically tells the liquidity providers to provide liquidity per portion of different tokens in the pool; otherwise they'd have to pay more than they can get by their liquidity through `burn` in the future.
>
> ```solidity
> liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
> ```

The intention behind this is the to maintain the pool stability, hence reduces possible slippage.

## Problem 5

What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution
>
> A sandwich attack is when a blockchain attacker sandwiches a swap between two transactions to make a profit. In a sandwich attack, a malicious actor exploits the predictability of price movements at the expense of other traders. Here's how a sandwich attack typically works:
>
> 1.  A user submits a swap, and it is pending confirmation.
> 2.  A blockchain attacker sees the pending transaction, and knows the price for the token swapped will increase. So, they submit a swap. This is called **front-running**.
> 3.  The blockchain attackers swap is completed at a low price.
> 4.  The user’s transaction is completed at a high price, which means they receive less tokens than expected.
> 5.  The blockchain attacker swaps the tokens again at a higher price. This is called **back-running**.
>
> The blockchain attacker profits from the increase in price from the previous transactions. This results in a gain for the attacker, and a loss for the user.
