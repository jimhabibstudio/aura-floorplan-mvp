# layout_optimizer.py
# AURA One MVP - Optional AI Layout Optimization Module

from typing import List, Dict
import random

Room = Dict[str, any]


def optimize_layout(rooms: List[Room]) -> List[Room]:
    """
    Placeholder for optimizing layout order using simple heuristics.
    Later this can use ML models or graph-based spatial optimization.
    For now, we'll group functional adjacencies: bedrooms near bathrooms, etc.
    """
    bedroom_zone = [room for room in rooms if "bedroom" in room['name']]
    bathroom_zone = [room for room in rooms if "bathroom" in room['name']]
    kitchen_zone = [room for room in rooms if "kitchen" in room['name']]
    living_zone = [room for room in rooms if "living" in room['name'] or "dining" in room['name']]
    other = [room for room in rooms if room not in bedroom_zone + bathroom_zone + kitchen_zone + living_zone]

    # Concatenate in functional flow order
    optimized = living_zone + kitchen_zone + bathroom_zone + bedroom_zone + other
    
    # Shuffle slightly to simulate a more dynamic plan
    if len(optimized) > 3:
        random.shuffle(optimized[1:-1])

    return optimized


if __name__ == "__main__":
    # Sample data to test
    test_rooms = [
        {'name': 'bedroom'}, {'name': 'bathroom'}, {'name': 'kitchen'},
        {'name': 'living_room'}, {'name': 'storage'}
    ]
    print("Before Optimization:", [r['name'] for r in test_rooms])
    result = optimize_layout(test_rooms)
    print("After Optimization:", [r['name'] for r in result])
