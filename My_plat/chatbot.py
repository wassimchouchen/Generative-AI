from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory.buffer import ConversationBufferMemory
import os, json,tempfile,requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
autotext_url = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"

llm=OpenAI(openai_api_key=OPENAI_API_KEY,temperature=0.7)


conversation=ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_input = body.get('input', "")
        if user_input == "mem" and conversation.verbose == False:
            conversation.verbose = True
        elif user_input == "mem" and conversation.verbose == True:
            conversation.verbose = False

        bot = conversation.predict(input=user_input)
        payload = {"inputs": bot}
        respons = requests.post(autotext_url, headers=headers, json=payload)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(respons.content)
            filename = f.name
        with open(filename, 'rb') as f:
            audio_content = f.read()
        os.unlink(filename)
        return HttpResponse(audio_content, content_type='audio/wav')
    
    return JsonResponse({'error': 'Invalid request method'})

    

    

