import streamlit as st
import os
import base64

def main():
    st.set_page_config(
        page_title="Decision-Making Interview Preparation App",
        page_icon="🎯",
        layout="centered"
    )
    
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Load and encode logo
    with open(os.path.join("static", "logo.png"), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # Logo container with custom styling
    st.markdown(f"""
        <div class="logo-container">
            <img class="logo-img" src="data:image/png;base64,{encoded_string}">
        </div>
    """, unsafe_allow_html=True)
    
    # Main container
    with st.container():
        st.title("Sharpen Your Decision-Making Skills")
        st.markdown('<p style="font-size:20px; color:rgb(112, 112, 112); padding-bottom: 40px;">Prepare for your next big opportunity by practicing realistic decision-making scenarios tailored to your role and industry. Sharpen your critical thinking skills, explore different choices, and get valuable feedback to boost your interview performance. Ready to challenge yourself and grow? Let\'s get started!</p>', unsafe_allow_html=True)
        
        # Center the button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Practicing", type="primary"):
                st.switch_page("pages/practice.py")

if __name__ == "__main__":
    main() 