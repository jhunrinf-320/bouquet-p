import pygame
import math
import random
import sys

# ============================================================
# BLOOM — ALIGNED BLUE BOUQUET
# Optimized for Pydroid 3
# ============================================================

pygame.init()

WIDTH, HEIGHT = 360, 800
FPS = 24
FLOWER_FRAMES = 12

try:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
except pygame.error:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

SCREEN_W, SCREEN_H = screen.get_size()
pygame.display.set_caption("Bloom - Blue Bouquet")

canvas = pygame.Surface((WIDTH, HEIGHT)).convert()
clock = pygame.time.Clock()

# ============================================================
# COLORS
# ============================================================

BG_TOP = (5, 10, 30)
BG_BOTTOM = (12, 24, 55)

WHITE = (240, 247, 255)
ICE = (195, 220, 255)

DARK_GREEN = (19, 65, 58)
GREEN = (34, 105, 83)
LIGHT_GREEN = (75, 155, 120)

PAPER = (205, 218, 240)
PAPER_LIGHT = (235, 241, 255)
PAPER_SHADOW = (135, 160, 205)

# ============================================================
# BOUQUET LAYOUT
# All flower, stem, leaf and wrapper positions use this layout.
# ============================================================

FLOWER_BASE_Y = 235
STEM_BASE_Y = 665
WRAPPER_TOP = 555
WRAPPER_BOTTOM = 735

flowers = [
    {"x": 112, "y": 280, "type": "rose", "size": 1.00, "delay": 0.4},
    {"x": 180, "y": 230, "type": "daisy", "size": 0.95, "delay": 0.8},
    {"x": 248, "y": 280, "type": "rose", "size": 0.90, "delay": 1.2},
    {"x": 72,  "y": 385, "type": "daisy", "size": 0.78, "delay": 1.6},
    {"x": 150, "y": 380, "type": "tulip", "size": 0.92, "delay": 2.0},
    {"x": 225, "y": 390, "type": "daisy", "size": 0.80, "delay": 2.4},
    {"x": 288, "y": 390, "type": "tulip", "size": 0.70, "delay": 2.8},
]

# Each stem begins near the bottom center of its flower.
# All stems converge toward the bouquet's tied base.
for flower in flowers:
    flower["stem_start"] = (
        flower["x"],
        flower["y"] + int(55 * flower["size"])
    )

    flower["stem_end"] = (
        180 + (flower["x"] - 180) * 0.16,
        STEM_BASE_Y
    )

# ============================================================
# BACKGROUND
# ============================================================

def make_background():
    bg = pygame.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = (
            int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio),
            int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio),
            int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        )
        pygame.draw.line(bg, color, (0, y), (WIDTH, y))

    # Static background stars
    random.seed(12)

    for _ in range(35):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(20, HEIGHT - 20)
        radius = random.randint(1, 2)

        pygame.draw.circle(
            bg, (35, 60, 105), (x, y), radius
        )

    # Static soft light behind flowers
    glow = pygame.Surface((240, 300), pygame.SRCALPHA)

    for radius in range(120, 0, -5):
        alpha = int(2 + 8 * radius / 120)
        pygame.draw.circle(
            glow,
            (35, 75, 145, alpha),
            (120, 150),
            radius
        )

    bg.blit(glow, (60, 140))
    return bg


background = make_background()

# ============================================================
# FLOWER DRAWING
# ============================================================

