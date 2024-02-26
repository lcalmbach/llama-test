import streamlit as st
import replicate
import os

# modified from https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")
MODEL_OPTIONS = ['Llama2-7B', 'Llama2-13B', 'Llama-70b', 'Mixtral-8x7b']
# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama/Mistral Chatbots')
    
    replicate_api = st.secrets['REPLICATE_API_TOKEN']
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', MODEL_OPTIONS, key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    elif selected_model == 'Llama2-70B':
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    else:
        llm = "mistralai/mixtral-8x7b-instruct-v0.1"
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=100, max_value=4000, value=2000, step=100)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input, placeholder):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
            
    input = {"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
             "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1}
    if 'llama' in selected_model.lower():
        output = replicate.run(llm,
                            input=input)
    else:
        iterator = replicate.run(
            llm,
            input=input,
        )
        output = ''
        for item in iterator:
            output += item
            placeholder.markdown(output)
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            placeholder = st.empty()
            response = generate_llama2_response(prompt, placeholder)
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)