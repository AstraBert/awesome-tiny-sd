import gradio as gr
import time
from imgen import *

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_message(history, message):
    if len(message["files"]) > 0:
        history.append((message["files"], None))
    if message["text"] is not None and message["text"] != "":
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)



def bot(history):
    if type(history[-1][0]) != tuple:
        try:
            prompt = history[-1][0]
            image = pipeline(prompt).images[0]
            image.save("generated_image.png")
            response = ("generated_image.png",)
            history[-1][1] = response
            yield history
        except Exception as e:
            response = f"Sorry, the error '{e}' occured while generating the response; check [troubleshooting documentation](https://astrabert.github.io/awesome-tiny-sd/#troubleshooting) for more"
            history[-1][1] = ""
            for character in response:
                history[-1][1] += character
                time.sleep(0.05)
                yield history
    if type(history[-1][0]) == tuple:
        response = f"Sorry, this version still does not support uploaded files :("
        history[-1][1] = ""
        for character in response:
            history[-1][1] += character
            time.sleep(0.05)
            yield history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [[None, ("Hi, I am awesome-tiny-sd, a little stable diffusion model that lets you generate images:blush:\nJust write me a prompt, I'll generate what you ask for:heart:",)]],
        label="awesome-tiny-sd",
        elem_id="chatbot",
        bubble_full_width=False,
    )

    chat_input = gr.MultimodalTextbox(interactive=True, file_types=["pdf"], placeholder="Enter your image-generating prompt...", show_label=False)

    chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
    bot_msg = chat_msg.then(bot, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

    chatbot.like(print_like_dislike, None, None)
    clear = gr.ClearButton(chatbot)

demo.queue()
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=False)

	