import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document
from langchain.retrievers import BaseRetriever
from typing import List

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

# Initialize the database
db = SQLDatabase.from_uri("sqlite:///kids_coding_university.db")

# Initialize the language model
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

# Create a custom prompt template
_DEFAULT_TEMPLATE = """Given an input question, create a syntactically correct sqlite query to run.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"

Only use the following tables:

Courses: CourseID, ProgramName, AgeRange, Duration, LanguagesTaught, Cost, Prerequisites, LearningOutcomes, ClassFormat, ClassSize, CertificationOffered, WeeklyTimeCommitment, AdditionalCosts, ProgressTracking, HomeworkProjects, StudentSupport, AdvancedOpportunities, OnlineSafetyMeasures, RefundPolicy, ParentInvolvement, CareerPreparation

CourseTopics: TopicID, CourseID, TopicName, TopicDescription

FAQ: FAQID, Question, Answer

Question: {question}"""

PROMPT = PromptTemplate(
    input_variables=["question"],
    template=_DEFAULT_TEMPLATE
)

# Create the SQL query chain
sql_chain = create_sql_query_chain(llm, db)

# Custom retriever
class SQLDatabaseRetriever(BaseRetriever):
    def __init__(self, db, sql_chain):
        self.db = db
        self.sql_chain = sql_chain

    def get_relevant_documents(self, query: str) -> List[Document]:
        sql_query = self.sql_chain.invoke({"question": query})
        result = self.db.run(sql_query)
        return [Document(page_content=str(result))]

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)

# Initialize the custom retriever
retriever = SQLDatabaseRetriever(db, sql_chain)

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the conversational chain
conversation = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

def chatbot(input_text):
    response = conversation({"question": input_text})
    return response['answer']

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("Ask about our courses (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = chatbot(user_input)
        print("Chatbot:", response)
