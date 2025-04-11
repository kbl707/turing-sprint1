import streamlit as st
from prompts import generate_scenario, generate_feedback
from utils import display_progress, show_loading
import config

def initialize_session():
    """Initialize session state variables if they don't exist."""
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = 0
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'role' not in st.session_state:
        st.session_state.role = ""
    if 'category' not in st.session_state:
        st.session_state.category = ""

def display_practice_page():
    """Display the practice page with role input and category selection."""
    st.title("Practice Decision-Making Scenarios")
    st.markdown("""
    Select your professional role and choose a category to start practicing realistic decision-making scenarios.
    Each scenario will present you with a challenging situation and multiple options to choose from.
    """)
    
    # Category selection grid
    st.subheader("Select a Category")
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
    
    # Create a 3x3 grid of cards
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            # Create a card-like button with consistent height
            if st.button(
                category,
                key=f"category_{i}",
                use_container_width=True,
                help=f"Practice {category} scenarios"
            ):
                st.session_state.category = category
                st.session_state.page = "scenario"
                st.experimental_rerun()
    
    # Role input below categories
    role = st.text_input(
        "Enter your professional role (optional)",
        value=st.session_state.role,
        max_chars=50,
        placeholder="Enter your professional role (optional)",
        label_visibility="collapsed"
    )
    if role:
        st.session_state.role = role
    
    # Submit button aligned to the right
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Submit →", type="primary", use_container_width=True):
            if not st.session_state.category:
                st.error("Please select a category to continue")
            else:
                st.session_state.page = "scenario"
                st.experimental_rerun()

def display_scenario():
    """Display the current scenario and collect response."""
    if st.session_state.current_scenario >= len(st.session_state.scenarios):
        # Generate new scenario
        with show_loading("Generating your next decision challenge..."):
            scenario = generate_scenario(
                st.session_state.category,
                st.session_state.role
            )
            st.session_state.scenarios.append(scenario)
    
    scenario = st.session_state.scenarios[st.session_state.current_scenario]
    
    st.title(f"Scenario {st.session_state.current_scenario + 1} of 10")
    st.markdown(scenario['description'])
    
    # Display multiple choice options
    selected_option = st.radio(
        "Select your decision:",
        scenario['options'],
        key=f"option_{st.session_state.current_scenario}"
    )
    
    # Additional text input for explanation
    explanation = st.text_area(
        "Explain your decision (optional):",
        key=f"explanation_{st.session_state.current_scenario}"
    )
    
    if st.button("Submit"):
        st.session_state.responses.append({
            'scenario': scenario,
            'selected_option': selected_option,
            'explanation': explanation
        })
        st.session_state.current_scenario += 1
        
        if st.session_state.current_scenario >= 10:
            st.session_state.page = "results"
        st.experimental_rerun()

def display_results():
    """Display the results page with feedback."""
    st.title("Practice Session Results")
    
    with show_loading("Generating your feedback..."):
        feedback = generate_feedback(st.session_state.responses)
    
    st.markdown("### Overall Feedback")
    st.markdown(feedback['overall'])
    
    st.markdown("### Improvement Suggestion")
    st.markdown(feedback['suggestion'])
    
    st.markdown("### Detailed Feedback")
    for i, (response, scenario_feedback) in enumerate(zip(st.session_state.responses, feedback['detailed'])):
        with st.expander(f"Scenario {i + 1}"):
            st.markdown(f"**Your Decision:** {response['selected_option']}")
            if response['explanation']:
                st.markdown(f"**Your Explanation:** {response['explanation']}")
            st.markdown(f"**Feedback:** {scenario_feedback}")
    
    if st.button("Start New Session"):
        st.session_state.clear()
        st.session_state.page = "practice"
        st.experimental_rerun()

def main():
    """Main function to run the practice app."""
    st.set_page_config(
        page_title="Decision-Making Practice",
        page_icon="🎯",
        layout="wide"
    )
    
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    initialize_session()
    
    if 'page' not in st.session_state:
        st.session_state.page = "practice"
    
    if st.session_state.page == "practice":
        display_practice_page()
    elif st.session_state.page == "scenario":
        display_scenario()
    elif st.session_state.page == "results":
        display_results()

if __name__ == "__main__":
    main()