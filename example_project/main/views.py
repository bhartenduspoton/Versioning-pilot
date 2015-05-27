from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
#from Loggin.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from main.models import UserData,Project
from django.contrib.auth.models import User
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from main.forms import UserDataForm,ProjectForm
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
        'username': username, 'userdatas': userdata_list
    }, context_instance=RequestContext(request))



@csrf_exempt  # request.POST is accessed by CsrfViewMiddleware
def apiUpload(request):
    #print project_id
    print 'apiUpload called'
    print request.POST
    print request.File

    if request.method == "POST":
        user_data_id=request.POST['user_data_id']
        p=Project.objects.get(pk=project_id)
        username=p.user.username
        userdata_list=UserData.objects.filter(project=p)
        return render_to_response("excel.html", {
            'username': username, 'userdatas': userdata_list
        }, context_instance=RequestContext(request))
    
    else:
        return HttpResponse('Only POST here')
