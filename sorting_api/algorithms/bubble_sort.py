def bubble_sort(input_data):
    n = len(input_data)
    steps = []

    for i in range(n - 1):
        for j in range(n - i - 1):
            steps.append({"type": "compare", "indices": [j, j + 1]})

            if input_data[j] > input_data[j + 1]:
                input_data[j], input_data[j + 1] = input_data[j + 1], input_data[j]

                steps.append({"type": "swap", "indices": [j, j + 1]})

        steps.append({"type": "sorted", "indices": [n - 1 - i]})

    # Mark the first element as sorted after the loop completes
    steps.append({"type": "sorted", "indices": [0]})
    return input_data, steps
