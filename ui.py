# ui.py
# Streamlit UI for AURA One MVP - Floor Plan Generator

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from backend.procedural_generator import procedural_floorplan

def render_floor_plan(rooms):
    """
    Visualize the generated floor plan using Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_aspect('equal')
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.invert_yaxis()
    ax.axis('off')

    for room in rooms:
        rect = patches.Rectangle(
            (room['x'], room['y']),
            room['width'],
            room['height'],
            linewidth=2,
            edgecolor='black',
            facecolor='lightblue',
            label=room['name']
        )
        ax.add_patch(rect)
        ax.text(
            room['x'] + room['width']/2,
            room['y'] + room['height']/2,
            f"{room['name'].replace('_', ' ').title()}\n{room['width']}m x {room['height']}m",
            color='black',
            ha='center',
            va='center',
            fontsize=9
        )

    st.pyplot(fig)

def display_app():
    """
    Main interface for AURA One MVP in Streamlit.
    """
    st.set_page_config(page_title="AURA One - AI Floor Plan Generator", layout="centered")
    st.title("🏠 AURA One - Procedural Floor Plan Generator")
    st.markdown("Generate instant architecture layouts from a simple list of rooms.")

    with st.form("floorplan_form"):
        user_input = st.text_input(
            "Enter desired rooms (comma-separated):",
            "living_room, bedroom, bedroom, kitchen, bathroom"
        )
        submitted = st.form_submit_button("Generate Floor Plan")

    if submitted:
        rooms_requested = [r.strip().lower() for r in user_input.split(",") if r.strip() != ""]
        floor_plan = procedural_floorplan(rooms_requested)

        if floor_plan:
            st.success("✅ Floor plan generated successfully!")
            render_floor_plan(floor_plan)
        else:
            st.error("❌ No valid room types provided. Please enter known room types.")
