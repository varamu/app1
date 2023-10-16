import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is a content that may be poorly worded.
    Your goal is to:
    - Properly format the content into product description
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different age groups:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the content with a warm introduction. Add the introduction if you need to.
    
    Below is the content, age group, and hobby:
    Age group: {agegroup}
    Main Hobby: {hobby}
    Content: {content}
    
    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["agegroup", "hobby", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personalized marketing text generator")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Kasutusjuhend: 1) valmista ette tootekirjeldus (sisendtekst);
2) määra tarbijasegemendid lähtuvalt vanuserühma ja hobbide kombinatsioonidest;
3) sisesta ükshaaval tarbijasegmentide lõikes eeltoodud info äpi kasutajaliideses, saada ära;
4) kopeeri ükshaaval tarbijasegmentide lõikes äpi väljundteksti kõnealuse toote tutvustuslehele.
")

with col2:
    st.image(image='companylogo.jpg', caption='Our company motto')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_agegroup = st.selectbox(
        'Which age group would you like your content to target?',
        ('9-15', '16-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100'))
    
#with col2:
#    option_hobby = st.selectbox(
#        'Customers main hobby',
#        ('American', 'British'))

def get_hobby():
    input_text = st.text_input(label="Customers main hobby", key="hobby_input")
    return input_text

hobby_input = get_hobby()

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "t shirts, all clolors, cotton, responsible manufacturing"

st.button("*See An Example*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(agegroup=option_agegroup, hobby=hobby_input, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
