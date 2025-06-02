import streamlit as st
import random
import svgwrite

# --- Layout Parameters ---
room_templates = {
    "bedroom": {"min_size": (3, 3), "max_size": (4, 5)},
    "bathroom": {"min_size": (2, 2), "max_size": (2.5, 3)},
    "kitchen": {"min_size": (3, 3), "max_size": (4, 4)},
    "living": {"min_size": (4, 4), "max_size": (6, 5)},
    "dining": {"min_size": (3, 3), "max_size": (4, 4)},
    "garage": {"min_size": (3, 5), "max_size": (4, 6)},
}

# --- Generate Random Room ---
def random_room(name, offset_x, offset_y):
    size_x = round(random.uniform(*room_templates[name]["min_size"]), 1)
    size_y = round(random.uniform(*room_templates[name]["max_size"]), 1)
    return {"name": name, "x": offset_x, "y": offset_y, "w": size_x, "h": size_y}

# --- Layout Logic Engine ---
def generate_plan(num_bedrooms=3, has_garage=True):
    plan = []
    x, y = 0, 0

    # Living Room at Entry
    plan.append(random_room("living", x, y))
    y += 5

    # Kitchen and Dining Next
    plan.append(random_room("kitchen", x, y))
    x += 4
    plan.append(random_room("dining", x, y))
    y += 4
    x = 0

    # Bedrooms
    for i in range(num_bedrooms):
        plan.append(random_room("bedroom", x, y))
        x += 4
        plan.append(random_room("bathroom", x, y))  # Nearby bath
        x = 0
        y += 4

    # Garage if required
    if has_garage:
        plan.append(random_room("garage", x, y))

    return plan

# --- SVG Drawing Function ---
def draw_svg(plan):
    dwg = svgwrite.Drawing(size=("800px", "800px"))
    scale = 60  # meters to pixels
    for room in plan:
        x, y, w, h = room["x"] * scale, room["y"] * scale, room["w"] * scale, room["h"] * scale
        dwg.add(dwg.rect(insert=(x, y), size=(w, h), stroke='black', fill='lightgray', stroke_width=2))
        dwg.add(dwg.text(room["name"], insert=(x + 5, y + 15), font_size="14px", fill='black'))
    return dwg.tostring()

# --- Streamlit UI ---
st.set_page_config(page_title="AURA - Floor Plan Generator")
st.title("🏠 AURA - AI Architect: Random Floor Plan Generator")

st.write("Describe your project:")
bedrooms = st.slider("Number of Bedrooms", 1, 5, 3)
garage = st.checkbox("Include Garage", value=True)

if st.button("🧠 Generate Floor Plan"):
    floor_plan = generate_plan(bedrooms, has_garage=garage)
    svg_code = draw_svg(floor_plan)
    st.components.v1.html(svg_code, height=600, scrolling=True)
