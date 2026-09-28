# Sorting Visualizer Operation Protocol

The Django backend returns a sequence of generic operations describing how React should visualize a sorting algorithm.

React should understand the operations themselves without containing algorithm-specific sorting logic.

## `compare`

Highlights one or more array positions currently involved in a comparison.

```json
{
  "type": "compare",
  "indices": [1, 2]
}
```

`indices` may contain one or more positions depending on the algorithm.

For example, Insertion Sort may compare an array value against a separately held key:

```json
{
  "type": "compare",
  "indices": [2]
}
```

---

## `swap`

Swaps two values in the displayed array.

```json
{
  "type": "swap",
  "indices": [1, 2]
}
```

Used when two existing array positions directly exchange values.

A `swap` should not be emitted when both indices refer to the same position.

---

## `write`

Writes a value directly into an array position.

```json
{
  "type": "write",
  "index": 2,
  "value": 7
}
```

`write` only changes the displayed value at the specified position. Other visualization state, such as a held value or gap, is controlled by separate operations.

---

## `hold`

Displays a value separately from the normal array positions.

```json
{
  "type": "hold",
  "value": 5
}
```

The held value remains active until a `release` operation is received.

Currently used by Insertion Sort.

---

## `release`

Releases the currently held value.

```json
{
  "type": "release"
}
```

`release` only controls the held-value visualization. It does not modify gap state.

Currently used by Insertion Sort.

---

## `gap`

Marks one array position as the current visual gap.

```json
{
  "type": "gap",
  "index": 3
}
```

A new `gap` operation replaces the previous gap position.

This allows the gap to move independently as values are shifted or written.

Currently used by Insertion Sort.

---

## `ungap`

Clears the current visual gap.

```json
{
  "type": "ungap"
}
```

`ungap` only controls gap visualization and does not release a held value.

Currently used by Insertion Sort.

---

## `move`

Moves an existing displayed value from one position to another.

```json
{
  "type": "move",
  "from": 4,
  "to": 2
}
```

The value at `from` is removed and inserted at `to`. Values between those positions shift as necessary.

For example:

```text
[3, 8, 4, 5]

move 2 → 1

[3, 4, 8, 5]
```

Currently used by Merge Sort.

A `move` should not be emitted when `from` and `to` are the same position.

---

## `group`

Changes the visual recursion depth of a contiguous range of positions.

```json
{
  "type": "group",
  "start": 0,
  "length": 4,
  "depth": 1
}
```

The affected positions are:

```text
start ... start + length - 1
```

For the example above:

```text
0, 1, 2, 3
```

`depth` represents the group's current recursive visualization level.

A later `group` operation may return the same range to a shallower depth as recursion unwinds.

Currently used by Merge Sort and Quick Sort to visually separate recursive subproblems.

Single-element groups are not emitted because a single value does not require recursion-depth visualization.

---

## `pivot`

Marks one array position as the currently active pivot.

```json
{
  "type": "pivot",
  "index": 6
}
```

React should visually distinguish the pivot from ordinary active comparison positions.

A new `pivot` operation replaces the previously active pivot position. This allows the pivot visualization to follow the pivot value if it moves to another position.

A `swap` does not implicitly update the pivot position. If a swap moves the pivot, the backend must emit a new `pivot` operation with its new index.

Currently used by Quick Sort.

---

## `unpivot`

Clears the currently active pivot.

```json
{
  "type": "unpivot"
}
```

`unpivot` only controls pivot visualization. It does not modify array values or finalized positions.

A `sorted` operation does not implicitly clear the pivot. The backend must emit `unpivot` explicitly.

When a pivot reaches its final position, Quick Sort may emit:

```text
pivot
...
swap
pivot
sorted
unpivot
```

This allows the pivot to transition directly from its pivot visualization to its finalized visualization without requiring React to infer pivot behavior from `swap` or `sorted`.

Currently used by Quick Sort.

---

## `sorted`

Marks one or more array positions as finalized.

```json
{
  "type": "sorted",
  "indices": [3]
}
```

Multiple positions may be finalized by one operation:

```json
{
  "type": "sorted",
  "indices": [0, 1, 2, 3]
}
```

A finalized position has reached its final location in the sorted result and should remain visually marked as sorted.

`sorted` means finalized, not merely that the values currently appear in sorted order.

Other visualization state, such as a pivot, held value, gap, or recursion depth, is controlled by its own operation.