# procedural_generator.py
# AURA One MVP - Procedural Floor Plan Generator
# This module generates a basic, procedural floor plan layout from user-defined parameters.

import random
from typing import List, Dict

Room = Dict[str, any]  # Type alias for clarity

# Room size presets (width, height in meters)
ROOM_TYPES = {
    "living_room": (4, 5),
    "bedroom": (3, 4),
    "kitchen": (3, 3),
    "bathroom": (2, 2.5),
    "dining_room": (3, 4),
    "study": (2.5, 3.5),
    "laundry": (2, 2),
    "storage": (2, 2),
}

def generate_room(name: str, position: tuple, size: tuple) -> Room:
    """
    Create a single room definition.
    """
    x, y = position
    width, height = size
    return {
        "name": name,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "area": width * height
    }

def arrange_rooms(room_list: List[str]) -> List[Room]:
    """
    Arrange rooms in a grid-like layout procedurally.
    Each room is placed next to the previous one.
    """
    x_cursor = 0
    y_cursor = 0
    row_height = 0
    max_width = 12  # Reset row if cumulative width exceeds this
    plan: List[Room] = []

    for room_name in room_list:
        size = ROOM_TYPES.get(room_name, (3, 3))
        room_width, room_height = size

        if x_cursor + room_width > max_width:
            x_cursor = 0
            y_cursor += row_height + 1
            row_height = 0

        plan.append(generate_room(room_name, (x_cursor, y_cursor), size))

        x_cursor += room_width + 1
        row_height = max(row_height, room_height)

    return plan

def procedural_floorplan(prompt_keywords: List[str] = None) -> List[Room]:
    """
    Main function to generate a procedural layout from prompt keywords.
    If no keywords are given, defaults to a typical 2-bedroom layout.
    """
    if not prompt_keywords:
        prompt_keywords = ["living_room", "bedroom", "bedroom", "kitchen", "bathroom"]

    # Filter valid room types only
    filtered = [r for r in prompt_keywords if r in ROOM_TYPES.keys()]
    return arrange_rooms(filtered)


if __name__ == "__main__":
    # Example test run
    layout = procedural_floorplan()
    for room in layout:
        print(room)
