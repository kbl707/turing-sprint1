import pytest
import streamlit as st
from pages.practice import initialize_session, display_practice_page

def test_role_input_validation():
    """Test role input validation."""
    # Initialize session
    initialize_session()
    
    # Test valid input
    st.session_state.role = "Software Engineer"
    assert len(st.session_state.role) <= 50
    
    # Test input at max length
    st.session_state.role = "A" * 50
    assert len(st.session_state.role) == 50
    
    # Test input exceeding max length
    st.session_state.role = "A" * 51
    assert len(st.session_state.role) <= 50  # Should be truncated

def test_category_selection():
    """Test category selection functionality."""
    # Initialize session
    initialize_session()
    
    # Test initial state
    assert st.session_state.category == ""
    
    # Test category selection
    categories = [
        "General Workplace",
        "Management & Leadership",
        "Military & Defense",
        "Computer Science & Engineering",
        "Marketing & Communications",
        "Healthcare & Medicine",
        "Finance & Banking",
        "Entrepreneurship & Startups",
        "Education & Training"
    ]
    
    # Test each category
    for category in categories:
        st.session_state.category = category
        assert st.session_state.category == category
        assert st.session_state.category in categories

def test_session_state_persistence():
    """Test that session state persists correctly."""
    # Initialize session
    initialize_session()
    
    # Set values
    st.session_state.role = "Test Role"
    st.session_state.category = "Test Category"
    
    # Verify persistence
    assert st.session_state.role == "Test Role"
    assert st.session_state.category == "Test Category"
    
    # Clear session
    st.session_state.clear()
    initialize_session()
    
    # Verify cleared state
    assert st.session_state.role == ""
    assert st.session_state.category == ""

if __name__ == "__main__":
    pytest.main([__file__]) 