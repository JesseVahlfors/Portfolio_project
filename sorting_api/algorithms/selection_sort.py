def selection_sort(input_data):
    n = len(input_data)
    steps = []

    for i in range(n - 1):
        minIdx = i

        for j in range(i + 1, n):
            steps.append({"type": "compare", "indices": [j, minIdx]})
            if input_data[j] < input_data[minIdx]:
                minIdx = j

        if minIdx != i:
            input_data[i], input_data[minIdx] = input_data[minIdx], input_data[i]
            steps.append({"type": "swap", "indices": [i, minIdx]})

        steps.append({"type": "sorted", "indices": [i]})
    steps.append({"type": "sorted", "indices": [n - 1]})

    return input_data, steps
