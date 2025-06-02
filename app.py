# AURA MVP: COMPONENT 1 - Prompt to Floor Plan Generator (Lightweight Version)

import streamlit as st
import svgwrite
from openai import OpenAI

# --- SETUP ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AURA | Floor Plan AI", layout="centered")
st.title("🏠 AURA - Instant Floor Plan Generator")
st.markdown("Type your building requirements below, and get a generated floor plan sketch in seconds.")

# --- PROMPT INPUT ---
prompt = st.text_area(
    "✏️ Describe your building (e.g. 3-bedroom bungalow in Lagos with open kitchen, 2 baths, modern style):"
)

if st.button("Generate Floor Plan") and prompt:
    with st.spinner("Thinking like an architect..."):

        # --- STEP 1: PARSE ROOMS FROM GPT ---
        system_msg = """
        You are an expert architect AI. Extract rooms and their approximate sizes (in meters) from user prompt. 
        Respond with a list of rooms and sizes, e.g.
        Living Room: 6x5
        Kitchen: 4x3
        Bedroom 1: 4x4
        Bedroom 2: 4x3
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            room_text = response.choices[0].message.content.strip()
            room_list = room_text.split("\n")
        except Exception as e:
            st.error(f"Failed to parse layout. Try a simpler description. Error: {str(e)}")
            st.stop()

        # --- STEP 2: DRAW SVG ---
        dwg = svgwrite.Drawing(size=(800, 600))
        x, y = 10, 10
        gap = 10

        for room in room_list:
            try:
                name, size = room.split(":")
                width_m, height_m = map(float, size.strip().lower().replace("m", "").split("x"))
                width_px = width_m * 40
                height_px = height_m * 40
                dwg.add(dwg.rect(insert=(x, y), size=(width_px, height_px), fill='lightblue', stroke='black'))
                dwg.add(dwg.text(name.strip(), insert=(x + 5, y + 20), font_size='14px', fill='black'))
                y += height_px + gap
            except Exception as e:
                st.warning(f"Could not draw room: {room}")

        # --- STEP 3: DISPLAY SVG ---
        st.subheader("🧩 Generated Floor Plan Sketch")
        svg_code = dwg.tostring()
        st.image(dwg.tostring(), use_column_width=True, caption="Not to scale - demo layout")

        # --- STEP 4: Download Link ---
        st.download_button("⬇️ Download SVG", data=svg_code, file_name="floorplan.svg", mime="image/svg+xml")
