import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages the conversation history between the user and the AI.
    """

    def __init__(self, system_message):
        """
        Initialize the ConversationManager with a system message.

        Args:
            system_message (str): The initial system message to set the context of the conversation.
        """
        self.system_message = f"System: {system_message}"
        self.conversation_history = [self.system_message]
        logger.info("ConversationManager initialized with system message")

    def update_history(self, user_input, ai_response):
        """
        Update the conversation history with a new user input and AI response.

        Args:
            user_input (str): The user's input message.
            ai_response (str): The AI's response message.
        """
        self.conversation_history.append(f"Human: {user_input}")
        self.conversation_history.append(f"AI: {ai_response}")
        logger.info("Conversation history updated")

    def get_history(self):
        """
        Get the current conversation history.

        Returns:
            list: The list of conversation messages.
        """
        return self.conversation_history


def test_conversation_manager():
    """
    Test function for ConversationManager.
    """
    system_message = "You are a helpful assistant."
    manager = ConversationManager(system_message)

    assert manager.get_history() == ["System: You are a helpful assistant."], "Initial history is incorrect"

    manager.update_history("Hello", "Hi there! How can I assist you today?")
    history = manager.get_history()
    assert len(history) == 3, "History length is incorrect after update"
    assert history[-2] == "Human: Hello", "User input not correctly added to history"
    assert history[-1] == "AI: Hi there! How can I assist you today?", "AI response not correctly added to history"

    logger.info("ConversationManager tests passed successfully")


if __name__ == "__main__":
    test_conversation_manager()
