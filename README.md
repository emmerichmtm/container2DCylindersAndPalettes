# 2-D Container Loading Checker

A tiny Python utility that validates a 2-D load plan for a truck or container and produces a colour-coded PNG showing any problems. Rectangles represent Euro-pallets (or other boxes); circles represent paper rolls (or any cylindrical load).

<div align="center">
  <img src="docs/example.png" alt="Example output" width="650"/>
</div>

---

## ✨ Features

* **Boundary check** – warns when a shape sticks outside the container walls.
* **Collision check** – detects overlaps among any mix of rectangles and circles.
* **Red-tinted highlights** for every invalid item in the PNG output.
* **Single-file script** – no external dependencies beyond Matplotlib.
* Works in a normal Python script *or* a Jupyter notebook.

---

## 🛠 Requirements

| Package    | Version      |
| ---------- | ------------ |
| Python     | 3.8 or newer |
| matplotlib | ≥ 3.0        |

Install the dependency (Matplotlib) globally or in a virtual env:

```bash
python -m pip install matplotlib
```

---

## 🚀 Quick start

```bash
git clone https://github.com/your-username/container-loading-checker.git
cd container-loading-checker
python container_loading.py
```

The script writes **`container_loading.png`** in the same directory and prints its absolute path.

> **Tip:** Edit the `rectangles` and `circles` lists near the top of `container_loading.py` to try your own pallet / roll layouts. The rest of the code adapts automatically.

---

## ⚙️ Configuration

| Constant                 | Default | Meaning                                         |
| ------------------------ | ------- | ----------------------------------------------- |
| `CONTAINER_LENGTH`       | 13.6 m  | Internal *x* dimension of the box               |
| `CONTAINER_WIDTH`        | 2.45 m  | Internal *y* dimension of the box               |
| `rectangles` / `circles` | sample  | Lists of **dicts** that describe each load item |

### Rectangle dictionary

```python
{
  "id": "P1",          # unique label (string)
  "center": (1.0, 0.6), # (x, y) in metres
  "w": 1.2,            # width  (x-span)
  "h":
```
