#-------------------------------------ICON_SCORE-------------------------------------------
import json, time, datetime
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.icon_service import IconService
from iconsdk.builder.call_builder import CallBuilder


#-------------------------------------Server-------------------------------------------
from .models import Receive_Google_Data, Receive_Naver_Data
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max

#-------------------------------------ICON_SCORE_option-------------------------------------------
_score_address = "cx58833c3d35953053ecc21bf814ce117765c640e4"
_keystore_address = "hx62ad26ca172e347300fa795bb5b554c9123b64ed"
node_uri = "https://bicon.net.solidwallet.io/api/v3"
icon_service = IconService(HTTPProvider(node_uri))


#-------------------------------------Naver RT-------------------------------------------

def index(request):
    userdate = request.GET.get("userdate")
    usertime = request.GET.get("usertime")

    if userdate and usertime :
        split_Date = userdate.split('-')
        split_Time = usertime.split(':')
        input_Date = "".join(split_Date)
        input_Time = "".join(split_Time)

        if int(input_Date) >= 20190200 and int(input_Date) <= 20200200:

            params = {
                "_Call_date": "".join(input_Date),
                "_Call_time": "".join(input_Time),
                "_Call_div": "NAVER"
            }

            Inquiry = CallBuilder() \
                .from_(_keystore_address) \
                .to(_score_address) \
                .method("inquiry_RT") \
                .params(params) \
                .build()
            response = icon_service.call(Inquiry)
            if response == "":
                return HttpResponse("No data")
            else:
                posts = json.loads(response)
                return render(request, 'crawling/realtime.html', {'posts': posts, 'date': userdate, 'time': usertime})


        else:
            # posts = str(Receive_Naver_Data.objects.last())
            # return render(request, 'crawling/realtime, {'posts' : posts})
            return HttpResponse("No data " + userdate)


    elif userdate == None or usertime == None:
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        nowTime = now.strftime('%H%M')
        # return HttpResponse("No data aaa" + nowDate + nowTime)
        realTime = int(nowTime) - 1
        shit = "0" + str(realTime)

        params = {
            #"_Call_date": nowDate,
            "_Call_date": "20190227",
            #"_Call_time": shit,
             "_Call_time": "0853",
            "_Call_div": "NAVER"
        }

        Inquiry = CallBuilder() \
            .from_(_keystore_address) \
            .to(_score_address) \
            .method("inquiry_RT") \
            .params(params) \
            .build()

        response = icon_service.call(Inquiry)
        posts = json.loads(response)

        temp1 = str(nowDate)[0:4]
        temp2 = str(nowDate)[4:6]
        temp3 = str(nowDate)[6:8]
        convert_date = temp1 + "-" + temp2 + "-" + temp3

        temp1 = str(shit)[0:2]
        temp2 = str(shit)[2:4]
        convert_time = temp1 + ":" + temp2

        # userdate = Receive_Naver_Data.objects.last().date - recent DB data call
        # posts = list(Post.objects.filter(date=userdate))
        return render(request, 'crawling/realtime.html', {'posts' : posts, 'date': convert_date,'time':convert_time})


#-------------------------------------Google RT-------------------------------------------

def index2(request):
    userdate = request.GET.get("userdate")
    usertime = request.GET.get("usertime")

    if userdate and usertime :
        split_Date = userdate.split('-')
        split_Time = usertime.split(':')
        input_Date = "".join(split_Date)
        input_Time = "".join(split_Time)

        if int(input_Date) >= 20190200 and int(input_Date) <= 20200200:

            params = {
                "_Call_date": "".join(input_Date),
                "_Call_time": "".join(input_Time),

                "_Call_div": "GOOGLE"
            }

            Inquiry = CallBuilder() \
                .from_(_keystore_address) \
                .to(_score_address) \
                .method("inquiry_RT") \
                .params(params) \
                .build()
            response = icon_service.call(Inquiry)
            if response == "":
                return HttpResponse("No data")
            else:
                posts = json.loads(response)
                return render(request, 'crawling/realtime_google.html', {'posts': posts, 'date': userdate, 'time': usertime})


        else:
            # posts = str(Receive_Naver_Data.objects.last())
            # return render(request, 'crawling/realtime, {'posts' : posts})
            return HttpResponse("No data " + userdate)


    elif userdate == None or usertime == None:
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        nowTime = now.strftime('%H%M')
        # return HttpResponse("No data aaa" + nowDate + nowTime)
        realTime = int(nowTime) - 1
        shit = "0" + str(realTime)

        params = {
            #"_Call_date": nowDate,
            #"_Call_time": shit,
            "_Call_date": "20190227",
            "_Call_time": "1006",
            "_Call_div": "GOOGLE"
        }

        Inquiry = CallBuilder() \
            .from_(_keystore_address) \
            .to(_score_address) \
            .method("inquiry_RT") \
            .params(params) \
            .build()

        response = icon_service.call(Inquiry)
        posts = json.loads(response)

        temp1 = str(nowDate)[0:4]
        temp2 = str(nowDate)[4:6]
        temp3 = str(nowDate)[6:8]
        convert_date = temp1 + "-" + temp2 + "-" + temp3

        temp1 = str(shit)[0:2]
        temp2 = str(shit)[2:4]
        convert_time = temp1 + ":" + temp2

        # userdate = Receive_Naver_Data.objects.last().date - recent DB data call
        # posts = list(Post.objects.filter(date=userdate))
        return render(request, 'crawling/realtime_google.html', {'posts' : posts, 'date': convert_date,'time':convert_time})



def top(request):
    userdate = request.GET.get("userdate")

    if userdate:
        split_Date = userdate.split('-')
        input_Date = "".join(split_Date)

        if int(input_Date) >= 20190200 and int(input_Date) <= 20200200:
            temp_posts = list(Receive_Naver_Data.objects.filter(key1=input_Date).order_by('-N_Rating'))
            posts = temp_posts[0:20]

            return render(request, 'crawling/realtime_Top20.html', {'posts': posts, 'date': userdate})
        # print error
        else:
            return render(request, 'crawling/realtime_Top20.html')
    else:

        userdate = Receive_Naver_Data.objects.last().key1

        temp_posts = list(Receive_Naver_Data.objects.filter(key1=userdate).order_by('-N_Rating'))
        posts = temp_posts[0:20]

        return render(request, 'crawling/realtime_Top20.html', {'posts': posts})


def top2(request):
    userdate = request.GET.get("userdate")

    if userdate:
        split_Date = userdate.split('-')
        input_Date = "".join(split_Date)

        if int(input_Date) >= 20190200 and int(input_Date) <= 20200200:
            temp_posts = list(Receive_Google_Data.objects.filter(key1=input_Date).order_by('-G_Rating'))
            posts = temp_posts[0:20]

            return render(request, 'crawling/realtime_Top20_google.html', {'posts': posts, 'date': userdate})
        # print error
        else:
            return render(request, 'crawling/realtime_Top20_google.html')

    elif userdate == None:
        userdate = Receive_Google_Data.objects.last().key1
        temp_posts = list(Receive_Google_Data.objects.filter(key1=userdate).order_by('-G_Rating'))
        posts = temp_posts[0:20]

        return render(request, 'crawling/realtime_Top20_google.html', {'posts': posts})



def input(request):
    return render(request, 'crawling/index.html')



