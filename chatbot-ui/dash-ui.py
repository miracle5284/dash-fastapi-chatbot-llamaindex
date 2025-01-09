from styles import *
from config import *
from utils import extract_from_dict
from requests import post
from dash import Dash, html, dcc, callback, State, Output, Input

# Initialize the Dash application
app = Dash(__name__)

# Backend server configuration
CHATBOT_URL = f"{CHATBOT_SERVER['url']}:{CHATBOT_SERVER['port']}"
UI_URL, UI_PORT, DEBUG = extract_from_dict(UI_SERVER, 'url', 'port', 'debug')

# Define the application layout
app.layout = html.Div([
    html.Div(id="output-conversation", style=output_conversation_style),
    html.Div([
        dcc.Textarea(
            id="input-text",
            placeholder="Type here...",
            style=input_text_style
        ),
        html.Button("Submit", id="input-submit")
    ], style=layout_div_nth_2_style),
    dcc.Store(id="store-chat", data="")
])

# Callback to handle chatbot queries
@app.callback(
    [Output('store-chat', 'data'), Output('input-text', 'value')],
    [Input('input-submit', 'n_clicks')],
    [State('input-text', 'value'), State('store-chat', 'data')]
)
def query_chatbot(n_clicks, input_value, chat):
    if not n_clicks:
        return chat, ''
    if not input_value:
        return chat, ''

    # Update the chat history
    chat += f'You: {input_value}<split>Bot: '
    query = chat.replace('<split>', '\n').replace('Bot:', '').replace('You:', '')

    try:
        # Send the user query to the backend chatbot
        chatbot_response = post(CHATBOT_URL, json={'question': query})
        chatbot_response.raise_for_status()
        response = chatbot_response.json().get('response', 'Error: Invalid response format')
    except Exception as e:
        response = f"Error: {str(e)}"

    chat += f'{response}<split>'
    return chat, ""

# Callback to update the conversation display
@app.callback(
    Output('output-conversation', 'children'),
    Input('store-chat', 'data')
)
def update_conversation(conversation):
    if not conversation:
        return []
    messages = conversation.split('<split>')
    return [html.Div(message, style=conversation_message_style) for message in messages if message.strip()]


# Main entry point
if __name__ == "__main__":
    app.run(port=UI_PORT, debug=DEBUG)
