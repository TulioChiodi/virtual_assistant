class ConversationManager:
    def __init__(self, system_message):
        self.system_message = f"System: {system_message}"
        self.conversation_history = [self.system_message]

    def update_history(self, user_input, ai_response):
        self.conversation_history.append(f"Human: {user_input}")
        self.conversation_history.append(f"AI: {ai_response}")

    def get_history(self):
        return self.conversation_history
