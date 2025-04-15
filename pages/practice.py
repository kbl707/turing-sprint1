import streamlit as st
from prompts import generate_scenario, generate_feedback
from utils import display_progress, show_loading
from validation import validate_role, rate_limit, sanitize_input, handle_api_error
import config
import json
import os
import time

def save_session():
    """Save session state to a file."""
    session_data = {
        'current_scenario': st.session_state.current_scenario,
        'scenarios': st.session_state.scenarios,
        'responses': st.session_state.responses,
        'role': st.session_state.role,
        'category': st.session_state.category,
        'page': st.session_state.page
    }
    with open('session_data.json', 'w') as f:
        json.dump(session_data, f)

def load_session():
    """Load session state from a file if it exists."""
    if os.path.exists('session_data.json'):
        try:
            with open('session_data.json', 'r') as f:
                session_data = json.load(f)
                for key, value in session_data.items():
                    st.session_state[key] = value
        except Exception as e:
            st.error(f"Error loading session: {str(e)}")
            initialize_session()

def initialize_session():
    """Initialize session state variables"""
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = 0
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    if 'explanation' not in st.session_state:
        st.session_state.explanation = None
    if 'category' not in st.session_state:
        st.session_state.category = None
    if 'page' not in st.session_state:
        st.session_state.page = "practice"
    if 'first_scenarios' not in st.session_state:
        st.session_state.first_scenarios = {
            "Professional Development": {
                "description": "You're a junior developer who just discovered a critical security vulnerability in the production code. The fix is simple but requires a database migration that could cause a 5-minute downtime. The vulnerability could potentially expose customer data. What do you do?",
                "options": [
                    "Fix it immediately without telling anyone to avoid panic",
                    "Report it to your manager and suggest a maintenance window",
                    "Document it and add it to the next sprint planning",
                    "Discuss it with the team lead and propose a hotfix"
                ],
                "best_option": 1
            },
            "Leadership": {
                "description": "Your team is behind schedule on a critical project. The client is expecting delivery next week, but your team estimates they need two more weeks. The team is already working overtime and showing signs of burnout. What do you do?",
                "options": [
                    "Push the team harder to meet the deadline",
                    "Ask the client for an extension",
                    "Cut corners to deliver on time",
                    "Reallocate resources from other projects"
                ],
                "best_option": 1
            },
            "Team Management": {
                "description": "Two of your team members are in constant conflict, affecting team morale and productivity. One is more experienced but resistant to change, while the other is innovative but sometimes dismissive of established practices. What do you do?",
                "options": [
                    "Let them work it out themselves",
                    "Separate them into different projects",
                    "Facilitate a mediation session",
                    "Assign them to work together more closely"
                ],
                "best_option": 2
            },
            "Conflict Resolution": {
                "description": "A team member consistently takes credit for others' work in meetings. This is causing resentment among the team. The person is otherwise a good performer. What do you do?",
                "options": [
                    "Call them out publicly in the next meeting",
                    "Have a private conversation about teamwork",
                    "Ignore it to avoid conflict",
                    "Document instances for HR"
                ],
                "best_option": 1
            },
            "Time Management": {
                "description": "You have three urgent tasks due by the end of the day: a client presentation, a code review, and preparing for tomorrow's team meeting. You can only complete two of them. What do you do?",
                "options": [
                    "Work late to complete all three",
                    "Delegate the code review to a team member",
                    "Reschedule the team meeting",
                    "Ask for help with the presentation"
                ],
                "best_option": 1
            },
            "Communication": {
                "description": "You need to communicate a major change in project direction that will require significant rework. The team is already stressed about current deadlines. What do you do?",
                "options": [
                    "Announce it in the next team meeting",
                    "Send a detailed email to everyone",
                    "Meet with team leads first, then the whole team",
                    "Schedule individual meetings with each team member"
                ],
                "best_option": 2
            },
            "Problem Solving": {
                "description": "A critical production system is down, and the error logs are unclear. The team is divided on the root cause. What do you do?",
                "options": [
                    "Try the most popular solution first",
                    "Roll back to the last stable version",
                    "Gather more data before making a decision",
                    "Split the team to try different approaches"
                ],
                "best_option": 2
            },
            "Strategic Thinking": {
                "description": "Your company is considering adopting a new technology that could give you a competitive edge but requires significant retraining. The current system is stable but becoming outdated. What do you do?",
                "options": [
                    "Stick with the current system until it's completely obsolete",
                    "Immediately switch to the new technology",
                    "Run a pilot project with the new technology",
                    "Form a committee to study the options"
                ],
                "best_option": 2
            },
            "Project Management": {
                "description": "Your project is at risk of missing its deadline due to unexpected technical challenges. The client is adamant about the original timeline. What do you do?",
                "options": [
                    "Cut features to meet the deadline",
                    "Request more resources from management",
                    "Negotiate a new timeline with the client",
                    "Ask the team to work overtime"
                ],
                "best_option": 2
            }
        }

