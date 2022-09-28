
class Item:

    def __init__(self, weight, value, index):
        self.weight = weight
        self.value = value
        self.index = index
        self.cost = value // weight

    def __lt__(self, other):
        return self.cost < other.cost


class FractionalKnapsock:

    @staticmethod
    def get_max_value(weight, value, capacity):
        items = []
        for i in range(len(weight)):
            items.append(Item(weight[i], value[i], i))

        # Sort items in decreasing order of ratio value/weight
        items.sort(reverse=True)

        max_value_selected = 0

        for i in items:
            wt = int(i.weight)
            val = int(i.value)

            if capacity-wt >= 0:
                capacity -= wt
                max_value_selected += val
            else:
                f = capacity/wt
                max_value_selected += (f*val)
                capacity = int(capacity-(f*val))
                break

        return max_value_selected


if __name__ == "__main__":
    wt = [10, 40, 20, 30]
    val = [60, 40, 100, 120]
    capacity = 50

    max_value = FractionalKnapsock.get_max_value(wt, val, capacity)
    print("Maximum value in Knapsack =", max_value)

    weights = [4, 9, 10, 20, 2, 1]
    values = [400, 1800, 3500, 4000, 1000, 200]
    capacity = 20

    max_value = FractionalKnapsock.get_max_value(weights, values, capacity)
    print("Maximum value in Knapsack =", max_value)
