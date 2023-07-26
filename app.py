import box
import timeit
import yaml
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from src.utils import setup_dbqa
from src.prompts import qa_template, qa_template_cyber_compliance, qa_template_military_intel
from src.llm import build_llm

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def main():
    # Streamlit app title
    st.title('Chatbot for Documents')

    # Prompt template for QA retrieval
    prompt_templates = {
        'Default Prompt': qa_template,
        'Cyber-Compliance Prompt': qa_template_cyber_compliance,
        'Military Intel Prompt': qa_template_military_intel
    }
    selected_prompt = st.selectbox('Select a Prompt', list(prompt_templates.keys()), index=0)
    st.text(prompt_templates[selected_prompt])

    # Input widget for user query
    user_query = st.text_input('Enter your query:', 'Enter your question here')

    # Setup LLM and DBQA
    if st.button('Get Answer'):
        start = timeit.default_timer()
        llm = build_llm()
        dbqa = setup_dbqa(selected_prompt)  # Pass the selected prompt name
        response = dbqa({'query': user_query})  # Use the key 'query' instead of 'input'
        end = timeit.default_timer()

        # Display the response and source documents
        st.text(f'Answer: {response["result"]}')
        st.text('='*50)

        # Process source documents
        source_docs = response['source_documents']
        for i, doc in enumerate(source_docs):
            st.text(f'\nSource Document {i+1}\n')
            st.text(f'Source Text: {doc.page_content}')
            st.text(f'Document Name: {doc.metadata["source"]}')
            st.text(f'Page Number: {doc.metadata["page"]}')
            st.text('='*60)

        st.text(f'Time to retrieve response: {end - start}')


if __name__ == '__main__':
    main()