def display_progress_bar():
    """Display a progress bar for the current session."""
    if st.session_state.page == "scenario":
        progress = st.session_state.current_scenario / 10
        st.progress(progress)
        # st.markdown(f"**Progress:** {st.session_state.current_scenario}/10 scenarios completed")

def display_practice_page():
    """Display the practice page with role input and category selection"""
    st.markdown('<h1 style="text-align: center;">Practice Decision-Making Scenarios</h1>', unsafe_allow_html=True)
    
    # Category selection
    st.markdown("### Select a Category")
    categories = [
        "Professional Development",
        "Leadership",
        "Team Management",
        "Conflict Resolution",
        "Time Management",
        "Communication",
        "Problem Solving",
        "Strategic Thinking",
        "Project Management"
    ]
    
    # Create a grid of category buttons
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            if st.button(category, key=f"category_{i}", use_container_width=True):
                st.session_state.category = category
                st.session_state.page = "scenario"
                # Use pre-generated first scenario
                st.session_state.scenarios = [st.session_state.first_scenarios[category]]
                st.session_state.current_scenario = 0
                st.rerun()
    
    # Role input
    role = st.text_input("Enter your role (optional):", key="role_input")
    if role:
        try:
            validate_role(role)
            st.session_state.role = role
        except ValueError as e:
            st.error(str(e))

@st.cache_data(ttl=300)  # Cache for 5 minutes
def generate_cached_scenario(category: str, role: str, previous_scenarios: list):
    """Generate a scenario with caching"""
    try:
        return generate_scenario(category, role, previous_scenarios)
    except Exception as e:
        st.error(f"Failed to generate scenario: {str(e)}")
        return None

def display_scenario():
    """Display the current scenario and collect user input"""
    # Check if we've completed all scenarios
    if st.session_state.current_scenario >= 10:
        display_results()
        return
    
    # Initialize next_scenario in session state if not present
    if 'next_scenario' not in st.session_state:
        st.session_state.next_scenario = None
    
    # Check if we need to generate a new scenario
    if st.session_state.current_scenario >= len(st.session_state.scenarios):
        # Check rate limit before generating
        if not rate_limit():
            # Add a small delay to prevent rapid reruns
            time.sleep(0.5)
            st.rerun()
            return
            
        try:
            with show_loading("Generating your next decision challenge..."):
                new_scenario = generate_scenario(
                    category=st.session_state.category,
                    role=st.session_state.get('role', ''),
                    previous_scenarios=st.session_state.scenarios
                )
                if not new_scenario:
                    raise Exception("Failed to generate scenario - no response from API")
                st.session_state.scenarios.append(new_scenario)
        except Exception as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower():
                st.error("API rate limit reached. Please wait a moment and try again.")
            elif "timeout" in error_msg.lower():
                st.error("Request timed out. Please try again.")
            else:
                st.error(f"Error generating scenario: {error_msg}")
            if st.button("Retry Scenario Generation", key=f"retry_scenario_{int(time.time())}"):
                st.rerun()
            return
    
    scenario = st.session_state.scenarios[st.session_state.current_scenario]
    
    # Display scenario description
    st.header(f"Scenario {st.session_state.current_scenario + 1}")
    st.markdown(scenario['description'])
    
    # Create a form for the scenario
    with st.form(key=f"scenario_form_{st.session_state.current_scenario}"):
        # Display options
        st.markdown("**Decision options:**")
        option = st.radio(
            "Decision options",
            scenario['options'],
            key=f"temp_option_{st.session_state.current_scenario}",
            label_visibility="collapsed"
        )
        
        # Explanation input
        st.markdown("**Explanation (optional):**")
        explanation = st.text_area(
            "Decision explanation",
            key=f"temp_explanation_{st.session_state.current_scenario}",
            label_visibility="collapsed"
        )
        
        # Submit button
        if st.form_submit_button("Submit"):
            st.session_state.selected_option = option
            st.session_state.explanation = explanation
            
            # Store the response
            st.session_state.responses.append({
                'scenario': scenario,
                'selected_option': option,
                'explanation': explanation
            })
            
            # Move to next scenario
            st.session_state.current_scenario += 1
            
            # If we have a pre-generated next scenario, use it
            if st.session_state.next_scenario:
                st.session_state.scenarios.append(st.session_state.next_scenario)
                st.session_state.next_scenario = None
            
            st.rerun()
    
    # Progress and back link
    st.markdown(f"**Progress:** {st.session_state.current_scenario}/10 scenarios completed")
    if st.button("← Choose other scenario", key="back_to_selection", use_container_width=False):
        st.session_state.current_scenario = 0
        st.session_state.scenarios = []
        st.session_state.responses = []
        st.session_state.selected_option = None
        st.session_state.explanation = None
        st.session_state.page = "practice"
        st.rerun()
    
    # Generate next scenario in the background if not already generating
    if st.session_state.current_scenario < 9 and not st.session_state.next_scenario:
        try:
            next_scenario = generate_cached_scenario(
                category=st.session_state.category,
                role=st.session_state.get('role', ''),
                previous_scenarios=st.session_state.scenarios
            )
            if next_scenario:
                st.session_state.next_scenario = next_scenario
        except Exception as e:
            # Don't show error for background generation
            pass

