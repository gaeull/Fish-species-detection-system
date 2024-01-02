from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .celery import app
#from .model import Caught_fish
import requests

# celery 사용해서 비동기적으로 실행되는 Task 함수임
@shared_task
def decision(response, confidence, name):
    
    # ai_url = 'http://localhost:5001/model'
    # fish = response.objects.get()
    
    # ai서버로 요청을 보냄, 요청데이터는 json형식임.
    # test = requests.post('http://localhost:5001/test/',json={"id": response.data}) 
    test = requests.post('http://localhost:5003/',json={"id": response.data}) 
    print(test)    

    #requests.post(ai_url,json={"id":response})
    return test


