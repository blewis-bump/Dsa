# Time Complexity Visualizer

A local Flask API that empirically measures how an algorithm's running time
scales with input size, plots the result with matplotlib, and returns both
the raw timing data and a base64-encoded snapshot of the chart.

## Contents

- [How it works](#how-it-works)
- [Project layout](#project-layout)
- [Requirements](#requirements)
- [Running the server](#running-the-server)
- [API reference](#api-reference)
  - [`GET /analyze`](#get-analyze)
  - [`GET /algorithms`](#get-algorithms)
- [Supported algorithms](#supported-algorithms)
- [Stack and Queue](#stack-and-queue)
- [Snapshots](#snapshots)
- [Adding a new algorithm](#adding-a-new-algorithm)
- [Known limitations](#known-limitations)

## How it works

For a request like `algo=linear_search`, `step=10`, `n_max=100`, the server:

1. Builds a list of input sizes `0, step, 2*step, ..., n_max` (inclusive of
   `n_max` when it lands on a step boundary).
2. Runs the chosen algorithm once per input size, timing each run with
   `time.time()`.
3. Plots input size (x-axis) against running time in seconds (y-axis) with
   matplotlib, using the non-interactive `Agg` backend so it can run headless
   on a server with no display.
4. Saves the plot as a PNG under `snapshots/` and also encodes it as base64.
5. Returns both the raw `(input_sizes, times)` series and the base64 image in
   a single JSON response.

`n_min` is always `0` — the task only exposes `algo`, `step`, and `n_max` as
parameters.

## Project layout

| File | Responsibility |
|---|---|
| [`server.py`](server.py) | Flask app; defines `/analyze` and `/algorithms`, validates query params, saves snapshots, builds the JSON response. |
| [`algorithms.py`](algorithms.py) | The algorithm implementations available to the visualizer, keyed in the `ALGORITHMS` dict. |
| [`Algorithm.py`](Algorithm.py) | `time_complexity_visualizer(...)` — runs an algorithm across a range of input sizes and returns a matplotlib figure plus the timing data. |
| [`data_structures.py`](data_structures.py) | `Stack` and `Queue` classes used by the stack/queue entries in `ALGORITHMS`. |
| [`test_data_structures.py`](test_data_structures.py) | `unittest` suite covering `Stack` and `Queue`. |
| `snapshots/` | Created automatically on first run; holds one timestamped PNG per `/analyze` request. |

## Requirements

- Python 3.10+
- `flask`
- `matplotlib`
- `numpy`

Install with:

```powershell
pip install flask matplotlib numpy
```

## Running the server

From the project root:

```powershell
python server.py
```

The app listens on `http://localhost:8000` (debug mode is on, so it
auto-reloads when you edit the source). Stop it with `Ctrl+C` in that
terminal — avoid killing it via `taskkill /IM python.exe`, since that
terminates every Python process on the machine, not just this server.

## API reference

### `GET /analyze`

Runs one algorithm across a range of input sizes and returns timing data plus
a chart.

**Query parameters**

| Name | Type | Required | Notes |
|---|---|---|---|
| `algo` | string | Yes | One of the [supported algorithms](#supported-algorithms). Case-insensitive; surrounding quotes are stripped, so `algo='linear_search'` and `algo=linear_search` are equivalent. |
| `step` | integer | Yes | Must be a positive integer. Spacing between successive input sizes. |
| `n_max` | integer | Yes | Must be a positive integer. Upper bound on input size. Commas are accepted (e.g. `10,000`). |

`n_min` is implicit and always `0`.

**Example request**

```
GET http://localhost:8000/analyze?algo=linear_search&step=10&n_max=100
```

**Example response** (`200 OK`)

```json
{
  "algo": "linear_search",
  "step": 10,
  "n_min": 0,
  "n_max": 100,
  "input_sizes": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
  "times": [0.0000024, 0.0000131, ...],
  "snapshot_path": "C:\\...\\snapshots\\linear_search_20260921_104834.png",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgA..."
}
```

`image_base64` is a raw base64-encoded PNG — decode it directly to bytes and
write to a `.png` file, or prefix it with `data:image/png;base64,` to embed
it in an `<img>` tag or Markdown.

**Error responses** (`400 Bad Request`)

| Condition | Body |
|---|---|
| `algo` missing | `{"error": "Missing required query parameter: algo"}` |
| `algo` not recognized | `{"error": "Unknown algorithm '<value>'", "supported_algorithms": [...]}` |
| `step` missing, non-numeric, or ≤ 0 | `{"error": "Query parameter 'step' must be a positive integer"}` |
| `n_max` missing | `{"error": "Missing required query parameter: n_max"}` |
| `n_max` non-numeric | `{"error": "Query parameter 'n_max' must be an integer"}` |
| `n_max` ≤ 0 | `{"error": "Query parameter 'n_max' must be greater than 0"}` |

### `GET /algorithms`

Lists the algorithm names accepted by `algo`.

**Example response**

```json
{
  "supported_algorithms": [
    "binary_search",
    "bubble_sort",
    "insertion_sort",
    "linear_search",
    "nested_loops",
    "selection_sort"
  ]
}
```

## Supported algorithms

All algorithms are defined in [`algorithms.py`](algorithms.py) as a single
function `f(n)` that performs one run of the algorithm on an input of size
`n`. Sorting/searching algorithms are run in their worst case (target absent,
or already-sorted input reversed as needed) so the timing curve reflects the
algorithm's worst-case complexity rather than a lucky best case.

| `algo` value | Description | Expected time complexity |
|---|---|---|
| `linear_search` | Scans a list of `n` random integers for a value that isn't present. | O(n) |
| `binary_search` | Binary search over a sorted range of `n` integers for a value that isn't present. | O(log n) |
| `bubble_sort` | Bubble sort on a random list of `n` integers. | O(n²) |
| `nested_loops` | Two nested `range(n)` loops with a counter increment — a baseline O(n²) reference with no data-dependent branching. | O(n²) |
| `insertion_sort` | Insertion sort on a random list of `n` integers. | O(n²) |
| `selection_sort` | Selection sort on a random list of `n` integers. | O(n²) |
| `stack_push_pop` | Pushes `n` items onto a [`Stack`](data_structures.py) then pops them all off. | O(n) |
| `queue_enqueue_dequeue` | Enqueues `n` items onto a [`Queue`](data_structures.py) then dequeues them all. This `Queue.dequeue()` is `list.pop(0)`, which shifts every remaining element, so the operation itself is O(n). | O(n²) |
| `stack_based_reversal` | Reverses a random list of `n` integers by pushing all of them onto a `Stack` and popping them back off. | O(n) |
| `queue_based_rotation` | Rotates a random list of `n` integers by repeatedly dequeuing the front of a `Queue` and enqueuing it back to the end. | O(n²) |

`stack_push_pop`/`stack_based_reversal` and `queue_enqueue_dequeue`/`queue_based_rotation`
are intentionally paired so the visualizer plots stack ops (O(n), all O(1)
operations) next to queue ops (O(n²), because this `Queue`'s `dequeue()` is
O(n)) and shows the two curves diverge as `n` grows.

## Stack and Queue

[`data_structures.py`](data_structures.py) provides `Stack` (LIFO) and
`Queue` (FIFO) classes, both backed by a Python list:

- `Stack`: `push`, `pop`, `peek`, `is_empty`, `len()`. `pop`/`peek` on an
  empty stack raise `IndexError`.
- `Queue`: `enqueue`, `dequeue`, `front`, `is_empty`, `len()`. `dequeue` is
  `list.pop(0)`, so it's O(n) rather than O(1) — see the note on
  `queue_enqueue_dequeue` below. `dequeue`/`front` on an empty queue raise
  `IndexError`.

Run the test suite (20 `unittest` cases covering push/pop/enqueue/dequeue,
LIFO/FIFO ordering, empty-structure errors, and falsy/`None` values):

```powershell
python -m unittest test_data_structures.py -v
```

Four algorithms built on `Stack`/`Queue` are registered in `ALGORITHMS` (see
[Supported algorithms](#supported-algorithms)) so they can be timed and
plotted through `/analyze` exactly like the sorting/searching algorithms,
e.g.:

```
GET http://localhost:8000/analyze?algo=stack_push_pop&step=100&n_max=1000
GET http://localhost:8000/analyze?algo=queue_enqueue_dequeue&step=100&n_max=1000
```

## Snapshots

Every `/analyze` call writes a PNG to `snapshots/<algo>_<YYYYMMDD_HHMMSS>.png`
in the project root (created automatically if it doesn't exist). The same
image is also returned inline as `image_base64`, so the file on disk is a
persistent copy/audit trail rather than something the caller must read to
get the chart.

## Adding a new algorithm

1. Add a function to [`algorithms.py`](algorithms.py) with the signature
   `def my_algorithm(n): ...` that does one full run for input size `n`.
2. Register it in the `ALGORITHMS` dict with the key you want exposed as the
   `algo` query value:

   ```python
   ALGORITHMS = {
       ...
       "my_algorithm": my_algorithm,
   }
   ```

3. No changes to `server.py` or `Algorithm.py` are needed — both read from
   `ALGORITHMS` dynamically.

## Known limitations

- Timing uses wall-clock `time.time()` around a single run per input size —
  there's no repetition/averaging, so results can be noisy for very small
  `n` or a busy machine. For steadier curves, use a larger `step`/`n_max`
  range where runtime dominates measurement overhead.
- O(n²) algorithms (`bubble_sort`, `nested_loops`, `insertion_sort`,
  `selection_sort`) with a large `n_max` can make a single request take a
  long time, since the server runs the algorithm once per input size
  synchronously before responding.
- The server runs with `debug=True`, which is convenient for local
  development but should not be used as-is if this is ever exposed beyond
  `localhost`.
