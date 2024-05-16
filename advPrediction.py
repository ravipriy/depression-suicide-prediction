# Import packages
import os
import torch
import random
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from IPython.display import Markdown, display
from datasets import Dataset

start_message = "==== Hello! I am Alex and I am your virtual friend. If you need a listening ear, I'm always here. To end the chat, input 'exit' in the chatbox. ===="

prevention_messages = ["Are you okay? How long have you been feeling this way?",
                       "That sounds so painful, and I appreciate you sharing that with me. How can I help?",
                       "I know things seem bleak now, but it can be hard to see possible solutions when you feel so overwhelmed.", 
                       "I'm concerned about you because I care, and I want to offer support however I can. You can talk to me.",
                       "I'm always here if you feel like talking.",
                       "I'm always here to listen, but do you think a therapist could help a little more?",
                       "Have you thought about talking to a therapist?",
                       "You can withstand any storm and when you are too tired to stand, I will hold you up. You are never alone.", 
                       "You know I’m always here for you.",
                       "You’re allowed to have bad days, but remember tomorrow is a brand new day.",
                       "You’ve got a place here on Earth for a reason.",
                       "It's okay to have such thoughts but if they become overwhelming, don't keep it to yourself. I am here for you.", 
                       "Everything is a season, and right now you’re in winter. It’s dark and cold and you can’t find shelter, but one day it’ll be summer, and you’ll look back and be grateful you stuck it out through winter.",
                       "I know you are going through a lot and you’re scared, but you will never lose me.",
                       "I know it feels like a lot right now. It’s OK to feel that way.",
                       "Is there anything I can do to make this day go easier for you?"]

helpline_message = "In times of severe distress where you need to speak with someone immediately, these are suicide hotline services available for you. You will be speaking with volunteers or professionals who are trained to deal with suicide crisis. Samaritans of Singapore (SOS; 24 hours): 1800 221 4444 Mental Health Helpline (24 hours): 6389 2222 Singapore Association for Mental Health (SAMH) Helpline: 1800 283 7019"

def load_suicide_tokenizer_and_model(tokenizer="google/electra-base-discriminator", model=r"C:\Users\ravip\OneDrive\Desktop\Aman\model\electra"):
  """Load tokenizer and model instance for suicide text detection model."""

  suicide_tokenizer = AutoTokenizer.from_pretrained(tokenizer)
  suicide_model = AutoModelForSequenceClassification.from_pretrained(model)
  
  return suicide_tokenizer, suicide_model

msg=""
def check_intent(text):
  """Check if suicidal intent is present in text"""

  global suicide_tokenizer, suicide_model

  tokenised_text = suicide_tokenizer.encode_plus(text, return_tensors="pt")

  logits = suicide_model(**tokenised_text)[0]

  prediction = round(torch.softmax(logits, dim=1).tolist()[0][1])
  

  print("====================> Predicition:",prediction)

  return prediction

myResponse=""
def generate_response(tokenizer, model, chat_round, chat_history_ids,user_input):
  """Generate a response to some user input."""

  if user_input == "exit":
    raise Exception("End of Conversation")

  # Encode user input and End-of-String (EOS) token
  new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

  # Append tokens to chat history
  bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_round > 0 else new_input_ids

  # Generate response given maximum chat length history of 1250 tokens
  chat_history_ids = model.generate(bot_input_ids, max_length=1250, pad_token_id=tokenizer.eos_token_id)

  # Print response based on intent
  global myResponse
  if check_intent(user_input):
    myResponse=random.choice(prevention_messages)
    print("*:* {}".format(myResponse))
    # print("{}".format(helpline_message))

  else:

    print("*Alex:* {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

  # Return the chat history ids
  return chat_history_ids

# Initialize chatbot tokenizer and model
def customload_tokenizer_and_model():
    tokenizer = AutoTokenizer.from_pretrained("dialogpt_tokenizer")
    model = AutoModelForCausalLM.from_pretrained("dialogpt_model")

    return tokenizer, model
    
tokenizer, model = customload_tokenizer_and_model()
print("***********Tokenizer and Model Loaded Successfully*********")

# Initialize chatbot history variable
chat_history_ids = None

# Initialise suicide detection tokenizer and model
suicide_tokenizer, suicide_model = load_suicide_tokenizer_and_model()
chat_history_ids = None
print("***********suicide_tokenizer and suicide_model Loaded Successfully*********")

def start_chatbot(user_input,n=1):
  """
  Chat with chatbot for n rounds
  """

  global tokenizer, model, chat_history_ids,myResponse

  # input() might not be able to run due to this line, restart the notebook
  print(start_message)

  # Chat for n rounds
  try:
    for chat_round in range(n):
      chat_history_ids = generate_response(tokenizer, model, chat_round, chat_history_ids,user_input)
  except Exception as e:
    print("Thank you! Have a good day...")

def getResponse(user_input):
  print("==============> User Message:",user_input)
  if check_intent(user_input):
    global msg
    msg=random.choice(prevention_messages)
    res=1
  else:
    msg=""
    res=0

  return res,msg

print("========>ADV Prediction Loaded Successfully<=========")


