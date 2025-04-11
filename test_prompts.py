import unittest
from unittest.mock import patch, MagicMock
from prompts import fetch_openai_completion

class TestOpenAIIntegration(unittest.TestCase):
    @patch('openai.ChatCompletion.create')
    def test_successful_completion(self, mock_create):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response

        result = fetch_openai_completion("Test prompt")
        self.assertEqual(result, "Test response")
        
        # Verify API call was made with correct parameters
        mock_create.assert_called_once()
        call_args = mock_create.call_args[1]
        self.assertEqual(call_args['temperature'], 0.3)
        self.assertEqual(call_args['model'], "gpt-3.5-turbo")

    @patch('openai.ChatCompletion.create')
    def test_api_error(self, mock_create):
        # Mock API error
        mock_create.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            fetch_openai_completion("Test prompt")
        self.assertTrue("Error fetching OpenAI completion" in str(context.exception))

if __name__ == '__main__':
    unittest.main() 