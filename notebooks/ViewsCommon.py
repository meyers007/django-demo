from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import pandas as pd
import os, json, sys, re, subprocess, pkgutil

sys.path.append("../notebooks")
#sys.path.append("app1/templates")

from datetime import datetime
import threading
from numba import njit
from multiprocessing import Pool
#--------------------------------------------------------------------------------
def index(request):
    return HttpResponse("Version 1.2");
#--------------------------------------------------------------------------------
def Query(request):
    q = request.GET.get( 'q', '')
    return HttpResponse(q);
#--------------------------------------------------------------------------------
def Debug(request, APPNAME=''):
    rpath = request.path.split('/')[-2] #en(APPNAME)+2:-1]
    template = "/templates/" + rpath;
    pyModule = rpath;
    
    print(f"{template} Requested")
    getlist = [ c for c in request.GET.items()]
    ret = f''' <pre>\n Response Object: \n{os.getcwd()} path_info:{request.path_info}: final:{rpath}
               Page exists:  {template} : {os.path.exists(template)}
               Page exists:  {pyModule} : {os.path.exists(pyModule)}
               {getlist} </pre> '''
    return HttpResponse(ret);
#--------------------------------------------------------------------------------
def CommonPython(request):
    rpaths = [c for c in request.path.split("/") if (c) ];
    pyMethod = rpaths[-1];
 
    #print(f"importing ... {pyMethod} ...")
    if ( pyMethod.find("modules.") < 0 ):
        return HttpResponse(f"{pyMethod} not understood 0")
        
    spl = pyMethod.split('.');
 
    if ( len(spl) < 2):
        print("Hmmm ... May be not what is intended!! module name")
        return HttpResponse(f"{pyMethod} not understood 2");
    
    #print(f"importing ... {modName} ...")
    
    modName = ".".join(spl[:-1])
    __import__(modName, fromlist="dummy")
    
    funName = spl[-1]
    for v in sys.modules:
        if (v.startswith(modName)):
            method= getattr(sys.modules[v], funName)
            print(v, type(v), funName, method, type(method), callable(method))
            return method(request)
        
    return HttpResponse(f"{pyMethod} not understood3 ");
    
#--------------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def CommonSecured(request, apage):
    return render(request, apage)
#--------------------------------------------------------------------------------
def CommonOld(request):
    rpaths = [c for c in request.path.split("/") if (c)];
    template = "/".join(rpaths[:-1]) + "/templates/" + rpaths[-1];
    template = f"{rpaths[0]}/templates/{'/'.join(rpaths[1:])}";
    rpath = "/".join(rpaths[1:]);
    
    stemplate=template; spath=''
    if (request.path.find("/secured/") >0):
        stemplate= request.path.replace("/secured/", "/templates/secured/")[1:-1];
        if 'secured' in rpaths:
            spath = "/".join(rpaths[rpaths.index("secured"):])
        else:
            spath = "/" +rpaths[-1]

    print(rpaths, f'=>{stemplate}; {template}; {request.path.find("/secured/")}, {request.path}');
    print(rpaths, f'=*=>{stemplate}; {template}; {spath} rpath');
    
    if ( os.path.exists(stemplate) and request.path.find("/secured/") > 0) : 
        print("Secured ==> " , rpaths, "==>", stemplate);
        return CommonSecured(request, spath)
    elif ( os.path.exists(template) ):
        return render(request, rpath)
    elif rpath.startswith("modules"): #Must be a python module call
        return CommonPython(request)
    else:
        return HttpResponse(f"{rpath} not understood");
#--------------------------------------------------------------------------------
def Common(request):
    rpaths = [c for c in request.path.split("/") if (c)];
    template = f"{rpaths[0]}/templates/{'/'.join(rpaths[1:])}";
    rpath = "/".join(rpaths[1:]);
    
    print(rpaths, f'=*=>{template}; {rpaths} ++ {rpath}');
    
    if ( os.path.exists(template) and request.path.find("/secured/") > 0) : 
        print("Secured ==> " , rpaths, "==>", template);
        return CommonSecured(request, rpath)
    elif ( os.path.exists(template) ):
        return render(request, rpath)
    elif rpath.find("modules.") >= 0: #Must be a python module call
        print("**** Getting python Module")
        return CommonPython(request)
    else:
        return HttpResponse(f"{rpath} not understood");
