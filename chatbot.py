# Import necessary libraries
import openai
import os
import json
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from PIL import Image
import yfinance as yf

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = 'YOUR-KEY-HERE'
openai.api_key = "YOUR-KEY-HERE" 

# Example dummy function hard coded to return your account balance
def get_saldo(cuenta):
    saldo_info = {
        "saldo": "$1,100 USD"
    }
    return json.dumps(saldo_info)

# Function to get stock information using Yahoo Finance
def get_stock(cuenta):
    stk = yf.Ticker(cuenta)
    hist = stk.history(period="1dy")
    ticker_info = {
        "ticker": str(hist)
    }
    return json.dumps(ticker_info)

# Function to interact with the chatbot using GPT-3-turbo-0613
# Using this model because it supports function calling with intent
def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

# Function to run a conversation with the chatbot
def run_conversation():
    # Step 1: send the conversation and available functions to GPT   
    functions = [
        {
            "name": "get_saldo",
            "description": "Consults and obtains balance of an bank account",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuenta": {
                        "type": "string",
                        "description": "The bank account balance",
                    }
                }
            },
        },
        {
            "name": "get_stock",
            "description": "Obtain stock symbol information",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuenta": {
                        "type": "string",
                        "description": "The stock symbol",
                    }
                }
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_saldo": get_saldo,
            "get_stock": get_stock,
        }  # only two functions in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            cuenta=function_args.get("cuenta")
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response

        return second_response['choices'][0]['message']['content']
    
    else:   
        return chatbot(user_input)

# Function to construct an index from a directory
def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(
        temperature=0.7, 
        model_name="gpt-3.5-turbo-0613",
        max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

# Initializing
# Creating the chatbot interfaces using Streamlit
with st.sidebar:
        st.title("AI Chatbot")
        image = Image.open('logo.png')
        st.image(image, caption='mexmarv FAQ chatbot w/Function Intent - gpt-3.5-turbo-0613')
        st.write("This chatbot answers from training documents or FAQs, and calls two functions (APIs) if it finds context automatically.")
        st.code("1. Intention to call balance API.\n2. Intention to call stock information from Yahoo Finance.")
        st.caption("by Marvin Nahmias.")

        st.spinner('Initializing...')
        path = './index.json'
        check_file = os.path.isfile(path)
        # Detect index.json vectors if not construct
        if check_file:
            st.spinner("Training done previously.")
            st.success('Done.')
        else:
            st.spinner("Training with files located in /docs...")
            construct_index("docs") 
        st.success('Done.')

# Storing the user's input
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Function to get user's input from a text input field
def get_text():
    input_text = st.text_input("",placeholder="Ask me something from docs.")    
    return input_text

# Get user's input
user_input = get_text()

if user_input:
    messages = [{"role": "user", "content": user_input}]
    output = run_conversation()

    # Store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) -1, -1, -1):
        st.chat_message("assistant").write(st.session_state["generated"][i], key=str(i))
        st.chat_message("user").write(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
