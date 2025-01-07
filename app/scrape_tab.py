import pyperclip
import gradio as gr
from utils.scraper import scrape_websites


def create_scrape_tab() -> gr.Tab:
    # data variable to save scraped data
    data = []


    async def scrape(topic: str, num_results: int):
        global data
        results = await scrape_websites(topic, num_results)
        data = results
        choices = [result.split('\n')[0] for result in results]
        return gr.update(choices=choices, value=None)


    def update_outlines(index: int) -> str:
        global data
        if index is not None and isinstance(index, int) and 0 <= index < len(data):
            return data[index]
        else:
            return 'choose a source to see its outlines'


    def copy_curr_page_link(curr_page_index: int) -> str:
        global data
        if data and curr_page_index:
            page_details = data[curr_page_index]
            page_link = page_details.split('\n')[1].split(' ')[1]
            pyperclip.copy(page_link)
        return update_outlines(curr_page_index)


    with gr.Tab("Scrape Google") as scrape_tab:
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

    return scrape_tab
