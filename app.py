from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
from models.database import init_db, save_chat_log, fetch_chat_history, create_user, get_user, clear_chat_history, delete_user_by_id
from utils.helpers import validate_username, validate_password, verify_password, format_chat_history, format_user_response
import os 
from groq import Groq
import pandas as pd
import time
import json
import bcrypt
from typing import Any, Dict, List, Optional
import re
import psycopg2
from psycopg2 import sql
from utils.helpers import hash_password, log_error, sanitize_input
from nlp_lang.model import get_model_response


# Initialize FastAPI app
app = FastAPI()

Groq_API_key = "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"

client = Groq(api_key=Groq_API_key)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP model
nlp_model = client

# Pydantic models for request bodies
class ClearHistoryRequest(BaseModel):
    username: str
    password: str

class MessageRequest(BaseModel):
    message: str
    user_id: int

class UserRequest(BaseModel):
    username: str
    password: str

class DeleteUserRequest(BaseModel):
    username: str
    password: str

class HistoryRequest(BaseModel):
    user_id: int
    limit: int = None  # Add limit parameter

# Initialize the database
init_db('chatbot', 'postgres', 'amit2808')  # Ensure the database is initialized on startup


# Message processing
def process_message(nlp_model, message):
    doc = get_model_response(message)
    # Extract entities as an example
    return doc


# API endpoint to handle messages
@app.post("/api/message")
async def handle_message(request: MessageRequest):
    # Process the user message
    entities = process_message(nlp_model, request.message)
    response = entities

    # Save chat log to the database
    save_chat_log(request.user_id, request.message, response)

    return {"response": response}


# API endpoint to fetch chat history
@app.post("/api/history")
async def get_chat_history(request: HistoryRequest):
    history = fetch_chat_history(request.user_id, request.limit)
    if not history:
        raise HTTPException(status_code=404, detail="No chat history found.")
    
    formatted_history = format_chat_history(history)
    return {"history": formatted_history}


# API endpoint for clearing char history 
@app.delete("/api/clear_history")
async def clear_history(request: ClearHistoryRequest):
    """Clear the chat history for the logged-in user."""
    user = get_user(request.username)
    if user is None or not verify_password(request.password, user[2]):  # Check the password
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    clear_chat_history(user[0])  # user[0] is the user ID
    return {"message": "Chat history cleared."}


# API endpoint to create a new user
@app.post("/api/register")
async def register_user(request: UserRequest):
    if not validate_username(request.username):
        raise HTTPException(status_code=400, detail="Invalid username format.")
    if not validate_password(request.password):
        raise HTTPException(status_code=400, detail=validate_password(request.password)[1])

    user_id = create_user(request.username, request.password)
    if user_id is None:
        raise HTTPException(status_code=500, detail="User creation failed.")

    return {"message": "User created successfully.", "user_id": user_id}


# API endpoint for user login
@app.post("/api/login")
async def login_user(request: UserRequest):
    user = get_user(request.username)
    if user is None or not verify_password(request.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    return {"message": "Login successful.", "user": format_user_response({"id": user[0], "username": user[1]})}


# API endpoint for deleting a user
@app.delete("/api/delete_user")
async def delete_user(request: DeleteUserRequest):
    user = get_user(request.username)
    if user is None or not verify_password(request.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    delete_user_by_id(user[0])  # user[0] is the user ID
    return {"User Deleted Successfully !"}


# Main function to run the app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
