# app.py
# AURA One MVP - Entry Point

import streamlit as st
from frontend.ui import display_app

# ====== MAIN STREAMLIT ENTRY POINT ======
def main():
    """
    Entry point that launches the Streamlit interface.
    """
    st.set_page_config(page_title="AURA One MVP", layout="wide")
    display_app()


if __name__ == "__main__":
    main()
