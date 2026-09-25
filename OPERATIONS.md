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

May optionally include a new gap position:

```json
{
  "type": "write",
  "index": 3,
  "value": 8,
  "gap": 2
}
```

The optional `gap` is currently used by Insertion Sort when shifting values while a key is being held.

---

## `hold`

Removes a value conceptually from normal array processing and displays it as a held value.

```json
{
  "type": "hold",
  "value": 5,
  "index": 3
}
```

`index` identifies the initial gap position.

Currently used by Insertion Sort.

---

## `release`

Releases the currently held value and clears the held/gap visualization.

```json
{
  "type": "release"
}
```

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

Currently used by Merge Sort to show recursive subdivision.

Single-element groups are not emitted because a single value requires no sorting.

---

## `sorted`

Marks one or more positions as finalized.

```json
{
  "type": "sorted",
  "indices": [4]
}
```

Multiple positions may be finalized at once:

```json
{
  "type": "sorted",
  "indices": [0, 1, 2, 3, 4]
}
```

`sorted` means the positions are in their final sorted state, not merely sorted relative to a temporary subarray.

---

# Design Rules

Operations describe visualization events rather than implementing sorting logic in React.

The backend decides **what happened**. React decides **how that operation is displayed**.

Avoid emitting operations that represent no visible change, such as:

```json
{
  "type": "move",
  "from": 2,
  "to": 2
}
```

or a same-position swap.

This keeps the operation stream meaningful and prevents misleading animations.