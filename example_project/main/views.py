import json
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
#from Loggin.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from main.models import UserData,Project,TotalG
from django.contrib.auth.models import User
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from main.forms import UserDataForm,ProjectForm,UploadFileForm
from django.db.models import Max
from django.conf import settings


def index(request):
    return render_to_response("index.html",
            context_instance=RequestContext(request))

@login_required
@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def home(request):
    projects = Project.objects
    projects = projects.filter(user=request.user)
    projects = projects.order_by('date').all()
    username=request.user.username
    return render_to_response("home.html", {
        'username': username, 'projects': projects
    }, context_instance=RequestContext(request))


def set_temporary_file_upload_handler(request):
    # Disable in memory upload before accessing POST
    # because we need a file from which to read metadata
    request.upload_handlers = [TemporaryFileUploadHandler()]

@login_required
@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def upload(request):
    set_temporary_file_upload_handler(request)
    if request.method == "POST":
        print request.POST
        form = UserDataForm(request.user,request.POST, request.FILES,)
        print form
        if form.is_valid():
            print 'sddkdhsjkdf'
            excel_file = request.FILES['excelsheet']
            print excel_file.name
            projectName=request.POST['Project_name']
            excel_file_path = excel_file.temporary_file_path()
            #print excel_file_path
            user_data = form.save(commit=False)
            p=Project.objects.filter(projectName=projectName)
            project_obj=p[0]
            user_obj_list=UserData.objects.filter(project=project_obj)
            flag=0
            if len(user_obj_list)>0:
                flag=1
            user_data.project = project_obj
            user_data.save()
            
            if flag>0:
                dd=UserData.objects.filter(project=project_obj).aggregate(Max('version'))
                print dd
                user_data.version=dd['version__max']+1

            ff=str(user_data.excelsheet)
            user_data.file_path=settings.MEDIA_ROOT+"/"+str(ff)
            fff= ff.split('/')
            user_data.file_name=fff[1]
            user_data.save()
            #print user_data.excelsheet
            #print user_data.file_path
            print settings.MEDIA_URL
            return HttpResponseRedirect('/')

    else:
        form = UserDataForm(request.user)
    return render_to_response("upload.html", {'form': form},
                              context_instance=RequestContext(request))

@login_required
@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            user_data = form.save(commit=False)
            user_data.user = request.user
            #print user_data.project
            user_data = form.save()
            return HttpResponseRedirect('/project')
    else:
        form = ProjectForm()
    return render_to_response("project.html", {'form': form},
                              context_instance=RequestContext(request))


@login_required
@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def project_details(request,project_id):
    print project_id
    p=Project.objects.get(pk=project_id)
    username=p.user.username
    userdata_list=UserData.objects.filter(project=p)
    return render_to_response("excel.html", {
        'username': username, 'userdatas': userdata_list,'project':p
    }, context_instance=RequestContext(request))



@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def apiUpload(request,user_data_id):
    #print project_id
    print 'apiUpload called'
    print request
    print request.POST
    print request.FILES
    print 'ddfj'
    user_data = UserData.objects.get(pk=user_data_id)
    print user_data.file_path
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES, instance=user_data)
        if form.is_valid():
            form = form.save()
            ff=str(form.excelsheet)
            form.file_path=settings.MEDIA_ROOT+"/"+str(ff)
            fff= ff.split('/')
            form.file_name=fff[1]
            form.processed=1;
            form.save();
            resp={}
            resp["status"]="success"
            resp["message"]="updatd db succesfully"
            return HttpResponse(json.dumps(resp), content_type='applications/json; charset=utf-8', status=200)
    
    else:
        resp={}
        resp["status"]="failed"
        resp["message"]="please use post method"
        return HttpResponse(json.dumps(resp), content_type='applications/json; charset=utf-8', status=500)


@login_required
@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def add_edit_effort(request,project_id):
    print project_id
    p=Project.objects.get(pk=project_id)
    if request.method=='POST':
        print request.POST
        username=p.user.username
        P1T1=request.POST['P1T1']
        P1T2=request.POST['P1T2']
        P1T3=request.POST['P1T3']
        P1T4=request.POST['P1T4']

        P2T1=request.POST['P2T1']
        P2T2=request.POST['P2T2']
        P2T3=request.POST['P2T3']
        P2T4=request.POST['P2T4']

        P3T1=request.POST['P3T1']
        P3T2=request.POST['P3T2']
        P3T3=request.POST['P3T3']
        P3T4=request.POST['P3T4']
     

        phase1=TotalG.objects.filter(project=p,phase=1)
        phase2=TotalG.objects.filter(project=p,phase=2)
        phase3=TotalG.objects.filter(project=p,phase=3)
        if len(phase1)==0:
            phase1=TotalG(project=p,phase=1,TG1=P1T1,TG2=P1T2,TG3=P1T3,TG4=P1T4)
            phase1.save()
        else:
            phase1=phase1[0]
            phase1.TG1=P1T1
            phase1.TG2=P1T2
            phase1.TG3=P1T3
            phase1.TG4=P1T4
            phase1.save()

        if len(phase2)==0:
            phase2=TotalG(project=p,phase=2,TG1=P2T1,TG2=P2T2,TG3=P2T3,TG4=P2T4)
            phase2.save()
        else:
            phase2=phase2[0]
            phase2.TG1=P2T1
            phase2.TG2=P2T2
            phase2.TG3=P2T3
            phase2.TG4=P2T4
            phase2.save()

        if len(phase3)==0:
            phase3=TotalG(project=p,phase=3,TG1=P3T1,TG2=P3T2,TG3=P3T3,TG4=P3T4)
            phase3.save()
        else:
            phase3=phase3[0]
            phase3.TG1=P3T1
            phase3.TG2=P3T2
            phase3.TG3=P3T3
            phase3.TG4=P3T4
            phase3.save()

        return HttpResponseRedirect('/home')
    
    else:
        print p
        TG={}
        phase1=TotalG.objects.filter(project=p,phase=1)
        phase2=TotalG.objects.filter(project=p,phase=2)
        phase3=TotalG.objects.filter(project=p,phase=3)

        if len(phase1)==0:
            TG['P1T1']=''
            TG['P1T2']=''
            TG['P1T3']=''
            TG['P1T4']=''
        else:
            phase1=phase1[0]
            TG['P1T1']=phase1.TG1
            TG['P1T2']=phase1.TG2
            TG['P1T3']=phase1.TG3
            TG['P1T4']=phase1.TG4

        if len(phase2)==0:
            TG['P2T1']=''
            TG['P2T2']=''
            TG['P2T3']=''
            TG['P2T4']=''
        else:
            phase2=phase2[0]
            TG['P2T1']=phase2.TG1
            TG['P2T2']=phase2.TG2
            TG['P2T3']=phase2.TG3
            TG['P2T4']=phase2.TG4

        if len(phase3)==0:
            TG['P3T1']=''
            TG['P3T2']=''
            TG['P3T3']=''
            TG['P3T4']=''

        else:
            phase3=phase3[0]
            TG['P3T1']=phase3.TG1
            TG['P3T2']=phase3.TG2
            TG['P3T3']=phase3.TG3
            TG['P3T4']=phase3.TG4

        #return HttpResponse('sjksjkd')
        print TG
        return render_to_response("efforts.html", {"project":p,'TG':TG
            }, context_instance=RequestContext(request))
        