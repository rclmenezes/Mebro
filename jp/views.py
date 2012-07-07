from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from jp.models import *
import json
from datetime import datetime, timedelta

# Proof of concept stuff
def get_current():
    entry = RainbowEntry.objects.order_by('-added')[0:1]
    current = entry[0].base
    return get_next(current)

def get_next(current):
    encode = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', 
                '2', '3', '4', '5', '6', '7', '8', '9', ',', 
                '.']
    
    if current == '':
        return encode[0]
    if current[-1] != encode[-1]:
        return current[:-1] + encode[encode.index(current[-1])+1]
    return get_next(current[:-1]) + encode[0]

def proof(request):
    base = get_current()
    return render_to_response("code-2.html")
    
def rainbow(request):
    base = get_current()
    return render_to_response("rainbow.js", {'base': base})
   
# Final stuff 
def home(request):
    if request.COOKIES.has_key( 'client_id' ):
        cookie = True
        client_id = request.COOKIES[ 'client_id' ]
        client = Client.objects.get(client_id=int(client_id))
        project = client.preferred_project
    else:
        cookie = False
        project = Project.objects.order_by('?')[0]
        client = Client(preferred_project=project)
        client.save()
    
    if request.method == "POST" and 'project' in request.POST:
        project = Project.objects.get(project_id=int(request.POST['project']))
        client.preferred_project = project
        client.save()
    projects = Project.objects.all()
    response = render_to_response('home.html', {"client": client, 'projects': projects})

    if not cookie:
        expires = datetime.now() + timedelta(days=365*20)
        response.set_cookie( 'client_id', str(client.client_id), expires=expires)
    return response
    
def work(request):
    if request.COOKIES.has_key( 'client_id' ):
        cookie = True
        client_id = request.COOKIES[ 'client_id' ]
        client = Client.objects.get(client_id=int(client_id))
        project = client.preferred_project
    else:
        cookie = False
        project = Project.objects.order_by('?')[0]
        client = Client(preferred_project=project)
        client.save()
        
    response = render_to_response(project.name + '_work.html', {'code': project.code})
        
    if not cookie:
        expires = datetime.now() + timedelta(days=365*20)
        response.set_cookie( 'client_id', str(client.client_id), expires=expires)
    return response
    
def checkpoint(request):
    if request.COOKIES.has_key( 'client_id' ) and request.method == "GET" and 'project' in request.GET and 'checkpoint' in request.GET:
        client_id = request.COOKIES[ 'client_id' ]
        client = Client.objects.get(client_id=int(client_id))
        project = Project.objects.get(name=request.GET['project'])

        try:
            # In case client lose input data
            job = Job.objects.get(client=client, input_data__project=project)
            job.checkpoint = int(float(request.GET['checkpoint'])*100)
            job.save()
        except:
            raise Http404
    
        return HttpResponse(job.checkpoint)
    else:
        raise Http404
    
def getjob(request):
    if request.COOKIES.has_key( 'client_id' ) and request.method == "POST" and 'project' in request.POST:
        client_id = request.COOKIES[ 'client_id' ]
        client = Client.objects.get(client_id=int(client_id))
        project = Project.objects.get(name=request.POST['project'])
        
        # In case client lose input data
        try:
            job = Job.objects.get(client=client, input_data__project=project)
            return HttpResponse(job.input_data.data)
        # No existing job? Make new job.
        except ObjectDoesNotExist:
            input_data = InputData.objects.order_by('?')[0]
            job = Job(client=client, input_data=input_data)
            job.save()
            input_data.num_dealt += 1
            input_data.save()
            return HttpResponse(input_data.data)
    elif request.COOKIES.has_key( 'client_id' ):
        return HttpResponse("?")
    else:
        raise Http404
    
def result(request):
    if request.COOKIES.has_key( 'client_id' ) and request.method == "POST" and 'project' in request.POST and 'result' in request.POST:
        client_id = request.COOKIES[ 'client_id' ]
        client = Client.objects.get(client_id=int(client_id))
        project = Project.objects.get(name=request.POST['project'])

        try:
            # In case client lose input data
            job = Job.objects.get(client=client, input_data__project=project)
            job.result = int(float(request.POST['result']))
            job.save()
        except:
            pass
    
        return HttpResponse(job.checkpoint)
    else:
        raise Http404

# Local data stuff
def localStorage(request):
    return render_to_response("code-3.html")
    
# Cross domain stuff
def ajax(request):
    # save values
    entry = RainbowEntry(base=request.GET['base'], hashes=request.GET['hashes'])
    entry.save()
    
    callback = request.GET.get('callback', 'callback123')
    req = {}
    req ['base'] = get_current()
    response = json.dumps(req)
    response = callback + '(' + response + ');'
    return HttpResponse(response, mimetype="application/json")
    
def getData(request):
    return render_to_response("getData.js")
    
def cross_localStorage(request):
    return render_to_response("code-4.html")