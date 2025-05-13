
#!/usr/bin/env python3
"""
2-D truck-container loading checker & visualiser
   - Rectangles represent Euro-pallets (or any box)
   - Circles represent paper rolls (all same radius here)
Author: ChatGPT (May 2025 example)
"""
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from pathlib import Path

# ─────────────────────────
# 1.  Container dimensions
# ─────────────────────────
CONTAINER_LENGTH = 13.6   # metres (x)
CONTAINER_WIDTH  =  2.45  # metres (y)

# ─────────────────────────
# 2.  Define your load list
#     – edit freely –
# ─────────────────────────
# Euro-pallets (rectangles)
rectangles = [
    {"id": "P1", "center": (1.0, 0.6),  "w": 1.2, "h": 0.8},   # overlaps P2
    {"id": "P2", "center": (1.5, 0.6),  "w": 1.2, "h": 0.8},   # overlaps P1
    {"id": "P3", "center": (13.2, 0.6), "w": 1.2, "h": 0.8},   # sticks out
    {"id": "P4", "center": (3.0, 1.8),  "w": 1.2, "h": 0.8},   # OK
    {"id": "P5", "center": (6.0, 0.6),  "w": 1.2, "h": 0.8},   # OK
    {"id": "P6", "center": (9.0, 1.8),  "w": 1.2, "h": 0.8},   # OK
]

# Paper rolls (circles)
RADIUS = 0.5
circles = [
    {"id": "R1", "center": (4.0, 0.6), "r": RADIUS},           # overlaps R2
    {"id": "R2", "center": (4.3, 0.6), "r": RADIUS},           # overlaps R1
    {"id": "R3", "center": (8.0, 1.5), "r": RADIUS},           # OK
    {"id": "R4", "center": (14.0, 1.0), "r": RADIUS},          # sticks out
]

# ─────────────────────────
# 3.  Geometry helpers
# ─────────────────────────
def rect_inside_container(rect):
    cx, cy, w, h = rect["center"][0], rect["center"][1], rect["w"], rect["h"]
    left, right  = cx - w/2, cx + w/2
    bottom, top  = cy - h/2, cy + h/2
    return (0 <= left <= CONTAINER_LENGTH) and (0 <= right <= CONTAINER_LENGTH) \
        and (0 <= bottom <= CONTAINER_WIDTH) and (0 <= top <= CONTAINER_WIDTH)

def circle_inside_container(circ):
    cx, cy, r = circ["center"][0], circ["center"][1], circ["r"]
    return (r <= cx <= CONTAINER_LENGTH - r) and (r <= cy <= CONTAINER_WIDTH - r)

def rects_overlap(a, b):
    dx = abs(a["center"][0] - b["center"][0])
    dy = abs(a["center"][1] - b["center"][1])
    return dx < (a["w"] + b["w"]) / 2 and dy < (a["h"] + b["h"]) / 2

def circles_overlap(a, b):
    dx = a["center"][0] - b["center"][0]
    dy = a["center"][1] - b["center"][1]
    return (dx*dx + dy*dy) < (a["r"] + b["r"])**2

def rect_circle_overlap(rect, circ):
    rx, ry, w, h = rect["center"][0], rect["center"][1], rect["w"], rect["h"]
    cx, cy, r    = circ["center"][0], circ["center"][1], circ["r"]
    # closest point on rect to circle
    closest_x = max(rx - w/2, min(cx, rx + w/2))
    closest_y = max(ry - h/2, min(cy, ry + h/2))
    dx, dy = closest_x - cx, closest_y - cy
    return (dx*dx + dy*dy) < r*r

# ─────────────────────────
# 4.  Validation phase
# ─────────────────────────
invalid = set()       # IDs that violate anything
# (a) outside walls
invalid.update([r["id"] for r in rectangles if not rect_inside_container(r)])
invalid.update([c["id"] for c in circles if not circle_inside_container(c)])

# (b) pair-wise overlaps
for i in range(len(rectangles)):
    for j in range(i+1, len(rectangles)):
        if rects_overlap(rectangles[i], rectangles[j]):
            invalid.update([rectangles[i]["id"], rectangles[j]["id"]])

for i in range(len(circles)):
    for j in range(i+1, len(circles)):
        if circles_overlap(circles[i], circles[j]):
            invalid.update([circles[i]["id"], circles[j]["id"]])

for r in rectangles:
    for c in circles:
        if rect_circle_overlap(r, c):
            invalid.update([r["id"], c["id"]])

# ─────────────────────────
# 5.  Plot and save
# ─────────────────────────
fig, ax = plt.subplots(figsize=(14, 3))          # single plot
# container outline
ax.add_patch(Rectangle((0, 0), CONTAINER_LENGTH, CONTAINER_WIDTH,
                       fill=False, linewidth=2))
# pallets
for r in rectangles:
    cx, cy, w, h = r["center"][0], r["center"][1], r["w"], r["h"]
    lower_left = (cx - w/2, cy - h/2)
    fill = 'red' if r["id"] in invalid else 'none'
    alpha = 0.4 if r["id"] in invalid else 1.0
    ax.add_patch(Rectangle(lower_left, w, h,
                           edgecolor='black', facecolor=fill, alpha=alpha, lw=1.5))
    ax.text(cx, cy, r["id"], ha='center', va='center', fontsize=9)

# rolls
for c in circles:
    cx, cy, r = c["center"][0], c["center"][1], c["r"]
    fill = 'red' if c["id"] in invalid else 'none'
    alpha = 0.4 if c["id"] in invalid else 1.0
    ax.add_patch(Circle((cx, cy), r,
                        edgecolor='black', facecolor=fill, alpha=alpha, lw=1.5))
    ax.text(cx, cy, c["id"], ha='center', va='center', fontsize=9)

# axes tweaks
ax.set_xlim(-0.2, CONTAINER_LENGTH + 0.2)
ax.set_ylim(-0.2, CONTAINER_WIDTH  + 0.2)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel("Length (m)")
ax.set_ylabel("Width (m)")
ax.set_title("2-D Container Loading  –  problem items tinted red", pad=15)
plt.tight_layout()

# save PNG next to script
out_path = Path(__file__).with_name("container_loading.png")
fig.savefig(out_path, dpi=300)
print(f"Load-plan graphic written to {out_path.resolve()}")
