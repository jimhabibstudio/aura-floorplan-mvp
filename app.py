# app.py
# Main entry point for AURA One MVP - AI Floor Plan Generator

import streamlit as st
from frontend.ui import display_app

# Run the main app interface
def main():
    """
    Launch AURA One MVP Streamlit UI
    """
    display_app()

if __name__ == '__main__':
    main()
