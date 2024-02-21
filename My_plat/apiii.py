import subprocess
import requests
import torch
import json
import openai
from PIL import Image  # Import the required libraries
import base64
from io import BytesIO
import transformers
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import whisper
from diffusers import StableDiffusionPipeline


def ASR_WHISPER(payload) :
        file = open(payload, "rb")
        response = openai.Audio.transcribe("whisper-1", file)
        return (response["text"]) 

# Use the text generation function to generate a response
def GPT35(payload) :
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content":payload }])
        return (response["choices"][0]["message"]["content"]) 



def french_translator(payload):
	response = requests.post(API_URL_fr, headers=headers, json=payload)
	return response.json()
	

 


def Translator(payload):
	response = requests.post(API_URL_translator, headers=headers, json=payload)
	return response.json()



def en2ar(payload):
	response = requests.post(API_URL_en2ar, headers=headers, json=payload)
	return response.json()
  


def ar2en(payload):
	response = requests.post(API_URL_ar2en, headers=headers, json=payload)
	return response.json()


def Summarizer(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL_Summarizer, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

def QA(payload):
	response = requests.post(API_URL_QA, headers=headers, json=payload)
	return response.json()