def create_daisy(size):
    s = int(150 * size)
    flower = pygame.Surface((s, s), pygame.SRCALPHA)
    center = s // 2

    petal_count = 12
    petal_length = int(s * 0.30)
    petal_width = int(s * 0.15)

    colors = [WHITE, ICE, (210, 230, 255)]

    for i in range(petal_count):
        angle = i * (360 / petal_count)

        petal = pygame.Surface(
            (petal_width * 2, petal_length * 2),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            petal,
            colors[i % len(colors)],
            (
                petal_width // 2,
                0,
                petal_width,
                petal_length * 2
            )
        )

        rotated = pygame.transform.rotate(petal, -angle)
        distance = int(s * 0.22)

        px = center + math.cos(math.radians(angle - 90)) * distance
        py = center + math.sin(math.radians(angle - 90)) * distance

        rect = rotated.get_rect(center=(int(px), int(py)))
        flower.blit(rotated, rect)

    pygame.draw.circle(
        flower, (225, 177, 75),
        (center, center), int(s * 0.14)
    )

    pygame.draw.circle(
        flower, (255, 220, 125),
        (center - 3, center - 4), int(s * 0.07)
    )

    return flower


def create_rose(size):
    s = int(150 * size)
    flower = pygame.Surface((s, s), pygame.SRCALPHA)
    center = s // 2

    petal_colors = [
        (75, 125, 210),
        (95, 145, 225),
        (125, 165, 235),
        (155, 190, 245),
        (185, 210, 255)
    ]

    for i in range(10):
        angle = i * 36

        petal = pygame.Surface(
            (s // 2, s // 2),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            petal,
            petal_colors[i % 3],
            (5, 5, s // 2 - 10, s // 2 - 10)
        )

        rotated = pygame.transform.rotate(petal, -angle)
        distance = s * 0.19

        px = center + math.cos(math.radians(angle)) * distance
        py = center + math.sin(math.radians(angle)) * distance

        rect = rotated.get_rect(center=(int(px), int(py)))
        flower.blit(rotated, rect)

    for i in range(7):
        angle = i * 51
        radius = s * 0.11

        px = center + math.cos(math.radians(angle)) * radius
        py = center + math.sin(math.radians(angle)) * radius

        color = petal_colors[(i + 2) % len(petal_colors)]

        pygame.draw.ellipse(
            flower,
            color,
            (
                int(px - s * 0.12),
                int(py - s * 0.16),
                int(s * 0.24),
                int(s * 0.30)
            )
        )

    pygame.draw.circle(
        flower, (65, 105, 185),
        (center, center), int(s * 0.09)
    )

    return flower


def create_tulip(size):
    s = int(145 * size)
    flower = pygame.Surface((s, s), pygame.SRCALPHA)

    pygame.draw.ellipse(
        flower, (90, 145, 225),
        (int(s * 0.22), int(s * 0.28),
         int(s * 0.56), int(s * 0.55))
    )

    pygame.draw.ellipse(
        flower, (125, 175, 245),
        (int(s * 0.12), int(s * 0.22),
         int(s * 0.38), int(s * 0.55))
    )

    pygame.draw.ellipse(
        flower, (75, 125, 210),
        (int(s * 0.50), int(s * 0.22),
         int(s * 0.38), int(s * 0.55))
    )

    pygame.draw.ellipse(
        flower, (190, 215, 255),
        (int(s * 0.38), int(s * 0.30),
         int(s * 0.23), int(s * 0.42))
    )

    pygame.draw.circle(
        flower, (145, 185, 245),
        (int(s * 0.31), int(s * 0.30)), int(s * 0.15)
    )

    pygame.draw.circle(
        flower, (105, 155, 230),
        (int(s * 0.68), int(s * 0.30)), int(s * 0.15)
    )

    return flower


def create_flower(flower_type, size):
    if flower_type == "rose":
        return create_rose(size)
    if flower_type == "tulip":
        return create_tulip(size)
    return create_daisy(size)


# ============================================================
# PRE-RENDER FLOWER ANIMATION FRAMES
# ============================================================

def ease_out(value):
    value = max(0.0, min(1.0, value))
    return 1 - (1 - value) ** 3


for flower in flowers:
    original = create_flower(flower["type"], flower["size"])
    flower["frames"] = []

    original_w = original.get_width()
    original_h = original.get_height()

    for frame_index in range(FLOWER_FRAMES):
        progress = frame_index / (FLOWER_FRAMES - 1)
        scale = 0.08 + 0.92 * ease_out(progress)

        frame_size = (
            max(1, int(original_w * scale)),
            max(1, int(original_h * scale))
        )

        flower["frames"].append(
            pygame.transform.smoothscale(original, frame_size)
        )

# ============================================================
# STEMS
# ============================================================

stem_layer = pygame.Surface(
    (WIDTH, HEIGHT), pygame.SRCALPHA
)

for flower in flowers:
    x1, y1 = flower["stem_start"]
    x2, y2 = flower["stem_end"]

    pygame.draw.line(
        stem_layer,
        DARK_GREEN,
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        5
    )

    pygame.draw.line(
        stem_layer,
        LIGHT_GREEN,
        (int(x1 - 1), int(y1)),
        (int(x2 - 1), int(y2)),
        2
    )

# ============================================================
# LEAVES
# ============================================================

def draw_leaf(surface, x, y, length, angle, color=LIGHT_GREEN):
    leaf = pygame.Surface(
        (length + 20, length // 2 + 20),
        pygame.SRCALPHA
    )

    w = length + 20
    h = length // 2 + 20

    points = [
        (5, h // 2),
        (w // 3, 5),
        (w - 5, h // 2),
        (w // 3, h - 5)
    ]

    pygame.draw.polygon(leaf, color, points)

    pygame.draw.aaline(
        leaf,
        (145, 195, 160),
        (8, h // 2),
        (w - 8, h // 2)
    )

    rotated = pygame.transform.rotate(leaf, angle)
    rect = rotated.get_rect(center=(int(x), int(y)))
    surface.blit(rotated, rect)


leaf_layer = pygame.Surface(
    (WIDTH, HEIGHT), pygame.SRCALPHA
)

# Leaves are positioned around the stems, below the flower heads.
draw_leaf(leaf_layer, 105, 535, 78, 25)
draw_leaf(leaf_layer, 245, 535, 85, -25)
draw_leaf(leaf_layer, 145, 590, 75, -20)
draw_leaf(leaf_layer, 215, 590, 75, 20)
draw_leaf(leaf_layer, 180, 555, 65, 5)

# ============================================================
# WRAPPER
# ============================================================

def create_wrapper():
    layer = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    top_y = WRAPPER_TOP
    bottom_y = WRAPPER_BOTTOM
    center_x = 180

    # Back folds
    pygame.draw.polygon(
        layer,
        PAPER_SHADOW,
        [
            (105, top_y),
            (center_x, top_y + 15),
            (center_x - 35, bottom_y),
            (65, bottom_y - 5)
        ]
    )

    pygame.draw.polygon(
        layer,
        PAPER,
        [
            (255, top_y),
            (center_x, top_y + 15),
            (center_x + 35, bottom_y),
            (295, bottom_y - 5)
        ]
    )

    # Main front paper
    pygame.draw.polygon(
        layer,
        PAPER_LIGHT,
        [
            (105, top_y + 5),
            (255, top_y + 5),
            (center_x + 35, bottom_y),
            (center_x - 35, bottom_y)
        ]
    )

    # Paper creases
    pygame.draw.line(
        layer, (165, 185, 220),
        (120, top_y + 20), (155, bottom_y - 10), 2
    )

    pygame.draw.line(
        layer, (165, 185, 220),
        (240, top_y + 20), (205, bottom_y - 10), 2
    )

    pygame.draw.line(
        layer, WHITE,
        (180, top_y + 25), (180, bottom_y - 15), 2
    )

    return layer


wrapper_layer = create_wrapper()

# ============================================================
# RIBBON
# ============================================================

def create_ribbon():
    layer = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    y = 635

    pygame.draw.ellipse(
        layer, (80, 125, 205),
        (145, y - 10, 35, 22)
    )

    pygame.draw.ellipse(
        layer, (110, 155, 225),
        (180, y - 10, 35, 22)
    )

    pygame.draw.polygon(
        layer, (55, 95, 175),
        [(155, y), (130, y + 45), (165, y + 30)]
    )

    pygame.draw.polygon(
        layer, (55, 95, 175),
        [(205, y), (230, y + 45), (195, y + 30)]
    )

    pygame.draw.circle(
        layer, (175, 205, 255),
        (180, y), 8
    )

    return layer


ribbon_layer = create_ribbon()

# ============================================================
# SPARKLES
# ============================================================

random.seed(21)
sparkles = []

for _ in range(20):
    sparkles.append({
        "x": random.randint(15, WIDTH - 15),
        "y": random.randint(80, HEIGHT - 80),
        "size": random.randint(1, 2),
        "phase": random.random() * math.tau
    })


def draw_sparkles(surface, elapsed):
    for star in sparkles:
        pulse = (
            math.sin(elapsed * 2 + star["phase"]) + 1
        ) / 2

        radius = star["size"] + (1 if pulse > 0.85 else 0)

        color = (
            80 + int(pulse * 60),
            120 + int(pulse * 60),
            190 + int(pulse * 50)
        )

        pygame.draw.circle(
            surface,
            color,
            (star["x"], star["y"]),
            radius
        )

# ============================================================
# DRAW SCENE
# ============================================================

def draw_scene(elapsed):
    canvas.blit(background, (0, 0))
    draw_sparkles(canvas, elapsed)

    # Stems grow upward from the tied end.
    stem_progress = ease_out(elapsed / 2.5)

    if stem_progress > 0:
        for flower in flowers:
            x1, y1 = flower["stem_start"]
            x2, y2 = flower["stem_end"]

            current_x = x2 + (x1 - x2) * stem_progress
            current_y = y2 + (y1 - y2) * stem_progress

            pygame.draw.line(
                canvas,
                DARK_GREEN,
                (int(current_x), int(current_y)),
                (int(x2), int(y2)),
                5
            )

            pygame.draw.line(
                canvas,
                LIGHT_GREEN,
                (int(current_x - 1), int(current_y)),
                (int(x2 - 1), int(y2)),
                2
            )

    # Leaves
    leaf_progress = ease_out((elapsed - 1.0) / 2.0)

    if leaf_progress > 0.1:
        canvas.blit(leaf_layer, (0, 0))

    # Wrapper reveal.
    # IMPORTANT: The destination and source rectangles match.
    # This keeps the wrapper at the bottom instead of the top.
    wrapper_progress = ease_out((elapsed - 2.0) / 2.0)

    if wrapper_progress > 0:
        reveal_height = int(
            (WRAPPER_BOTTOM - WRAPPER_TOP) * wrapper_progress
        )

        source_rect = pygame.Rect(
            0,
            WRAPPER_TOP,
            WIDTH,
            reveal_height
        )

        canvas.blit(
            wrapper_layer,
            source_rect.topleft,
            source_rect
        )

    # Flowers bloom one by one.
    for flower in flowers:
        progress = ease_out(
            (elapsed - flower["delay"]) / 1.3
        )

        if progress <= 0:
            continue

        frame_index = int(
            progress * (FLOWER_FRAMES - 1)
        )

        frame_index = min(
            FLOWER_FRAMES - 1,
            max(0, frame_index)
        )

        image = flower["frames"][frame_index]

        rect = image.get_rect(
            center=(flower["x"], flower["y"])
        )

        canvas.blit(image, rect)

    # Ribbon appears after wrapper.
    ribbon_progress = ease_out((elapsed - 4.0) / 1.5)

    if ribbon_progress > 0.1:
        canvas.blit(ribbon_layer, (0, 0))


# ============================================================
# MAIN LOOP
# ============================================================

start_time = pygame.time.get_ticks()
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    elapsed = (
        pygame.time.get_ticks() - start_time
    ) / 1000.0

    draw_scene(elapsed)

    scaled_frame = pygame.transform.scale(
        canvas,
        (SCREEN_W, SCREEN_H)
    )

    screen.blit(scaled_frame, (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()