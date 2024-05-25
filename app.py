import gradio as gr
import random
from scraperr import scrape_google
from pdf_converter import create_pdf



async def scrape_websites(topic, num_links, num_results_per_link=10):
    output_text = await scrape_google(topic, num_results_per_link)
    # Ensure output_text is a list
    if not isinstance(output_text, list):
        output_text = [output_text]
    # Select random links based on the user's input
    selected_links = random.sample(output_text, min(num_links, len(output_text)))
    # Convert the list of strings to a single string
    output_string = "\n".join(selected_links)
    return output_string

def convert_to_pdf(url):
    pdf_path = create_pdf(url)
    return pdf_path

html = """
<div style="text-align:center; max-width: 900px; margin: 0 auto; margin-top:5px">
    <h1>Research Assistant</h1>
    <p> Welcome to the Research Assistant app! This tool helps you find relevant information on your topic of interest.</p>
</div>"""
css = """container{max-width:900px; margin-left:auto; margin-right:auto;padding:20px}"""

with gr.Blocks(css=css,theme=gr.themes.Monochrome( primary_hue= gr.themes.colors.orange , secondary_hue=gr.themes.colors.blue,neutral_hue=gr.themes.colors.gray,radius_size=gr.themes.sizes.radius_md)) as demo:
    gr.HTML(html)
    with gr.Tab("Scrape Google"):
      with gr.Row():  
            with gr.Column(variant="panel"):
                
                topic = gr.Textbox(label="What is your Research Topic?", container= True)
                num_links = gr.Slider(label="Specify the Number of Links to Scrape!",minimum= 0, container= True)
                text_button = gr.Button("Scrape")
                
            with gr.Column(min_width=600):
                text_output = gr.Textbox(label="Result", lines= 10, container=True, autoscroll=False)
        
            text_button.click(scrape_websites, inputs=[topic, num_links], outputs=text_output, scroll_to_output=False)        
            
            
    
    with gr.Tab("Convert To PDF"):
        url_input = gr.Textbox(label="URL")
        pdf_button = gr.Button("Convert")
        pdf_output = gr.File(label="PDF")
        pdf_button.click(convert_to_pdf, inputs=url_input, outputs=pdf_output)
        chat_bot_button = gr.Button("Proceed to ChatBot", link="https://2f6174dacb556ecc75.gradio.live")
        
        
        

if __name__ == "__main__":
    demo.launch(share = True)


