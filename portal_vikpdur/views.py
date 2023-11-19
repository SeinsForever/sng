import os
from threading import Timer
import json
import time

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from .models import History_plan, Structure, Cdng, Debits

def api_data_check_function():

    # with open(static('json/dataASUmonth.json')) as f:
    print("=============")
    print("Start checking JSON!")
    print("=============")
    with open("/Users/ivan/PycharmProjects/sng/portal_vikpdur/static/json/dataASUmonth.json") as f:
        data = json.load(f)

    for cdng in data["cdngs"]:
        print(f'{cdng["name"]} {cdng["uuid"]}')

        try:
            Cdng.objects.get(cdng_uuid=cdng["uuid"])
            print("already added in DB CDNG")
        except:
            try:
                Cdng.objects.create(structure_id=1,cdng_uuid=cdng["uuid"], cdng_name=cdng["name"], master_name=cdng["master"], master_phone=cdng["masterPhone"])
            except Exception as e:
                print("------error with db", e)
                return JsonResponse({"Result": "Error", "Description": "DB create problem"}, status=400)

        cdng_id_helper = Cdng.objects.get(cdng_uuid=cdng["uuid"])
        debits_last_date = Debits.objects.filter(cdng_id=cdng_id_helper.id).order_by("-date_time")[:1]
        for dld in debits_last_date:
            debits_last_date_value = dld.date_time
        print("Last value in JSON = ", debits_last_date_value)
        for deb in reversed(cdng["debits"]):
            # print("check deb dt = ", debits_last_date_value , deb["dt"])
            if int(debits_last_date_value) == int(deb["dt"]):
                print("debit data in DB = ", deb["dt"])
                break
            else:
                Debits.objects.create(date_time=deb["dt"], cdng_id=cdng_id_helper.id, debit=deb["debit"])

    print("=============")
    print("Data checked!")
    print("=============")

    return 0

api_data_check_function()

def index(request):
    try:
        name = request.session["name"]
    except KeyError:
        return HttpResponse("No login.")

    return HttpResponseRedirect("/mainpage")


def api_user_auth(request):
    name = request.GET.get("name", "Undefined")
    request.session["name"]=name
    print("Name has been set", request.session["name"])
    # response = HttpResponse(f"name:{name}")
    # return response
    return JsonResponse({"Result": "Success", "Name": name}, status=200)
    # return HttpResponseRedirect("")


def api_user_logout(request):
    try:
        print("delete session name")
        del request.session["name"]
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


def api_get_data(request):
    with open("/Users/ivan/PycharmProjects/sng/portal_vikpdur/static/json/dataASUmonth.json") as f:
        data = json.load(f)

    return JsonResponse(data)

    # try:
    #     cdng = Cdng.objects.get(cdng_uuid=cdng_id)
    # except:
    #     return JsonResponse({"Result": "Error", "Description": "DB create problem"}, status=400)
    # data = {}
    # history = History_plan.objects.filter(cdng_id=cdng.id)
    # data["someChanges"] = []
    # arr = []
    # for item in history:
    #     obj = {"editorName": item.editor_name, "dateTime": item.date_time, "newScorePlan": item.new_score_plan}
    #     print(obj)
    #     arr.append(obj)
    # data["someChanges"] = arr

    # return JsonResponse(data, safe=False)

def api_get_data_history(request):

    cdng_id = request.GET.get("uuid", "")

    try:
        cdng = Cdng.objects.get(cdng_uuid=cdng_id)
    except:
        return JsonResponse({"Result": "Error", "Description": "DB create problem"}, status=400)
    data = {}
    history = History_plan.objects.filter(cdng_id=cdng.id)
    data["someChanges"] = []
    arr = []
    for item in history:
        obj = {"editorName":item.editor_name, "dateTime":item.date_time, "newScorePlan":item.new_score_plan}
        print(obj)
        arr.append(obj)
    data["someChanges"] = arr

    return JsonResponse(data, safe=False)

def api_get_predict_data(request):
    uuid = request.GET.get("uuid", "")
    # date = request.GET.get("date", "") # Раскомментировать, если Дима доделает
    # if cdng_id == "" or date == "": # Раскомментировать, если Дима доделает
    if uuid == "":
        print("Api_set_predict No data")
        return JsonResponse({"Result": "Error", "Description": "No data"}, status=400)

    try:
        cdng = Cdng.objects.get(cdng_uuid=uuid)
        print(cdng.id)
        result = History_plan.objects.filter(cdng_id=cdng.id)
        for res in result:
            print(res.new_score_plan)
        # result = History_plan.objects.all(cdng_id=cdng.id, datetime=date) # Раскомментировать, если Дима доделает
        return JsonResponse({"Result": "Success"}, status=200)
    except Exception as e:
        return JsonResponse({"Result": "Error", "Description": e}, status=400)




def main_page_view(request):
    name = request.session["name"]
    return HttpResponse(name)
    # return render(request, "index.html")


def api_set_predict(request):
    try:
        cdng_id = request.GET.get("uuid", "")
        # name = request.session["name"]
        name = request.GET.get("name", "")
        value = request.GET.get("value", "")
        date = request.GET.get("date", "")
        print(cdng_id, name, value, date)
        if cdng_id == "" or value == "" or name == "" or date == "":
            print("Api_set_predict No data")
            return JsonResponse({"Result": "Error", "Description": "No data"}, status=400)

        try:
            cdng = Cdng.objects.get(cdng_uuid=cdng_id)
            result = History_plan.objects.create(editor_name=name, date_time=date, new_score_plan=value, cdng_id=cdng.id)
            print(result.id)
            # result = History_plan.objects.filter(editor_name=request.session["name"])
        except:
            print("smth wrong with db filter")
            return JsonResponse({"Result": "Error", "Description": "smth wrong with db filter"}, status=400)
        # for res in result:
        #     print(res.new_score_plan)
        # History_plan.objects.create(cdng_id=)
        return JsonResponse({"Result": "Success"}, status=200)
    except Exception as e:
        print("ERROR",e)
        return JsonResponse({"Result": "Error", "Description": e}, status=400)


