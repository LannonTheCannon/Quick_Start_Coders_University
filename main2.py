import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

# Initialize the database
db = SQLDatabase.from_uri("sqlite:///kids_coding_university.db")

# Initialize the language model
llm = ChatOpenAI(temperature=0, api_key=openai_api_key)

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create a custom prompt template
template = """
You are an AI assistant for a coding university for kids. Your task is to answer questions about the courses, 
teachers, and other aspects of the university. Use the provided SQL query results to inform your answers.
Here are some rules to follow:
1. Always base your answers on the SQL query results provided.
2. If you don't have enough information from the query results, say so and ask for clarification.
3. Be encouraging and positive about learning to code.
4. Make sure to keep the responses as short as possible. 
Here is the chat history, use this to understand the context of the conversation: 
{chat_history}
Given the question: '{question}' and the SQL query result: {sql_result}, provide a concise and informative answer.
"""
PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "sql_result"],
    template=template
)

# Create the SQL query chain
sql_chain = create_sql_query_chain(llm, db)

def chatbot(input_text):
    try:
        # Generate SQL query
        sql_query = sql_chain.invoke({"question": input_text})
        
        # Execute the query
        result = db.run(sql_query)
        
        # Generate a response based on the query result and chat history
        response = llm.predict(PROMPT.format(
            chat_history=memory.chat_memory.messages,
            question=input_text,
            sql_result=result
        ))
        
        # Save the interaction to memory
        memory.chat_memory.add_user_message(input_text)
        memory.chat_memory.add_ai_message(response)
        
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("Ask about our courses (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = chatbot(user_input)
        print("Chatbot:", response)
