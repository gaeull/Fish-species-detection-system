from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Caught_fish, Fish
from .serializers import CaughtFishSerializer
from django.http import QueryDict

# from .tasks import decision
# from celery.result import AsyncResult

from datetime import datetime, timedelta

import requests
from django.http import HttpResponse
import json

from django.http import JsonResponse
import math

# 금지체장 비교 함수
def length_cp(fish_info, request):
    E_fish_name = fish_info['name']
    fish_dic = Fish.objects.all()

    len = fish_dic.filter(E_fish_name=E_fish_name).values('prohibition_length')

    for i in len:
        length = i['prohibition_length']    

    user_length = float(request.POST['length'])

    if user_length <= length:
        length_return = "포획 불가능"
    else:
        length_return = "포획 가능"

    return length_return

# 금어기 비교 함수
def phdate_cp(fish_info, request):
    E_fish_name = fish_info['name']
    fish_dic = Fish.objects.all()

    startdate = fish_dic.filter(E_fish_name=E_fish_name).values('start_date')
    enddate = fish_dic.filter(E_fish_name=E_fish_name).values('end_date')

    for i in startdate:
        start = i['start_date']

    for i in enddate:
        end = i['end_date']

    today = datetime.today()

    sm = start.month
    lm = end.month
    tm = today.month

    sd = start.day
    ld = end.day
    d = today.day

    if sm<=tm and tm<=lm:
        if sm==tm:
            if d >= sd:
                returnVal = "포획 불가능"
            else:
                returnVal = "포획 가능"
        elif lm==tm:
            if d <= ld:
                returnVal = "포획 불가능"
            else:
                returnVal = "포획 가능"
        else :
            returnVal = "포획 불가능"
    else :
        returnVal = "포획 가능"

    return returnVal

# 최종 판별 결과 리턴
def Final_result(fish_info, request):
    length = length_cp(fish_info, request)
    date = phdate_cp(fish_info, request)

    if length == "포획 불가능": 
        final_return = "최종 포획 불가능"
    elif length == "포획 가능" and date == "포획 가능": 
        final_return = "최종 포획 가능"
    elif length == "포획 가능" and date == "포획 불가능":
        final_return = "최종 포획 불가능"
    else:
        final_return = "최종 포획 가능"
    
    return final_return

# discern = DB에 저장된 금어기 정보 불러와서 딥러닝 판별결과랑 비교해서 최종 포획 가능 여부 판별하는 함수.
# fish_ifo = 사용자 입력(위치, 길이, 이미지)
def discern(fish_info, request): 
    confidence = fish_info["confidence"]
    final_confidence = math.trunc(confidence * 100)
    
    final_return2 = Final_result(fish_info, request)
    confidence_info = indistinguishable(fish_info, request)

    E_fish_name = fish_info['name']
    fish_dic = Fish.objects.all()
    fish_name = fish_dic.get(E_fish_name=E_fish_name).fish_name
    return_sd = fish_dic.get(E_fish_name=E_fish_name).start_date
    return_ed = fish_dic.get(E_fish_name=E_fish_name).end_date
    return_region = fish_dic.get(E_fish_name=E_fish_name).prohibition_region
    return_length = fish_dic.get(E_fish_name=E_fish_name).prohibition_length

    return fish_name, final_confidence, return_sd, return_ed, return_length, return_region, final_return2, confidence_info

# 식별 결과 임계값 0.5 이하일 경우, 판별 불가 안내(=미탐)
def indistinguishable(fish_info, request):
    confidence = fish_info["confidence"]
    final_confidence = math.trunc(confidence * 100)

    if final_confidence <= 50:
        confidence_return = "판별 불가"
    else: 
        confidence_return = "해당없음"

    return confidence_return

class Caught_fish_View(generics.CreateAPIView):
    serializer_class = CaughtFishSerializer

    def post(self, request):  
        req_serializer =  CaughtFishSerializer(data=request.data)

        # 이미지 파일 가져오기
        image_file = request.FILES.get('image')

        # flask 서버로 이미지 파일 전송
        if image_file:
            url = 'http://127.0.0.1:5002/v1/object-detection/fishmo.pt'
            files = {'image': image_file}
            response = requests.post(url, files = files)
            resultVal = response.content
            # bytes 타입을 문자열로 변환
            resultVal_str = resultVal.decode('utf-8')
            resultVal_dic = json.loads(resultVal_str)
            resultVal_list = list(resultVal_dic)
            
            # 인식 불가, None리턴
            if resultVal_list == b'[]':
                discernVal = None
                return JsonResponse({"response": "{0}".format(discernVal)}, status=200)
            
            # ai로부터 결과값이 2개 이상일 때의 예외처리
            elif len(resultVal_list) > 1:
                return JsonResponse({"response": "한 마리 사진만 입력하세요"}, status=200)
            
        else:
            resultVal_str = None

        # ai서버로부터 받은 결과값을 딕셔너리로 반환
        result_dict = json.loads(resultVal_str)

        # 정확도, 어류 이름 딕셔너리로 반환(식별)
        resultVal_str = {"confidence": result_dict[0]['confidence'], "name": result_dict[0]['name']}
        discernVal = discern(resultVal_str, request)
        
        return JsonResponse({"response": "{0}".format(discernVal)},status=200)


