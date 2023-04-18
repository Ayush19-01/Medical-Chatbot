import os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from .predictor import Prediction
import json
@csrf_exempt
def test(request):
    if request.method == 'GET':
        return JsonResponse({"response": "Hello, welcome to the chatbot"})
    elif request.method == 'POST':
        symptom_l = json.loads(request.body)['symptoms']
        tmp = Prediction(symptom_l)
        data = tmp.predict()

        return JsonResponse({"status":status.HTTP_200_OK,"posted data":symptom_l,"disease_data":data,})
    else:
        return JsonResponse({'error': 'Invalid request method',})





