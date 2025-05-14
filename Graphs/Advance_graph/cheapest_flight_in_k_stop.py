class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        prices = [float('inf')] * n
        prices[src] = 0

        for i in range(k+1):
            temp_price = prices.copy()

            for s,d, p in flights:
                if prices[s] == float('inf'): continue
                if prices[s] + p < temp_price[d]:
                    temp_price[d] = prices[s] + p 
            prices = temp_price
        return -1 if prices[dst] == float('inf') else prices[dst]


