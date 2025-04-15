
# Decision-Making Interview Preparation App - Prompt Engineering Plan

## 📝 Step-by-Step Project Blueprint

## /spec.md

## ✅ Fine-Grained Prompt Engineering for Code Generation

### Prompt 1: Project Initialization & Streamlit Setup

```
Create a basic Python Streamlit app named "Decision-Making Interview Preparation App". 
The entry point file should be `app.py`. The page should display:
- A clear title: "Sharpen Your Decision-Making Skills".
- A subtitle with the text: "Prepare for realistic scenarios and improve your responses".
- A large primary button: "Start Practicing".

Provide tests to confirm Streamlit correctly renders these elements.
```

### Prompt 2: OpenAI API Integration

```
Implement secure integration with OpenAI API in Python. Create `config.py` to store the API key securely using environment variables. Create `prompts.py` with a function `fetch_openai_completion(prompt: str)` to handle API requests, set at temperature 0.3. 
Include tests to verify API connectivity and correct handling of typical responses and failures.
```

### Prompt 3: User Input & Category Selection Interface

```
Expand `app.py` to include:
- A text input field labeled "Enter your professional role (optional)" with input validation (no more than 50 chars).
- A grid layout displaying nine selectable cards/categories as per specification.
- Capture user inputs and selected category in Streamlit session state for later use.

Write tests confirming the input field and category selection are correctly captured and validated.
```

### Prompt 4: Scenario Generation & Display

```
Enhance the app to dynamically generate realistic decision-making scenarios using the OpenAI API. 
Define a structured *system* prompt in `prompts.py` that clearly instructs the AI to produce concise, practical scenarios (3–5 sentences), each containing one clear decision point with 3–4 multiple-choice answers.

On category selection, fetch and display the first scenario, including the decision description and multiple-choice options, in a clear Streamlit layout.

Include comprehensive tests for scenario fetching, response structure, and error conditions (e.g., empty response handling).
```

### Prompt 5: Session State & Progress Tracking

```
Add session management to track user progress through 10 scenarios using Streamlit’s `session_state`. 
Implement a visible progress indicator ("Scenario X of 10") on the scenario display page.

Provide mechanisms for storing each user decision input securely in session state.

Write thorough tests ensuring scenario progression and session state management operate correctly without losing data between steps.
```

### Prompt 6: Feedback Generation & Result Display

```
Create a results page in `app.py` to summarize the user session.
At the end of 10 scenarios:
- Use OpenAI API to generate general feedback, one-sentence improvement suggestion, and detailed scenario-by-scenario comments.
- Display results clearly with Streamlit components.

Include a "Start New Session" button to reset the state.

Provide robust tests validating feedback correctness, session completion logic, and reset functionality.
```

### Prompt 7: Security, Input Validation & Error Handling

```
Strengthen the app security and robustness by implementing in `validation.py`:
- Role input length checks and optional profanity filtering using a lightweight library or custom regex.
- Simple rate-limiting for API requests (one request every 2 seconds).
- API request retry mechanism and clear, friendly error messages in the UI for various failure conditions.

Write detailed tests verifying security mechanisms, input validations, rate-limiting functionality, and robust error handling.
```
