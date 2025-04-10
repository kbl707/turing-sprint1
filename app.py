import streamlit as st

def main():
    st.set_page_config(
        page_title="Decision-Making Interview Preparation App",
        page_icon="🎯",
        layout="centered"
    )
    
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Main container
    with st.container():
        st.title("Sharpen Your Decision-Making Skills")
        st.markdown("Prepare for your next big opportunity by practicing realistic decision-making scenarios tailored to your role and industry. Sharpen your critical thinking skills, explore different choices, and get valuable feedback to boost your interview performance. Ready to challenge yourself and grow? Let’s get started!")
        
        # Center the button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Practicing", type="primary"):
                st.session_state.started = True
                st.rerun()

if __name__ == "__main__":
    main() 