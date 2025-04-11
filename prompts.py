from openai import OpenAI
from config import OPENAI_API_KEY

# Configure OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_openai_completion(prompt: str) -> str:
    """
    Fetch completion from OpenAI API with temperature set to 0.3
    
    Args:
        prompt (str): The input prompt to send to OpenAI
        
    Returns:
        str: The completion text from OpenAI
        
    Raises:
        Exception: If there's an error with the API request
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error fetching OpenAI completion: {str(e)}")

def generate_scenario(category: str, role: str = "") -> dict:
    """
    Generate a decision-making scenario for the given category and role.
    
    Args:
        category (str): The category of the scenario
        role (str, optional): The user's role for context
        
    Returns:
        dict: A dictionary containing the scenario description and options
    """
    role_context = f" for a {role}" if role else ""
    prompt = f"""
    Generate a realistic decision-making scenario{role_context} in the {category} category.
    The scenario should be 3-5 sentences long and present a clear decision point.
    Include 3-4 multiple choice options, with one being clearly the best choice.
    Format the response as a JSON object with 'description' and 'options' keys.
    """
    
    response = fetch_openai_completion(prompt)
    try:
        # Parse the response as JSON
        import json
        scenario = json.loads(response)
        return scenario
    except json.JSONDecodeError:
        # Fallback to a simple format if JSON parsing fails
        lines = response.strip().split('\n')
        description = lines[0]
        options = [line.strip('- ').strip() for line in lines[1:] if line.strip()]
        return {
            'description': description,
            'options': options
        }

def generate_feedback(responses: list) -> dict:
    """
    Generate feedback for a set of user responses.
    
    Args:
        responses (list): List of user responses containing scenario, selected option, and explanation
        
    Returns:
        dict: A dictionary containing overall feedback, improvement suggestion, and detailed feedback
    """
    prompt = f"""
    Review these decision-making responses and provide feedback:
    {responses}
    
    Provide:
    1. Overall feedback on decision-making skills
    2. One key improvement suggestion
    3. Detailed feedback for each scenario
    
    Format as a JSON object with 'overall', 'suggestion', and 'detailed' keys.
    """
    
    response = fetch_openai_completion(prompt)
    try:
        # Parse the response as JSON
        import json
        feedback = json.loads(response)
        return feedback
    except json.JSONDecodeError:
        # Fallback to a simple format if JSON parsing fails
        lines = response.strip().split('\n')
        return {
            'overall': lines[0],
            'suggestion': lines[1],
            'detailed': lines[2:]
        } 