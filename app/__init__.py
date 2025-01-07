import gradio as gr
from .scrape_tab import create_scrape_tab
from .convert_tab import create_convert_tab
from .chat_tab import create_chat_tab
from .talk_tab import create_talk_tab
from utils.chatbot import ConversationalRAGModel


def create_app(chatbot_model: ConversationalRAGModel) -> gr.Blocks:
    html = """
        <div style="text-align:center; max-width: 900px; margin: 0 auto; margin-top:5px">
            <h1>Research Assistant</h1>
            <p> Welcome to the Research Assistant app! This tool helps you find relevant information on your topic of interest.</p>
        </div>
    """
    css = """
        container{max-width:900px; margin-left:auto; margin-right:auto;padding:20px}
        .centered{text-align:center;}
    """
    theme = gr.themes.Monochrome(
        primary_hue=gr.themes.colors.orange,
        secondary_hue=gr.themes.colors.blue,
        neutral_hue=gr.themes.colors.gray,
        radius_size=gr.themes.sizes.radius_md
    )


    with gr.Blocks(css=css, theme=theme) as app:
        gr.HTML(html)
        create_scrape_tab()
        create_convert_tab(chatbot_model)
        create_chat_tab(chatbot_model)
        create_talk_tab(chatbot_model)

    return app
