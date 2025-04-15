from openai import OpenAI
from config import OPENAI_API_KEY
import json
import streamlit as st
import time
from typing import List, Dict

# Configure OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# System prompt for scenario generation
SCENARIO_SYSTEM_PROMPT = """
You are an expert in creating realistic decision-making scenarios for professional development.
Your task is to generate concise, practical scenarios that:
1. Are 3-5 sentences long
2. Present one clear decision point
3. Include exactly 4 multiple choice options
4. Have one clearly best choice
5. Are realistic and relevant to the given category
6. Challenge the user's decision-making skills
7. Are unique and different from previous scenarios

Format your response as a JSON object with:
{
    "description": "The scenario description",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "best_option": "The index of the best option (0-based)"
}
"""

# System prompt for feedback generation
FEEDBACK_SYSTEM_PROMPT = """
You are an expert in providing constructive feedback on decision-making skills.
Your task is to analyze the user's responses and provide:
1. Overall assessment of decision-making skills
2. One specific, actionable improvement suggestion
3. Detailed feedback for each scenario

The feedback should be:
- Professional and constructive
- Focus on decision-making process, not just outcomes
- Include specific examples from responses
- Suggest concrete improvements
- Be encouraging while highlighting areas for growth

Format your response as a JSON object with:
{
    "overall": "Overall assessment of decision-making skills",
    "suggestion": "One specific improvement suggestion",
    "detailed": [
        {
            "scenario": "Brief scenario description",
            "selected_option": "User's selected option",
            "explanation": "User's explanation if provided",
            "feedback": "Detailed feedback on this specific decision",
            "strengths": ["List of strengths shown in this decision"],
            "improvements": ["List of specific improvements for this decision"]
        }
    ]
}
"""

def fetch_openai_completion(prompt: str) -> str:
    """Fetch completion from OpenAI API with error handling"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            timeout=30  # 30 second timeout
        )
        
        if not response.choices:
            raise ValueError("No choices in response")
            
        if not response.choices[0].message:
            raise ValueError("No message in first choice")
            
        content = response.choices[0].message.content
        
        # Clean up markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        if content.startswith("```"):
            content = content[3:]  # Remove ```
        if content.endswith("```"):
            content = content[:-3]  # Remove ```
            
        return content.strip()
        
    except Exception as e:
        error_msg = str(e).lower()
        if "timeout" in error_msg:
            raise Exception("The request timed out. Please try again.")
        elif "rate limit" in error_msg:
            raise Exception("API rate limit exceeded. Please wait a moment and try again.")
        elif "authentication" in error_msg:
            raise Exception("Authentication error. Please check your API key.")
        else:
            raise Exception(f"API Error: {str(e)}")

def validate_scenario(scenario: dict, previous_scenarios: list = None) -> tuple[bool, str]:
    """
    Validate a scenario to ensure it meets requirements.
    
    Args:
        scenario (dict): The scenario to validate
        previous_scenarios (list, optional): List of previous scenarios to check uniqueness
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    # Check required keys
    required_keys = ['description', 'options', 'best_option']
    if not all(key in scenario for key in required_keys):
        return False, "Missing required fields"
    
    # Check number of options
    if len(scenario['options']) != 4:
        return False, f"Expected 4 options, got {len(scenario['options'])}"
    
    # Check best option index
    if not isinstance(scenario['best_option'], int) or scenario['best_option'] not in range(4):
        return False, f"Invalid best option index: {scenario['best_option']}"
    
    # Check uniqueness if previous scenarios provided
    if previous_scenarios:
        for prev_scenario in previous_scenarios:
            if scenario['description'] == prev_scenario['description']:
                return False, "Scenario is not unique"
    
    return True, ""

def generate_scenario(category: str, role: str = "", previous_scenarios: List[Dict] = None) -> Dict:
    """Generate a unique scenario with options"""
    if previous_scenarios is None:
        previous_scenarios = []
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Create prompt with uniqueness check
            prompt = f"""Generate a unique decision-making scenario in the {category} category.
            The scenario should be different from these previous scenarios:
            {json.dumps(previous_scenarios, indent=2)}
            
            Format the response as a JSON object with these exact fields:
            {{
                "description": "A detailed scenario description",
                "options": [
                    "Option 1 text",
                    "Option 2 text",
                    "Option 3 text",
                    "Option 4 text"
                ],
                "best_option": 0  // Index of the best option (0-3)
            }}
            
            Requirements:
            1. Must be unique and different from previous scenarios
            2. Must have exactly 4 options
            3. Must specify best_option as an integer 0-3
            4. Must be a complete JSON object
            5. Keep the response concise and focused
            """
            
            response = fetch_openai_completion(prompt)
            scenario = json.loads(response)
            
            # Validate response structure
            if not isinstance(scenario, dict):
                raise ValueError("Response is not a JSON object")
                
            required_fields = ['description', 'options', 'best_option']
            for field in required_fields:
                if field not in scenario:
                    raise ValueError(f"Missing required field: {field}")
                    
            if not isinstance(scenario['options'], list) or len(scenario['options']) != 4:
                raise ValueError("Options must be a list of exactly 4 items")
                
            if not isinstance(scenario['best_option'], int) or not 0 <= scenario['best_option'] <= 3:
                raise ValueError("best_option must be an integer between 0 and 3")
                
            # Check if scenario is unique
            for prev_scenario in previous_scenarios:
                if scenario['description'] == prev_scenario['description']:
                    raise ValueError("Generated scenario is not unique")
            
            return scenario
            
        except json.JSONDecodeError as e:
            if attempt == max_retries - 1:
                raise ValueError("Failed to generate valid scenario after multiple attempts")
            continue
        except ValueError as e:
            if attempt == max_retries - 1:
                raise Exception(f"Error generating scenario: {str(e)}")
            continue
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Error generating scenario: {str(e)}")
            continue
    
    raise Exception("Failed to generate scenario after multiple attempts")

def generate_feedback(responses: List[Dict]) -> Dict:
    """Generate brief feedback focusing on correctness and general assessment"""
    try:
        # Format responses for the prompt
        formatted_responses = []
        for i, response in enumerate(responses, 1):
            formatted_responses.append(f"""
            Scenario {i}:
            Description: {response['scenario']['description']}
            Selected Option: {response['selected_option']}
            Best Option: {response['scenario']['options'][response['scenario']['best_option']]}
            """)
        
        prompt = f"""Analyze these decision-making responses and provide brief feedback.
        For each scenario, determine if the selected option matches the best option.
        
        Responses to analyze:
        {''.join(formatted_responses)}
        
        Format the response as a JSON object with these exact fields:
        {{
            "correct_count": 0,  // Number of correct answers
            "feedback": "Brief overall feedback (2-3 sentences max)",
            "suggestion": "One key improvement suggestion"
        }}
        """
        
        response = fetch_openai_completion(prompt)
        feedback = json.loads(response)
        
        # Validate feedback structure
        if not isinstance(feedback, dict):
            raise ValueError("Feedback is not a JSON object")
            
        required_fields = ['correct_count', 'feedback', 'suggestion']
        for field in required_fields:
            if field not in feedback:
                raise ValueError(f"Missing required field: {field}")
                
        return feedback
        
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from API")
    except Exception as e:
        raise Exception(f"Error generating feedback: {str(e)}") 