import gradio as gr
import pyperclip
from scraper import scrape_websites
from chatbot import create_chain, answer_query
from langchain_core.messages import HumanMessage, AIMessage
from pdf_converter import create_pdf
from speech import str_to_audio, audio_to_text


data = None
chains = [None]




def load(pdf_doc):
    return create_chain(chains, pdf_doc, use_local_model=True)


def answer_voice(query, chat_history=[]):
    prepared_history = []
    for a, b in chat_history:
        prepared_history.append(HumanMessage(content=a))
        prepared_history.append(AIMessage(content=b))
    try:
        query = audio_to_text(query)
    except Exception as e:
        # Replace query/answer values in case an error happens
        query = 'Unaudible voice'
        answer = str(e) if str(e) else 'Sorry, an error occured!'
        audio = str_to_audio(answer)
        return chat_history + [(query, answer)], audio
    answer = answer_query(chain=chains[0], query=query, chat_history=prepared_history)
    audio = str_to_audio(answer)
    return chat_history + [(query, answer)], audio


def answer(query, chat_history=[]):
    prepared_history = []
    for a, b in chat_history:
        prepared_history.append(HumanMessage(content=a))
        prepared_history.append(AIMessage(content=b))
    answer = answer_query(chain=chains[0], query=query, chat_history=prepared_history)
    return '', chat_history + [(query, answer)]


async def scrape(topic, num_results):
    global data
    results = await scrape_websites(topic, num_results)
    data = results
    choices = [result.split('\n')[0] for result in results]
    return gr.update(choices=choices, value=None)


def update_outlines(index):
    if index:
        return data[index]
    else:
        return 'choose a source to see its outlines'


def copy_curr_page_link(curr_page_index):
    if data and curr_page_index:
        page_details = data[curr_page_index]
        page_link = page_details.split('\n')[1].split(' ')[1]
        pyperclip.copy(page_link)
    return update_outlines(curr_page_index)


html = """
<div style="text-align:center; max-width: 900px; margin: 0 auto; margin-top:5px">
    <h1>Research Assistant</h1>
    <p> Welcome to the Research Assistant app! This tool helps you find relevant information on your topic of interest.</p>
</div>"""
css = """container{max-width:900px; margin-left:auto; margin-right:auto;padding:20px}
.centered{text-align:center;}"""
theme = gr.themes.Monochrome(
    primary_hue=gr.themes.colors.orange,
    secondary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.gray,
    radius_size=gr.themes.sizes.radius_md
)

with gr.Blocks(css=css, theme=theme) as demo:
    gr.HTML(html)
    with gr.Tab("Scrape Google"):
        with gr.Row():
            with gr.Column(variant="panel"):
                topic = gr.Textbox(label="What is your Research Topic?", container=True)
                num_links = gr.Slider(label="Specify the Number of Links to Scrape!", minimum=0, maximum=15, step=1,
                                      container=True)
                text_button = gr.Button("Scrape")

            with gr.Column(min_width=600):
                websites_dropdown = gr.Dropdown(interactive=True, type='index', label='Sources')
                text_output = gr.Textbox(label="Outlines", lines=10, container=True, autoscroll=True, interactive=False)
                copy_button = gr.Button(value='copy this page link')

            text_button.click(scrape, inputs=[topic, num_links], outputs=websites_dropdown, scroll_to_output=False)
            websites_dropdown.change(fn=update_outlines, inputs=websites_dropdown, outputs=text_output)
            copy_button.click(copy_curr_page_link, inputs=websites_dropdown, outputs=text_output)

    with gr.Tab("Convert To PDF"):
        with gr.Column():
            url_input = gr.Textbox(label="Insert URL of webpage you want to convert to pdf")
            pdf_button = gr.Button("Convert")
            gr.Markdown('or', elem_classes='centered')
            pdf_doc = gr.File(label="Upload a pdf directly from your device:", file_types=['.pdf', '.docx'],type='filepath')

            with gr.Row():
                load_pdf = gr.Button('Load pdf file')
                status = gr.Textbox(label="Status", placeholder='', interactive=False)

            load_pdf.click(load, inputs=pdf_doc, outputs=status)
            pdf_button.click(create_pdf, inputs=url_input, outputs=pdf_doc)

    with gr.Tab('Chat with your PDF'):
        with gr.Column():
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(label="type in your question")
            with gr.Row():
                submit_query = gr.Button("submit")
                clear = gr.ClearButton([user_input, chatbot])

            
            submit_query.click(answer, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
            
            #Optional
            user_input.submit(answer, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

    with gr.Tab('Talk with your PDF'):
        with gr.Column():
            chatbot = gr.Chatbot(visible=False)
            audio = gr.Audio(type='numpy')
            user_input = gr.Audio(sources='microphone', type='numpy')
            submit_query = gr.Button("submit")

            submit_query.click(answer_voice, inputs=[user_input, chatbot], outputs=[chatbot, audio])

            

if __name__ == "__main__":
    demo.launch(share=False)
