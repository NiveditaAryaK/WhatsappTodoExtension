from fastapi import FastAPI, Request
import os 
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
TWILIO_ACCOUNT_SID=os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER=os.getenv('TWILIO_WHATSAPP_NUMBER')
PERSONAL_NUMBER=os.getenv('PERSONAL_NUMBER')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
todos = []
app=FastAPI()
@app.post("/webhook")
async def todo(request:Request):
    data=await request.form()
    sender=data.get("From")
    message_body=data.get("Body")
    response = "I don't understand that command. Try:\n- add [task]\n- list\n- delete [number]"
    if message_body.lower().startswith("add "):
        task= message_body[4:]
        todos.append(task)
        response=f'Task "{task}" added to your todo list.'
        for i,task in enumerate(todos,1):
            response+=f'\n{i}. {task}'
    elif message_body.lower()=="list":
        if todos:
            response = "Your tasks:\n"
            for i, task in enumerate(todos, 1):
                response += f"{i}. {task}\n"
        else:
            response = "No tasks yet!"
    elif message_body.lower().startswith("delete "):
        try:
            index = int(message_body[7:].strip()) - 1 
            if 0 <= index < len(todos):
                deleted_task = todos.pop(index)
                response = f"Deleted: {deleted_task}\n\nCurrent tasks:\n"
                for i, task in enumerate(todos, 1):
                    response += f"{i}. {task}\n"
            else:
                response = "Invalid task number!"
        except ValueError:
            response = "Please specify a valid number to delete"

    message = client.messages.create(
    from_=TWILIO_WHATSAPP_NUMBER,
    body=response,
    to=sender
    )
    print(message.sid)
    print(data)
    return {"message":"ok"}

