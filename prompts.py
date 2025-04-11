import openai
from config import OPENAI_API_KEY

# Configure OpenAI client
openai.api_key = OPENAI_API_KEY

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
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error fetching OpenAI completion: {str(e)}") 