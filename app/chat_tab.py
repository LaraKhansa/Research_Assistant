import gradio as gr
from utils.chatbot import ConversationalRAGModel


def create_chat_tab(chatbot_model: ConversationalRAGModel) -> gr.Tab:
    def answer(query: str, chat_history=None):
        """
        Returns the given chat history after adding the model answer on the given query
        """
        if not chat_history:
            chat_history = []
        answer = chatbot_model.answer(query=query)
        return '', chat_history + [(query, answer)]


    with gr.Tab('Chat with your Docs') as chat_tab:
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(label="type in your question")
        with gr.Row():
            submit_query = gr.Button("submit")
            clear = gr.ClearButton([user_input, chatbot])

        submit_query.click(answer, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
        user_input.submit(answer, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

    return chat_tab
