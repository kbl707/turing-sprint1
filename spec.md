
**Full Specification: Decision-Making Interview Preparation App**

---

# 1. Project Overview
A single-page web application built with **Streamlit** to help users practice decision-making scenarios for interview preparation.
The app dynamically generates realistic decision-making challenges using the **ChatGPT API**, provides multiple-choice options and/or text input fields for responses, and gives structured feedback at the end.

---

# 2. Core User Flow
1. Landing Page with tagline "Sharpen Your Decision-Making Skills" and "Start Practicing" button.
2. User enters their **role** via text input (optional; if blank, proceed anyway).
3. User selects a **category** from a **grid of 9 cards**:
   - General Workplace
   - Management & Leadership
   - Military & Defense
   - Computer Science & Engineering
   - Marketing & Communications
   - Healthcare & Medicine
   - Finance & Banking
   - Entrepreneurship & Startups
   - Education & Training
4. Immediately after clicking a category, user is presented with the first scenario.
5. For each scenario (10 total):
   - Read 3–5 sentence realistic decision-making scenario.
   - Text input to write a decision **and** optional 3–4 multiple-choice answers.
   - Progress tracker displayed as "Scenario X of 10."
   - Simple loading message: "Generating your next decision challenge..."
6. After 10 scenarios, display a **results page**:
   - General AI-generated feedback (few sentences).
   - One-sentence improvement suggestion.
   - Scenario-by-scenario feedback (comment + ideal decision suggestion).
7. "Start New Session" button at the end.

---

# 3. AI Behavior
- Generate scenarios dynamically via ChatGPT API.
- System Prompt for generation:
  - Short, concise scenarios (3–5 sentences).
  - Realistic, practical, no fantasy or absurd cases.
  - One clear decision point per scenario.
  - Medium difficulty by default.
  - 3–4 multiple-choice options, with one clearly being the best choice.
- Temperature: 0.3 (low creativity, focused outputs).
- Easy editability of OpenAI settings in the config/code.

---

# 4. Security & Validation
- **API key security:** Key stored securely server-side.
- **Rate limiting:** One request every few seconds to avoid abuse.
- **Session token budget control:** Soft limit on API token usage per 10 scenarios.
- **Input Validation:**
  - Length check for user role input.
  - Optional profanity filter.
  - ChatGPT used for light validation: input safety and system prompt safety.
  - Friendly error messages if invalid inputs (e.g., "Please enter a professional role title to continue.")
- **System Prompt Validation:**
  - AI meta-validation to ensure prompts are within expected behavior.

---

# 5. UI Elements
- Streamlit default fonts and colors.
- Landing page: tagline + "Start Practicing" button.
- Role input: simple text field.
- Category selection: grid of 9 cards.
- Scenario view: simple layout with decision text + multiple-choice.
- Progress indicator: "Scenario X of 10".
- Loading animation: simple spinner and text.
- Results page: all feedback shown on a single page.
- Footer: "Built in Turing College with ❤️ using Streamlit and OpenAI"

---

# 6. Data Handling
- No persistent storage.
- Session data (role, category, scenarios, responses) kept in memory (Streamlit session_state).
- On session end, feedback generated based on collected inputs.
- No user accounts or personal data collected.

---

# 7. Error Handling Strategy
- Display user-friendly error messages for input validation failures.
- Retry mechanism if ChatGPT API call fails once (with error message if repeated failure).
- Protect against empty/malformed API responses.
- Timeout limits on API requests.

---

# 8. Basic Project Structure

```
/ (root)
|— app.py (Main Streamlit app entrypoint)
|— prompts.py (System prompt templates and AI communication)
|— validation.py (User input validation and system prompt validation)
|— utils.py (Helper functions: loading animation, progress tracker, etc.)
|— requirements.txt (Python dependencies)
|— config.py (OpenAI API key, adjustable settings like temperature)
|— README.md (Project setup instructions)
```

**Streamlit Page Layout**
- Page 1: Landing page
- Page 2: Role input + Category selection
- Page 3: Scenario presentation (decision input + multiple choice)
- Page 4: Results page (feedback summary)

---

# 9. Future Improvements (Optional Post-MVP)
- Allow user to choose number of scenarios per session.
- Add difficulty selector (easy, medium, hard).
- Option to download session results as PDF.
- User accounts for saving history.
- Admin panel to monitor API usage/cost.

---

**End of Full Developer-Ready Specification**

---
