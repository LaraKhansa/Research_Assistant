import os
from dotenv import load_dotenv
from app import create_app
from utils.chatbot import ConversationalRAGModel


load_dotenv()


chatbot_model = ConversationalRAGModel(use_local_model=True)
app = create_app(chatbot_model)
app.launch(server_name=os.getenv('HOST'), server_port=int(os.getenv('PORT')))
