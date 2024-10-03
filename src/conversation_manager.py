import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dateutil.tz import UTC

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection parameters
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
CONVERSATION_TABLE = os.getenv('CONVERSATION_TABLE')

# Create the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()


# Define the ConversationHistory model dynamically
def create_conversation_model(table_name):
    if table_name not in Base.metadata.tables:
        return Table(table_name, Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('message', String, nullable=False),
                     Column('timestamp', DateTime, default=lambda: datetime.now(UTC))
                     )
    else:
        return Base.metadata.tables[table_name]


# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_table_if_not_exists(table_name):
    """Create the conversation table if it doesn't exist."""
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        create_conversation_model(table_name).create(engine)
        logger.info(f"Created conversation table: {table_name}")


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
        self.table_name = CONVERSATION_TABLE
        create_table_if_not_exists(self.table_name)
        self.session = SessionLocal()
        self.ConversationHistory = create_conversation_model(self.table_name)
        self._initialize_conversation()
        logger.info(f"ConversationManager initialized with system message and database connection. Table: {self.table_name}")

    def _initialize_conversation(self):
        """Initialize the conversation with the system message."""
        if self.session.query(self.ConversationHistory).count() == 0:
            self.add_message(self.system_message)

    def add_message(self, message):
        """Add a single message to the conversation history."""
        new_message = self.ConversationHistory.insert().values(message=message)
        self.session.execute(new_message)
        self.session.commit()
        logger.info("Message added to conversation history")

    def update_history(self, user_input, ai_response):
        """
        Update the conversation history with a new user input and AI response.

        Args:
            user_input (str): The user's input message.
            ai_response (str): The AI's response message.
        """
        self.add_message(f"Human: {user_input}")
        self.add_message(f"AI: {ai_response}")
        logger.info("Conversation history updated")

    def get_history(self):
        """
        Get the current conversation history.

        Returns:
            list: The list of conversation messages.
        """
        return [msg.message for msg in self.session.query(self.ConversationHistory).order_by(self.ConversationHistory.c.timestamp).all()]

    def close(self):
        """Close the database session."""
        if hasattr(self, 'session'):
            self.session.close()
            logger.info("ConversationManager session closed")
