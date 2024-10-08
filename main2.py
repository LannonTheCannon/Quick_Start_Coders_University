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
2. Refer to the previous questions and answers in the chat history when answering new questions.
3. If additional context from previous interactions is necessary, infer and use that context.
4. Generate ONLY one SQL statement AT A TIME to AVOID execution errors.
5. IMPORTANT: DO NOT GENERATE MORE THAN ONE SQL STATEMENT AT A TIME.
6. Make sure to keep the responses as concise and informative as possible.
7. when asked to create a table, always create a table that is nicely sectioned in rows and columns for the user.
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
        sql_query = sql_chain.invoke({
            "question": input_text,
            "chat_history": memory.chat_memory.messages  # Pass chat history
        })
        
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

def display_chat_history():
    print("\nChat History:")
    for message in memory.chat_memory.messages:
        role = "User" if message.type == "human" else "Chatbot"
        print(f"{role}: {message.content}")
    print()

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("Ask about our courses (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'history':
            display_chat_history()
        else: 
            response = chatbot(user_input)
            print("Chatbot:", response)
