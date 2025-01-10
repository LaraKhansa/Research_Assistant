import gradio as gr
from utils.chatbot import ConversationalRAGModel
from utils.speech import str_to_audio, audio_to_text


def create_talk_tab(chatbot_model: ConversationalRAGModel) -> gr.Tab:
    def answer_voice(query, chat_history=None):
        if chat_history is None:
            chat_history = []
        try:
            query = audio_to_text(query)
        except Exception as e:
            # Replace query/answer values in case an error happens
            query = 'Unaudible voice'
            answer = str(e) if str(e) else 'Sorry, an error occured!'
            audio = str_to_audio(answer)
            return chat_history + [(query, answer)], audio
        answer = chatbot_model.answer(query=query)
        audio = str_to_audio(answer)
        return chat_history + [(query, answer)], audio


    with gr.Tab('Talk with your Docs') as talk_tab:
        chatbot = gr.Chatbot(visible=False)
        audio = gr.Audio(type='numpy')
        user_input = gr.Audio(sources='microphone', type='numpy')
        submit_query = gr.Button("submit")
        submit_query.click(answer_voice, inputs=[user_input, chatbot], outputs=[chatbot, audio])

    return talk_tab
