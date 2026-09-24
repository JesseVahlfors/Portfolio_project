def insertion_sort(input_data):
    n = len(input_data)
    steps = []

    for i in range(1, n):
        key = input_data[i]
        j = i - 1

        steps.append(
            {
                "type": "hold",
                "index": i,
                "value": key,
            }
        )

        while j >= 0:
            steps.append(
                {
                    "type": "compare",
                    "indices": [j],
                }
            )
            if input_data[j] <= key:
                break
            input_data[j + 1] = input_data[j]
            steps.append(
                {
                    "type": "write",
                    "index": [j + 1],
                    "value": input_data[j],
                    "gap": j,
                }
            )
            j -= 1
        input_data[j + 1] = key
        steps.append({"type": "write", "index": [j + 1], "value": key})
        steps.append(
            {
                "type": "release",
            }
        )
    steps.append({"type": "sorted", "indices": list(range(n))})
    return input_data, steps
