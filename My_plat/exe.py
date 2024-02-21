from django.views.decorators.csrf import csrf_exempt
from My_plat import models
from django.http import HttpResponse, JsonResponse
import json, requests
from My_plat import apiii
import time  








@csrf_exempt
def transcribe_view(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if audio_file is None or not audio_file.name.endswith('.wav'):
            return JsonResponse({'error': 'Invalid audio file'})

        with open('record.wav', 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        result = apiii.ASR_WHISPER('record.wav')
        return JsonResponse({'result': result})
    
    return JsonResponse({'error': 'Invalid request method'})



API_URL = "https://api.openai.com/v1/images/generations"
@csrf_exempt 
def generate_image(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        headers = {
            "Authorization": f"Bearer {api}",
            "Content-Type": "application/json",
     }
        data = {
            "model": "image-alpha-001",
            "prompt": text,
            "num_images": 1,
            "size": "256x256",
            "response_format": "url",
    }
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()
        print(response_data)
        image_url = response_data["data"][0]["url"] 
        image_data = image_url
        print(image_data)
        response = HttpResponse(image_data)
        return response





previous_response = ""
@csrf_exempt
def text_generation_function(request):
    """ 
    this function execute the text_generation api, it's a master piece :* 
    """

    global previous_response
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        print(previous_response)
        if previous_response=="":
             response = apiii.GPT35(text)
        else:
             response = apiii.GPT35(previous_response)
    
        previous_response = response[0]["generated_text"]
        
        
        return JsonResponse({"generated_text": response[0]["generated_text"]})
    
@csrf_exempt
def wassim_gen(request):
    """ 
    this function execute the text_generation api, it's a master piece :* 
    """

    global previous_response
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        time.sleep(2)
        
        response= "machine learning is a field of study and practice that focuses on developing algorithms and models that allow computers to learn and make predictions or decisions without being explicitly programmed. By using statistical techniques and large datasets, machine learning enables computers to analyze and interpret complex patterns and relationships in data."
        
        return JsonResponse({"generated_text": response })



@csrf_exempt
def GPT_turbo(request):
    """
    this function execute the gpt35 api
    """

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        response = apiii.GPT35(text)
        return HttpResponse(response)
    





@csrf_exempt
def summarizer_function(request):
    """ this function execute the summarization api"""

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        time.sleep(0.3)
        s = apiii.Summarizer(text)
        print(s)
        return JsonResponse({'summary': s[0]['summary_text']})


#







@csrf_exempt
def Translation(request):
    """this function execute the translator api"""

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body.get('text', "")
        to_lang = body.get('to_language', "")
        if to_lang == "German":
            time.sleep(0.01) 
            translated = apiii.Translator(text)   
            print(translated) 
        elif to_lang == "Arabic":
            time.sleep(0.01) 
            translated = apiii.en2ar(text)    
            print(translated,"hey")
        elif to_lang=="French":
            time.sleep(0.2) 
            print("hhhh")
            translated = apiii.french_translator(text)
            print(translated)
        elif to_lang=="English":
            time.sleep(0.02) 
            print("hhhh")
            translated=apiii.ar2en(text)
            print(translated)
        else:
            return HttpResponse("please select a language")
        
        return JsonResponse({'translation':translated[0]["translation_text"]})
    

      





""" this is a gpt3.5 response about how he could help us:  interesting response

    As an AI language model, I can assist you in several areas, such as:
1. Writing: I can help in drafting emails, creating content for social media, writing essays or reports, etc.
2. Research: I can assist in finding information on a particular topic and help in organizing it.
3. Math and Science: I can solve mathematical problems, equations, and help in understanding scientific theories andconcepts.
4. Translation: I can translate text from one language to another.
5. Time Management: I can help you manage your schedule, set reminders, and plan your tasks.
6. Personalized assistance: I can provide suggestions based on your interests, preferences, and behavior patterns.
Please let me know how I can best assist you!




"""


