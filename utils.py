import streamlit as st
import time

def display_progress(current, total):
    """Display a progress bar for the current scenario."""
    progress = current / total
    st.progress(progress)
    st.markdown(f"**Progress:** {current} of {total} scenarios completed")

def show_loading(message="Loading..."):
    """Context manager to show a loading spinner with message."""
    return st.spinner(message)

def rate_limit():
    """Simple rate limiting to avoid API abuse."""
    time.sleep(1)  # 1 second delay between API calls 