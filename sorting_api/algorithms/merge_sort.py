def merge_sort(input_data):
    steps = []

    def _merge_sort(array, start=0, depth=0, steps=None):
        if steps is None:
            steps = []

        # Base case: a single value is already sorted.
        if len(array) <= 1:
            return array

        # Split the current subarray into left and right halves.
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]

        # Move the left group one level deeper while it is being sorted.
        # Single values are not moved because they need no sorting.
        if len(left) > 1:
            steps.append(
                {
                    "type": "group",
                    "start": start,
                    "length": len(left),
                    "depth": depth + 1,
                }
            )

        # Recursively sort the left half.
        sorted_left = _merge_sort(left, start, depth + 1, steps)

        # Return the sorted left group to the current level.
        if len(left) > 1:
            steps.append(
                {
                    "type": "group",
                    "start": start,
                    "length": len(left),
                    "depth": depth,
                }
            )

        # Move the right group one level deeper while it is being sorted.
        if len(right) > 1:
            steps.append(
                {
                    "type": "group",
                    "start": start + mid,
                    "length": len(right),
                    "depth": depth + 1,
                }
            )

        # Recursively sort the right half.
        sorted_right = _merge_sort(right, start + mid, depth + 1, steps)

        # Return the sorted right group to the current level.
        if len(right) > 1:
            steps.append(
                {
                    "type": "group",
                    "start": start + mid,
                    "length": len(right),
                    "depth": depth,
                }
            )

        # Both halves are now sorted. Merge them at the current level.
        return merge(sorted_left, sorted_right, start, depth, steps)

    def merge(left, right, start, depth, steps):
        result = []
        i = j = 0

        # track subarray positions
        left_pos = start
        right_pos = start + len(left)

        # Compare the next unused values from each sorted half.
        while i < len(left) and j < len(right):
            destination = start + len(result)

            # Highlight the two values currently being compared.
            steps.append(
                {
                    "type": "compare",
                    "indices": [left_pos, right_pos],
                }
            )

            if left[i] <= right[j]:
                # Left value wins the comparison and is next in the merged result.
                value = left[i]

                result.append(value)
                i += 1
                left_pos += 1

            else:
                # Right value wins the comparison and is next in the merged result.
                value = right[j]

                # Move the right value into the next result position.
                steps.append(
                    {
                        "type": "move",
                        "from": right_pos,
                        "to": destination,
                    }
                )

                result.append(value)
                j += 1
                left_pos += 1
                right_pos += 1

        # One half is exhausted. Append any remaining left-side values.
        while i < len(left):
            value = left[i]

            result.append(value)
            i += 1

        # Append any remaining right-side values.
        while j < len(right):
            value = right[j]

            result.append(value)
            j += 1

        # Return this sorted subarray to the parent recursive call.
        return result

    sorted_array = _merge_sort(
        input_data,
        start=0,
        depth=0,
        steps=steps,
    )

    steps.append(
        {
            "type": "sorted",
            "indices": list(range(len(sorted_array))),
        }
    )

    return sorted_array, steps
