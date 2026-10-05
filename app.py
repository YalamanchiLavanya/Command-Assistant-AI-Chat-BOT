'''
Command Assistant AI chatbot

fow of our chatbot is as follows:

user type questions --> prompt --> system prompt + previous chat -->
context window --> hugging face API --> LLM --> Generates completion -->
display response --> save the response in a conversation.txt file

prompt -->  what we ask our AI model?
context window --> what AI remembers during the conversation?
completion  -->What AI generate as the answer 
system prompt --> Instructions that define AI behaviour
tokens --> the pieces of text model read and generate
'''

#import the libraries
import os
import time
from datetime import datetime #to get date and time for filename
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

#--------------------------------
#step-1 : -->load hugging face token from .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("Error: HF_TOKEN is not found")
    print("create a .env file and HF_TOKEN into the file")
    print("HF_TOKEN loaded successfully")
    exit()
    
#----------------------------------------------------------------
#Step:2 ---->Create HuggingFace Inference Client -->connects Python program
#to hugging face models

client=InferenceClient(provider = 'auto',
                       token = HF_TOKEN)

#-------------------------------------------------------------------
#Step:3 --->Choose the Hosted Model
MODEL_NAME = "openai/gpt-oss-120b"

#------------------------------------------------------------------
#Step:4 ----> Create conversation Memory -->System prompt will control
#Assistance behaviour
#User and Assistant messages are added during the chat

conversation = [
    {
        'role':'system',
        'content':"You are a helpful AI Assistant.Explain the concepts in a simple and clear way for the students."}
    ]
    
#----------------------------------------------------------------------
#Step:5 --> Get AI reply with streaming response and error handling

def get_reply(messages,attempts=3):
    """send the full conversation to the HuggingFace Model....
     Features:
     ----Uses ChatCompletion
     """
    for attempt in range(attempts):
        try:
            stream = client.chat.completions.create(
                model = MODEL_NAME,
                messages=messages,
                max_tokens = 150,
                stream = True)
            
            complete_response = ""
            for chunk in stream:
                if not chunk.choices:
                    continue
                piece = chunk.choices[0].delta.content
                if piece:
                    print(piece,end="",flush=True)
                    complete_response+=piece
            print()        


        except Exception as e:
            print(f'\n Attempt {attempt+1} failed')
            print('Reason:',e)
            if attempt<attempt-1:
                print("Retrying the connection")
                time.sleep(5)
        return "Sorry AI Model is currently unavailable,try again later"

#We will save the conversation in .txt file and make our chatbot active
#--------------------------------------------------------------------
#step:6 --->Save the conversation in a .txt file

def save_conversation(conversation):
    """Saves the complete chat into a timestamped .txt file"""
    #strdtime() -->String formatting
    filename = datetime.now().strftime("conversation_%y%m%d_%H%M.text")
    with open(filename,'w',encoding='utf-8') as file:
        file.write("="*50+'\n')
        file.write("AI Chat Conversation History.\n")
        file.write("="*50+'\n')
        #now we will load the conversation
        for message in conversation:
            if message['role']=='system':
                file.write("SYSTEM:\n")
            elif message['role']=='user':
                file.write("YOU:\n")
            elif message['role']=="assistant":
                file.write("AI:\n")
            file.write(message['content'])
            file.write("\n")
        file.write("="*50+"\n")
        file.write("End of Chat Conversation")
        file.write("="*50+"\n")
    print(f'Conversation is saved as {filename}')           

#--------------------------------------------------------------------                
#step:7 -->Start our command line assistant                   
#let us define some default statements to make our BOT active

print("AI Assistant is Ready")
print("Type your message and press enter:")
print("Type 'save' to save the conversation")
print("Type 'quit' to exit")

while True:
    #now accept user input
    user_input=input("\n You:")
    if user_input.lower()=="quit":
        print("Good Bye...ika jagratha chavukooo")
        break
    #save the conversation
    if user_input.lower() == "save":
        save_conversation(conversation)
        continue
    #ignore empty input
    if not user_input:
        continue
    #Add User prompt to our conversation
    conversation.append({'role':'user',
                         'content':user_input})
    #send prompt + previous chat to generate response
    print("\n Assistant")
    reply = get_reply(conversation)
    #store the AI completio in conversation memory
    conversation.append({'role':'user',
                         'content':reply})

#In above case we use save_conversation function to store conversation
#get_reply is to get the reply from AI assistant    





















