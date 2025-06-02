AURA MVP: Floor Plan Sketcher 2.1 - With Room Adjacency Logic & Realistic Layouts

import streamlit as st import svgwrite

--- PAGE SETUP ---

st.set_page_config(page_title="AURA | Floor Plan AI", layout="centered") st.title("🏠 AURA - Smarter Floor Plan Generator") st.markdown("Describe your building layout, and AURA will draw a more architecturally accurate floor plan with logical adjacency.")

--- INPUT ---

prompt = st.text_area("📋 Enter your building brief (e.g. 3-bedroom with living room, kitchen, bath, etc):")

--- ROOM PLACEMENT LOGIC WITH ADJACENCY ---

def create_adjacency_layout(rooms): layout = [] x, y = 20, 20 row_height = 0

adjacency_map = {
    "Living Room": ["Dining", "Kitchen"],
    "Kitchen": ["Dining"],
    "Bedroom 1": ["Bathroom"],
    "Bedroom 2": ["Bathroom"],
}

placed = set()
for room_name, w, h in rooms:
    if room_name in placed:
        continue
    group = [(room_name, w, h)]
    placed.add(room_name)

    # Add adjacent rooms
    for adj_name in adjacency_map.get(room_name, []):
        for r_name, rw, rh in rooms:
            if r_name == adj_name and r_name not in placed:
                group.append((r_name, rw, rh))
                placed.add(r_name)

    max_h = 0
    for r_name, rw, rh in group:
        layout.append({"name": r_name, "x": x, "y": y, "w": rw, "h": rh})
        x += rw * 40 + 20
        max_h = max(max_h, rh * 40)
    x = 20
    y += max_h + 20

return layout

--- DRAW FUNCTION ---

def draw_svg_plan(layout): dwg = svgwrite.Drawing(size=(1000, 800))

for room in layout:
    w_px = room['w'] * 40
    h_px = room['h'] * 40
    x = room['x']
    y = room['y']

    # Walls
    dwg.add(dwg.rect(insert=(x, y), size=(w_px, h_px), fill='white', stroke='black', stroke_width=3))
    
    # Room label
    dwg.add(dwg.text(room['name'], insert=(x + 10, y + 20), font_size='14px', fill='black'))

    # Door indicator at bottom center
    dwg.add(dwg.rect(insert=(x + w_px/2 - 5, y + h_px - 5), size=(10, 10), fill='brown'))

return dwg.tostring()

--- MOCK INTELLIGENT PARSER ---

def mock_parse(prompt_text): return [ ("Living Room", 6, 5), ("Kitchen", 4, 3), ("Dining", 4, 3), ("Bedroom 1", 4, 4), ("Bedroom 2", 4, 3), ("Bathroom", 2, 2), ]

--- MAIN ---

if st.button("Generate Floor Plan") and prompt: rooms = mock_parse(prompt) layout = create_adjacency_layout(rooms) svg_code = draw_svg_plan(layout)

st.subheader("🧩 Updated Floor Plan Sketch")
st.image(svg_code, use_container_width=True)
st.download_button("⬇️ Download SVG", data=svg_code, file_name="floorplan.svg", mime="image/svg+xml")

