'''
===========================================
        Module: Util functions
===========================================
'''
import box
import yaml

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from src.prompts import qa_template, qa_template_cyber_compliance, qa_template_military_intel  # Import the additional prompts
from src.llm import build_llm  # Import build_llm

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt


def build_retrieval_qa(llm, prompt, vectordb):
    dbqa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT}),
                                       return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return dbqa


def setup_dbqa(selected_prompt):  # Accept the selected_prompt as an argument
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    llm = build_llm()

    # Update qa_prompt based on the selected_prompt
    if selected_prompt == 'Default Prompt':
        qa_prompt = set_qa_prompt()
    elif selected_prompt == 'Cyber-Compliance Prompt':
        qa_prompt = PromptTemplate(template=qa_template_cyber_compliance, input_variables=['context', 'question'])
    elif selected_prompt == 'Military Intel Prompt':
        qa_prompt = PromptTemplate(template=qa_template_military_intel, input_variables=['context', 'question'])
    else:
        raise ValueError(f"Invalid prompt: {selected_prompt}")

    dbqa = build_retrieval_qa(llm, qa_prompt, vectordb)

    return dbqa
