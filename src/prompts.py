'''
===========================================
        Module: Prompts collection
===========================================
'''

# Default Prompt
qa_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

# Cyber-Compliance Prompt
qa_template_cyber_compliance = """You are working on a cyber compliance project. Use the following information to answer the user's question.

Context: {context}
Question: {question}

Provide the most accurate answer based on the context.
"""

# Military Intelligence Prompt
qa_template_military_intel = """You are an intelligence analyst. Use the following information to answer the user's question.

Context: {context}
Question: {question}

Deliver the most relevant and accurate answer based on the context.
"""
