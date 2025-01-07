import streamlit as st
from streamlit_chat import message

from phi.agent import Agent, RunResponse
from phi.model.deepseek import DeepSeekChat
from phi.model.groq import Groq
#from phi.model.ollama import Ollama
from phi.model.anthropic import Claude
from phi.tools.pubmed import PubmedTools
from phi.utils.pprint import pprint_run_response

#from dotenv import load_dotenv
#load_dotenv()

#message("My message") 
#message("Hello bot!", is_user=True)  # align's the message to the right

st.title("AI Search for PubMed")

llm = st.radio(
    "Select a Large Language Model",
    ["Llama", "Claude", "DeepSeek"],
)

chat_placeholder = st.empty()

st.session_state.setdefault(
    'generated', 
    [{'type': 'normal', 'data': 'Connecting to LLMs'},]
)

st.session_state.setdefault(
    'past', 
    ['Please connect to LLMs',]
)

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

def on_input_change():
    with st.spinner('Searching PubMed ...'):
        user_input = st.session_state.user_input
        st.session_state.past.append(user_input)
        response: RunResponse = agent.run(user_input, stream=False, markdown=False)
        output = response.content
        #st.write(output)

        gen = {'type': 'normal', 'data': output}
        st.session_state.generated.append(gen)

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

if llm == 'Llama':
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        #model=Claude(id="claude-3-5-sonnet-20240620"),
        #model=Claude(id="claude-3-5-haiku-latest"),
        tools=[PubmedTools()], 
        instructions=["Always include sources including links to the original article if possible."],
        show_tool_calls=True,
        markdown=True,
        debug=True,
    )
elif llm == 'Claude':
    agent = Agent(
        #model=Ollama(id="llama3.2"),
        model=Claude(id="claude-3-5-sonnet-20240620"),
        #model=Claude(id="claude-3-5-haiku-latest"),
        tools=[PubmedTools()], 
        show_tool_calls=True,
        markdown=True,
        debug=True,
    )
else:
    agent = Agent(
        #model=Ollama(id="llama3.2"),
        model=DeepSeekChat(),
        #model=Claude(id="claude-3-5-haiku-latest"),
        tools=[PubmedTools()], 
        show_tool_calls=True,
        markdown=True,
        debug=True,
    )

#Tell me about innovative methods to teach carb counting
#for i  in range(len(st.session_state['generated'])):
#    st.write('first', i )
         
with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):   
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            #is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear message", on_click=on_btn_click)



#with st.spinner('Searching PubMed ...'):



with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")