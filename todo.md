
# ✅ TODO Checklist - Decision-Making Interview Preparation App

## 🚀 Project Setup & Initial Configuration
- [x] Set up Python virtual environment (`venv` or `conda`)
- [x] Install Streamlit (`pip install streamlit`)
- [x] Install OpenAI Python client (`pip install openai`)
- [x] Initialize Git repository and commit initial setup

## 📁 Project Structure
- [x] Create root folder structure (`app.py`, `prompts.py`, `validation.py`, `utils.py`, `config.py`, `requirements.txt`)
- [x] Add `.gitignore` for Python projects

## 🔑 OpenAI API Integration
- [x] Register OpenAI account and obtain API key
- [x] Store OpenAI API key securely in environment variables
- [ ] Implement API call function in `prompts.py`

## 🎨 User Interface Setup (Streamlit)
- [ ] Implement landing page (`app.py`):
  - [ ] Add title and subtitle
  - [ ] Add "Start Practicing" button
- [ ] Create role input field with validation (max 50 chars)
- [ ] Develop category selection grid layout

## 🤖 Scenario Generation & API Integration
- [ ] Write system prompt in `prompts.py` for scenario generation
- [ ] Integrate dynamic scenario generation with OpenAI API
- [ ] Test scenario fetching and handling

## 📑 Scenario Display & Interaction
- [ ] Display scenarios with decision text and multiple-choice answers
- [ ] Add text input for user's decision and option selection UI
- [ ] Implement progress tracker ("Scenario X of 10")

## 💾 Session Management & Data Handling
- [ ] Implement Streamlit `session_state` management
- [ ] Store user inputs securely between scenarios
- [ ] Test session persistence and data integrity

## 📊 Feedback & Results Generation
- [ ] Generate general feedback, improvement suggestions, and scenario-specific feedback via API
- [ ] Display structured feedback in results page
- [ ] Implement "Start New Session" reset functionality

## 🔒 Security, Validation & Robustness
- [ ] Add input validation (role length, profanity check) in `validation.py`
- [ ] Implement rate-limiting (one request per 2 seconds)
- [ ] Set up error handling and retry mechanisms for API calls

## 🧪 Testing & Quality Assurance
- [ ] Write and execute tests for UI components
- [ ] Write and execute tests for API integration
- [ ] Write and execute tests for input validation and error handling

## 📖 Documentation & Deployment (Optional)
- [ ] Write `README.md` with setup instructions and usage examples
- [ ] Document project dependencies in `requirements.txt`
- [ ] Deploy Streamlit app (optional)

## 🎯 Future Enhancements (Post-MVP)
- [ ] Allow custom number of scenarios per session
- [ ] Add scenario difficulty levels (easy, medium, hard)
- [ ] Option to download session results as PDF
- [ ] Implement user accounts for saving history
- [ ] Admin panel for monitoring API usage and costs
