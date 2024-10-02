import logging
from typing import List
import ollama

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_response(conversation_history: List[str], user_input: str) -> str:
    """
    Generate an AI response based on the conversation history and user input.

    Args:
        conversation_history (List[str]): The list of previous conversation messages.
        user_input (str): The latest user input to respond to.

    Returns:
        str: The generated AI response.

    Raises:
        Exception: For any errors during response generation.
    """
    try:
        logger.info("Generating AI response")
        full_prompt = "\n".join(conversation_history + [f"Human: {user_input}"])
        response = ollama.generate(model="llama3.2", prompt=full_prompt)
        logger.info("AI response generated successfully")
        return response['response']
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        raise


def test_generate_response():
    """
    Test function for generate_response.
    """
    try:
        history = ["System: You are a helpful assistant.", "Human: Hello", "AI: Hi there!"]
        user_input = "How are you?"
        response = generate_response(history, user_input)
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"
        logger.info("generate_response test passed successfully")
    except Exception as e:
        logger.error(f"generate_response test failed: {str(e)}")


if __name__ == "__main__":
    test_generate_response()
