import gradio as gr
from utils.md_converter import create_markdown
from utils.chatbot import ConversationalRAGModel


async def add_markdown(url: str, docs: list) -> str:
    filepath = await create_markdown(url)
    if docs:
        docs.append(filepath)
    else:
        docs = [filepath]
    return docs


def create_convert_tab(chatbot_model: ConversationalRAGModel) -> gr.Tab:
    def load(docs: list) -> str:
        """
        Load the documents into the chatbot, so it can answer questions based on those files.
        """
        if not docs:
            chatbot_model.reset()
            return 'You must convert or upload a document first'
        chatbot_model.create_chain(docs)
        return 'Document has successfully been loaded'


    with gr.Tab("Convert To Markdown") as convert_tab:
        url_input = gr.Textbox(label="Insert URL of webpage you want to convert to markdown")
        doc_button = gr.Button("Convert")
        gr.Markdown('or', elem_classes='centered')
        docs = gr.File(label="Upload a document directly from your device:", file_types=['.pdf', '.docx', '.md', '.txt'], type='filepath', file_count='multiple')

        with gr.Row():
            load_docs = gr.Button('Load files')
            status = gr.Textbox(label="Status", placeholder='', interactive=False)

        load_docs.click(load, inputs=docs, outputs=status)
        doc_button.click(add_markdown, inputs=[url_input, docs], outputs=docs)

    return convert_tab
