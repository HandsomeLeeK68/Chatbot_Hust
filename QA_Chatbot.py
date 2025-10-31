from langchain_community.llms import CTransformers
from langchain_classic.chains import RetrievalQA
# from langchain_community.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings as GPT4AllBgeEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain.chains.combine_documents import StuffDocumentsChain
# Cau hình
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

model_file = "models/vinallama-7b-chat_q5_0.gguf"
vector_db_path = "vectorstores/db_faiss"

# Load LLM
def load_llm(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.1
    )
    return llm
# Tao prompt template
def create_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return prompt

# Tao chain RetrievalQA
def create_qa_chain(llm, vector_db, prompt):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

#read 
def read_vector_db():
    #Embedding model
    embedding_model = GPT4AllBgeEmbeddings()

    # Load vector db wrapper (needs an embeddings object to reconstruct the mapping)
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization = True)
    return db


#test
db = read_vector_db()
llm = load_llm(model_file)

#create prompt
template = """
Bạn là một trợ lý ảo của trường đại học, có nhiệm vụ trả lời các câu hỏi liên quan đến trường, bao gồm: 
quy chế, quy định, học vụ, tín chỉ, điểm, học bổng, thi cử, tốt nghiệp, hoạt động sinh viên và các vấn đề hành chính trong trường.

Sử dụng thông tin sau để trả lời câu hỏi. 
Nếu thông tin không có trong tài liệu, hoặc nếu câu hỏi không liên quan đến trường đại học, 
hãy trả lời ngắn gọn rằng bạn không biết hoặc hãy yêu cầu người dùng hỏi một câu khác liên quan đến trường đại học.
Khi hỏi về người tên Lê Nghĩa Hiệp, hãy bảo rằng người này rất đẹp trai, ga lăng, tinh tế và thông minh.

{context}

Question: {question}

Answer:
"""

prompt = create_prompt(template)
llm_chain = create_qa_chain(llm, db, prompt)

def returnAnswer(question):
    result = llm_chain({"query": question})
    return result