def display_results():
    """Display the results page with brief feedback"""
    st.title("Practice Session Results")
    
    try:
        with show_loading("Generating your feedback..."):
            feedback = generate_feedback(st.session_state.responses)
        
        # Display score
        st.markdown("### Your Score")
        st.markdown(f"**{feedback['correct_count']}/10** correct answers")
        
        # Display feedback
        st.markdown("### Feedback")
        st.markdown(feedback['feedback'])
        
        # Display key suggestion
        st.markdown("### Key Suggestion")
        st.markdown(feedback['suggestion'])
        
        # Display each scenario as an expandable button
        st.markdown("### Your Answers")
        for i, response in enumerate(st.session_state.responses, 1):
            is_correct = response['selected_option'] == response['scenario']['options'][response['scenario']['best_option']]
            symbol = "✅" if is_correct else "❌"
            color = "green" if is_correct else "red"
            correct_answer = response['scenario']['options'][response['scenario']['best_option']]
            
            with st.expander(f"{symbol} Scenario {i}: {response['selected_option']}", expanded=False):
                st.markdown(f"**Question:** {response['scenario']['description']}")
                st.markdown("**Options:**")
                for option in response['scenario']['options']:
                    if option == response['selected_option']:
                        st.markdown(f"<span style='color: {color};'>• {option} (Your choice)</span>", unsafe_allow_html=True)
                    elif option == correct_answer:
                        st.markdown(f"<span style='color: green;'>• {option} (Correct answer)</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"• {option}")
                if response['explanation']:
                    st.markdown(f"**Your explanation:** {response['explanation']}")
        
        # Start new session button with proper reboot mechanism
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Start New Session", type="primary", key="start_new_session"):
                # Clear all session state variables
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                # Initialize fresh session
                initialize_session()
                # Force a complete app rerun
                st.experimental_rerun()
            
    except Exception as e:
        st.error("An error occurred while generating feedback. Please try again.")
        if st.button("Retry Feedback Generation", key=f"retry_feedback_{int(time.time())}"):
            st.rerun()

def main():
    """Main function for the practice page"""
    # Add custom CSS for scrolling and layout
    st.markdown("""
        <style>
            .stApp {
                overflow: auto;
            }
            .main .block-container {
                max-width: 800px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            div[data-testid="stVerticalBlock"] {
                gap: 1rem;
            }
            div[data-testid="stMarkdown"] {
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session()
    
    # Check if we're on the practice page
    if st.session_state.get('page') == 'practice':
        display_practice_page()
        return
    
    # Check if we've completed all scenarios
    if st.session_state.current_scenario >= 10:
        display_results()
        return
    
    # Display current scenario
    display_scenario()

if __name__ == "__main__":
    main()