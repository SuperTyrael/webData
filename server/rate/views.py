import json
from pydoc import allmethods
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

from rate.models import ModuleInstance, Professor, Module, Rating
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg


def index(request):
    return HttpResponse("hello world")


@csrf_exempt
def register(request):
    req = json.loads(request.body)
    username = req.get('username')
    email = req.get('email')
    password = req.get('password')
    User.objects.create_user(username, email, password, is_superuser=False)
    return HttpResponse("Successfully registered!")


@csrf_exempt
def log_in(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    req = json.loads(request.body)
    username = req.get('username')
    password = req.get('password')
    user_obj = auth.authenticate(request, username=username, password=password)
    if user_obj is not None:
        login(request,user_obj)
        return HttpResponse("Successfully logged in!")
    else:
        http_bad_response.write("Invalid username or password")
        return HttpResponse(http_bad_response)


def log_out(request):
    logout(request)
    return HttpResponse("Successfully logout!")


def list_modules(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if request.user.is_authenticated:
        allModules = ModuleInstance.objects.all()
        module_list = []
        for module in allModules:
            item = {
                'module_id': module.module.code,
                'module_name': module.module.name,
                'module_year': module.year, 'module_semester': module.semester, 'module_professor': list(module.professor.all().values_list('name', flat=True)),
                'professor_id': list(module.professor.all().values_list('id', flat=True))}

            module_list.append(item)

        payload = {'modules': module_list}
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code = 200
        http_response.reason_phrase = 'OK'
        return HttpResponse(http_response)
    else:
        http_bad_response.write("You are not logged in")
        return HttpResponse(http_bad_response)


@csrf_exempt
def view(request):
    if request.user.is_authenticated:
        professors = Professor.objects.all()
        info = []
        for i, professor in enumerate(professors):
            avg_rating = Rating.objects.filter(professor_id=professor.id).aggregate(Avg('rate'))
            info.append({'professor_id': professor.id, 'professor_name': professor.name, 'average_rating': avg_rating['rate__avg']})
        return HttpResponse(json.dumps(info))
    else:
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.write("You are not logged in")
        return HttpResponse(http_bad_response)


@csrf_exempt
def average(request):
    if request.user.is_authenticated:
        req = json.loads(request.body)
        professor_id = req.get('professor_id')
        module_code = req.get('module_code')

        #ratings of the professor
        average_rating = Rating.objects.filter(module__module__code=module_code,professor=professor_id).aggregate(Avg('rate'))
        info = {
            'professor_name': Professor.objects.get(id=professor_id).name,
            'professor_id':professor_id,
            'module_code':module_code,
            'module_name': Module.objects.get(code=module_code).name,
            'rating': average_rating['rate__avg']
        }
        return HttpResponse(json.dumps(info))
    else:
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.write("You are not logged in")
        return HttpResponse(http_bad_response)

@csrf_exempt
def rating(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'
    if request.user.is_authenticated:
        rate_data = json.loads(request.body)

        module_code = rate_data.get('module_code')
        professor_id = rate_data.get('professor_id')
        rating = rate_data.get('rating')
        year = rate_data.get('year')
        semsester = rate_data.get('semester')
        user_id = request.user.id

        module_instance = ModuleInstance.objects.filter(module=module_code, year=year,semester=semsester)
        professor = Professor.objects.get(id=professor_id)
        if (module_instance.count() != 0):
            if (Rating.objects.filter(module=module_instance[0],user=user_id).count()==0):
                Rating.objects.create(user = request.user, module = module_instance[0], professor = professor, rate = rating)
                return HttpResponse("Successfully rated!")
            else:
                http_bad_response.write("Sorry you already rated this module")
                return http_bad_response
        else:
            http_bad_response.write("Invalid module information")
            return HttpResponse(http_bad_response)
    else:
        http_bad_response.write("You are not logged in")
        return HttpResponse(http_bad_response)

