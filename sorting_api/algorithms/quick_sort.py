def quick_sort(input_data):
    low = 0
    high = len(input_data) - 1
    steps = []

    def partition(array, low, high):
        pivot = array[high]
        steps.append(
            {
                "type": "pivot",
                "index": high,
            }
        )
        i = low - 1

        for j in range(low, high):
            steps.append({"type": "compare", "indices": [j, high]})

            if array[j] <= pivot:
                i += 1
                if i != j:
                    array[i], array[j] = array[j], array[i]
                    steps.append({"type": "swap", "indices": [i, j]})

        pivot_index = i + 1
        if pivot_index != high:
            array[pivot_index], array[high] = array[high], array[pivot_index]

            steps.append({"type": "swap", "indices": [pivot_index, high]})

            steps.append(
                {
                    "type": "pivot",
                    "index": pivot_index,
                }
            )

        steps.append({"type": "sorted", "indices": [pivot_index]})

        steps.append({"type": "unpivot"})

        return pivot_index

    def _quick_sort(array, low, high, depth=0):
        if low == high:
            steps.append(
                {"type": "sorted", "indices": [low]},
            )
            return
        if low < high:
            partitionIndex = partition(array, low, high)
            left_length = partitionIndex - low
            right_length = high - partitionIndex
            if left_length > 1:
                steps.append(
                    {
                        "type": "group",
                        "start": low,
                        "length": left_length,
                        "depth": depth + 1,
                    }
                )
            _quick_sort(array, low, partitionIndex - 1, depth + 1)

            if left_length > 1:
                steps.append(
                    {
                        "type": "group",
                        "start": low,
                        "length": left_length,
                        "depth": depth,
                    }
                )

            if right_length > 1:
                steps.append(
                    {
                        "type": "group",
                        "start": partitionIndex + 1,
                        "length": right_length,
                        "depth": depth + 1,
                    }
                )
            _quick_sort(array, partitionIndex + 1, high, depth + 1)

            if right_length > 1:
                steps.append(
                    {
                        "type": "group",
                        "start": partitionIndex + 1,
                        "length": right_length,
                        "depth": depth,
                    }
                )

    _quick_sort(input_data, low, high, 0)
    return input_data, steps
