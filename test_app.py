import streamlit as st
from app import main

def test_app_elements():
    # Mock Streamlit elements
    st.title = lambda x: x
    st.subheader = lambda x: x
    st.button = lambda x, type: x
    
    # Test if main function runs without errors
    try:
        main()
        assert True
    except Exception as e:
        assert False, f"Main function failed with error: {str(e)}" 