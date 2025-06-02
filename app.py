# AURA MVP: COMPONENT 1 - Prompt to Floor Plan Generator (Fallback Included)

import streamlit as st
import svgwrite
from openai import OpenAI, OpenAIError

# --- SETUP ---
st.set_page_config(page_title="AURA | Floor Plan AI", layout="centered")
st.title("🏠 AURA - Instant Floor Plan Generator")
st.markdown("Describe your building and get an instant sketch of your floor plan!")

# --- INIT OPENAI (Safely) ---
use_mock = False
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    use_mock = True
    st.warning("🔁 Running in demo mode. No OpenAI key or billing available.")

# --- USER PROMPT ---
prompt = st.text_area(
    "✏️ Describe your building (e.g. 3-bedroom bungalow with kitchen, 2 baths, and dining):"
)

if st.button("Generate Floor Plan") and prompt:
    st.info("🧠 Generating layout...")

    # --- STEP 1: TRY TO USE OPENAI ---
    if not use_mock:
        try:
            system_msg = """
            You are an expert architect AI. From the user prompt, extract rooms and their approximate sizes (in meters).
            Return a clean list. Example:
            Living Room: 6x5
            Kitchen: 4x3
            Bedroom 1: 4x4
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            room_text = response.choices[0].message.content.strip()
            room_list = room_text.split("\n")

        except Exception as e:
            st.warning(f"⚠️ Could not reach OpenAI. Switching to mock layout. ({str(e)})")
            use_mock = True

    # --- STEP 2: MOCK DATA IF NEEDED ---
    if use_mock:
        room_list = [
            "Living Room: 6x5",
            "Kitchen: 4x3",
            "Bedroom 1: 4x4",
            "Bedroom 2: 4x3",
            "Toilet: 2x2"
        ]
        st.info("🧪 Using sample data to demonstrate layout rendering.")

    # --- STEP 3: SVG LAYOUT GENERATOR ---
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
        except:
            st.warning(f"Could not draw: {room}")

    svg_code = dwg.tostring()
    st.subheader("🧩 Floor Plan Sketch")
    st.image(svg_code, use_container_width=True, caption="Concept sketch (not to scale)")

    st.download_button("⬇️ Download SVG", data=svg_code, file_name="floorplan.svg", mime="image/svg+xml")
