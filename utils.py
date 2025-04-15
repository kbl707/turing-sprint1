import streamlit as st
import time

def display_progress(current: int, total: int):
    """Display a progress bar for the current session."""
    progress = current / total
    st.progress(progress)
    st.markdown(f"**Progress:** {current}/{total} scenarios completed")

def show_loading(message: str):
    """Context manager to display a loading message while a task is running."""
    class LoadingContext:
        def __init__(self, message):
            self.message = message
            self.placeholder = None
            
        def __enter__(self):
            self.placeholder = st.empty()
            self.placeholder.info(self.message)
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.placeholder:
                self.placeholder.empty()
            return False  # Don't suppress exceptions
    
    return LoadingContext(message)

def rate_limit():
    """Simple rate limiting to avoid API abuse."""
    time.sleep(1)  # 1 second delay between API calls 