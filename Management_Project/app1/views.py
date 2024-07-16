# Imports

from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
import plotly.graph_objects as go
import plotly.io as pio
import os
import google.auth
from google.oauth2 import service_account
import gspread
from datetime import date
from .models import UserProfile
from .forms import AudioUploadForm


# Authorizing google service account and gspread

credential_json = {
  "type": "service_account",
  "project_id": "top-sunrise-420513",
  "private_key_id": "6792ab2b5f54fe8c496535b1b7ffa985cabfcf06",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC9kOF8i4roSBBC\n+DUcwqZ2Pw8+GLJQT4mkj+7TegPF3LJwutkGHd+mPIkE5Ql9DVTAryMEldGQsAws\nCPYvmmlmycaW78WAXbWNIdZ1tgq4DZo1Rr2+kExFd6bmA9LNfsOaKq4nbkGLxBPQ\nAAc7zJXba4YpzdW9iHo3vDna1GwbAEm7bfSen97MEmv2ZNRLuNcm80sHUsdALMsM\n1YTqEStS6WPZgyUtXpcZfJDn7Ws+0GdU+wEOe3KrmTs4Zp/51XzvXXm/uMVpRWEf\nySNMvLao6uWyDJDUpEP/uhH9x8aLCSy1HBK+EeFEYgd5ICoanb6TCXKilC6KZtoL\n5mpe+ul/AgMBAAECggEAGhp3ul86xwaZWqd0JNw28OR5FFtxPnbdZNA/GlbcayQb\nXEOWe+2kLO98DLT/S/2IdKoJP+njfDGJ04x+Xgq8xd82HfWxdB4zUFZfAkGJk1Oo\nLvrpSPL01cIGtPjEz/BLPhDvf1WC6Bydf9BpLpZa8maJiHskGh/PeJpOOzByHHt9\n86uI5A1Lop2OBieQ2rKhwsPB5NDTjIxjsyR/rISE8dJQchnnzFCRJbbznlA4drOR\nqG+G2I2xqI3RElCzlQZyYAKRGkLOfmgyP3jInm5UI8ALV88/FNPWlKI2jvvxHMat\noRhorsO0kHPPW/4ofmQED4y0AURZcdhG04naOzZjpQKBgQD7/RjJbNPQYno5zb58\nKzHrA8fQtcrSUVwEnoP2aT6sSojHsd3CQMZxSivyI4pVDk4ZOrbP1OCeljnz0Y92\n4PeXHIn8bCxbTJO7+4PHBfoIKsoH7+wYPKRTf9Xi5QHqS3Ghb8tMEt1vOv2JtO4Z\n7aWRtWbErpf+zeTe4B5RRWLcxQKBgQDAlWYv9S9r3u4dxWBKiBw/p0aFfjtItHAB\n6oTSSUYUXL+Ta4+3ewtONgBfwYpslYYU+Iv0ECF7TR1OsDf+tcd9j6A2bWhlJEp7\nuIRjzUPgzLqOpXHuPqUyABMRzVDp6kw0D+nES5FlQLZSZgQQ7Q7Mq6//Eeqp6JHn\ni9BUwSCZcwKBgDGflAQGpGfDHOLJO5vkPb5UTkMxqbFlSEO4m7Ao5ai0PN9mjY81\nhl7FBoZ2rUU2vfaF835WI63XU65KNIBqqRdfDWViQBHysJ0yWK8W5Dg7hPGvM8VK\nG+o9oHdANfJXzRbHlzdx951x9n/p24HLpPFe0dAludT54vppFE9Y5LEpAoGAPHgs\np+5Sv4o2Nj7dZ0mppQr/B7eFIeUWLmPW5LiBOq+Mr9tcOv51pE8seuSodEPW4ArS\n1wWhnbeu9iA61M17IB/S7IQZ/XgRsxtS5otzPsjJ4zRru6UL9dE0K6jOOUSKPOaq\nPiqEMsjI9sJ1kGL+/KEEGBEmH8eY2J18AsDJXaUCgYA4gwqk782JKQhDpvWdU7fm\n8aGOCdDsJJW2FVjgPp+NulHJ2/9uBGbs5g4Uy1I8Y3m92acWC7zEvzonn7HwdKAq\n2cHrVROJqbdo/VFdqHa6tsAJRNYN4gfDwCYAvu8BkucrGBvSezjgkomAV7UgoLMG\nnPM+/3LzD1Qz9myyaUQwow==\n-----END PRIVATE KEY-----\n",
  "client_email": "attendance-script@top-sunrise-420513.iam.gserviceaccount.com",
  "client_id": "102474679686669311891",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/attendance-script%40top-sunrise-420513.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}



# credential_path = 'sam_sir_project/app1/credentials.json'
credential_path = 'credentials.json'
# credentials, project = google.auth.default()
# credentials = service_account.Credentials.from_service_account_file(
#     credential_json)
scopes = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename='credentials.json', scopes=scopes)


# Create your views here.
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def HomePage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminreport')
        elif 'coordinator' not in request.user.username:
            return redirect('studentdashboard')
        else:
            return redirect('choice')
    return redirect('login')


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        batch_name = request.POST.get('batch')

        print(f"Batch: {batch_name}, uname: {uname}, pass1: {pass1} ")

        if pass1 != pass2:
            return HttpResponse("The passwords are not the same")
        else:
            # Create a new user
            user = User.objects.create_user(username=uname, password=pass1)

            # Create a UserProfile instance
            profile = UserProfile.objects.create(user=user, batch_name=batch_name)
            return redirect('login')
    return render(request, 'signup.html')


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        print(f'This is the user: {username}')
        user = authenticate(request, username = username, password = password)
        # user = SimpleUser.objects.filter(username=username, password=password).first()
        print("This user may or may not exist")
        # print(user.get_username())
        if user is not None:
            print('you are correct ')
            login(request, user)
            return redirect('home')
        else:
            # return HttpResponse('Invalid credentials')
            return render(request, 'login.html', context= {'error': 'Invalid credentials'})

    return render(request, 'login.html')

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def LogoutPage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def FormPage_1(request):
    profile = request.user.userprofile  # Assuming the related model field is 'userprofile'
    batch_name = profile.batch_name
    names = batchwise_names(batch_name)
    if request.method == 'POST':
        batch = request.POST.get('batch')
        checkbox_data = request.POST.getlist('student_names') 
        print(batch)
        print(checkbox_data)

        # database logic 
        students = {}
        for i in range(len(names)):
            students[names[i]] = i+2
            
        audio_report(batch_name, checkbox_data, students)



        return redirect('choice')
        # return HttpResponse("Submitted")
    # students = ['Muhammed Afsal','Muhammed Suhail', 'Muhammed Noushad', 'Aslah', 'Jasir', 'Devanandh', 'Jayakrishnan', 'Farsin', 'Vaisakh', 'Anil', 'Shijildas']  # Get student data from your source
    batches = ['Batch 154','Batch 155','Batch 166','Batch 167','Batch 168','Batch 186', 'Batch 198']


    # batch_and_students = {'Batch 154':['Muhammed Afsal','Muhammed Suhail', 'Muhammed Noushad', 'Aslah', 'Jasir', 'Devanandh', 'Jayakrishnan', 'Farsin', 'Vaisakh', 'Anil', 'Shijildas'],
    #                       'Batch 155':['Muhammed Noushad', 'Aslah', 'Jasir', 'Devanandh',]}

    # profile = request.user.userprofile  # Assuming the related model field is 'userprofile'
    # batch_name = profile.batch_name
    # names = batchwise_names(batch_name)

    context = {'students': names, 'batch': batch_name}
    return render(request, 'form1.html', context)


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def FormPage_2(request):
    profile = request.user.userprofile  # Assuming the related model field is 'userprofile'
    batch_name = profile.batch_name
    names = batchwise_names(batch_name)
    students = {}
    for i in range(len(names)):
        students[names[i]] = i+2
        print(batch_name)
    
    if request.method == 'POST':
        batch = request.POST.get('batch')
        checkbox_data = request.POST.getlist('student_names') 
        desc = request.POST.get('description')
        print(batch)
        print(checkbox_data)
        print(desc)
        print('REACHED HERE')
        # Database logic
        session_report(batch_name, checkbox_data, desc)

        return redirect('choice')
    # batches = ['Batch 154','Batch 155','Batch 166','Batch 167','Batch 168','Batch 186', 'Batch 198']
    
    context = {'students': students, 'batch': batch_name}
    return render(request, 'form2.html', context)


def UserChoice(request):
    if request.user.is_authenticated:   
        profile = request.user.userprofile  # Assuming the related model field is 'userprofile'
        batch_name = profile.batch_name
        context = {'batch_name': batch_name}
        return render(request, 'userchoice.html', context)
    else:
        return redirect('login')



def ReportChoice(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser:
            return render(request, 'reportchoice.html')
        else:
            return redirect('choice')
    else:
        return redirect('login')


def DailyAudio(request):

    if request.method == 'POST':
        batch_value = request.POST.get('batch')
        # Process the batch value here (e.g., save it to the database, etc.)
        print(batch_value)
        # return HttpResponse(f'Selected batch: {batch_value}')
        students = batchwise_names(batch_value)
        sh = gc.open('AUDIO')
        print(sh.title)
        batch_sheet = sh.worksheet(batch_value)
        records = batch_sheet.get_all_records()

        market_shares = []
        print()
        print()
        print()
        for record in records:
            count = 0
            for key, value in record.items():
                if value == 'Submitted':
                    count += 1
            market_shares.append(count)
        print()
        print(students)
        print(market_shares)
        
        total = sum(market_shares)
        student_amount = len(students)
        

    # students = ['Muhammed Suhail', 'Muhammed Noushad', 'Aslah', 'Jasir', 'Devanandh', 'Jayakrishnan', 'Farsin', 'Vaisakh', 'Anil', 'Shijildas', 'Muhammed Afsal']
    # market_shares = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0]
    # # students = 

    attendance = [15, 80, 5 ]
    # attendance = {'Authorised': 15, 'Unauthorised': 80, 'Absent': 5}

    # Create the bar plot
    fig = go.Figure(data=[go.Bar(x=students, y=market_shares)])
    # fig = go.Figure(data=[go.Bar(x=names, y=attendance)])

    # Create the pie chart
    fig1 = go.Figure(data=go.Pie(labels=['Unauthorised','Authorised', 'Absent'], values=attendance))

    # Update the layout
    fig.update_layout(xaxis_title='Students', yaxis_title='Attendance', plot_bgcolor='#3A3E54', paper_bgcolor='#3A3E54', font_color='#FFFFFF', autosize=True, margin=dict(l=40, r=40, t=40, b=40), yaxis_range=[0, 30])
    fig1.update_layout(plot_bgcolor='#3A3E54', paper_bgcolor='#3A3E54', font_color='#FFFFFF', autosize=True, margin=dict(l=40, r=40, t=40, b=40), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            
    print("Starting....")

    # Convert the figure to HTML with responsive configuration
    graph_html = pio.to_html(fig, full_html=False, config={'responsive': True})
    graph_html1 = pio.to_html(fig1, full_html=False, config={'responsive': True})
    return render(request, 'dailyreport1.html',  {'graph_html': graph_html, 'graph_html1': graph_html1, 'total': total, 'batch':batch_value, 'student_amount':student_amount})


def DailySession(request):
    if request.method == 'POST':
        batch_value = request.POST.get('batch')
        print(batch_value)
        sh = gc.open('SESSION')
        worksheet = sh.worksheet('July')
        today = date.today()
        day = today.day
        print(today.day)
        report = worksheet.cell(2, day+1).value
        print(report)



    return render(request, 'dailyreport2.html', context={'batch':batch_value, 'report':report})



def BatchChoiceAudio(request):
    # batches = ['BCE154','BCE148','BCE161','BCE163','BCE173','BCE177','BCE179','BCE186']
    batches = get_batch_names_out()
    context = {'batches': batches}
    return render(request, 'batchchoiceaudio.html', context=context)



def BatchChoiceSession(request):
    batches = get_batch_names_out()
    context = {'batches': batches}
    return render(request, 'batchchoicesession.html', context=context)


def StudentDashboard(request):
    if request.user.is_authenticated:
        filler_words = ["Actually","I mean","So","See"]
        filler_count = [10,15,20,16]
        # Create the bar plot
        fig = go.Figure(data=[go.Bar(x=filler_words, y=filler_count)])
        # Update the layout
        fig.update_layout(xaxis_title='Filler Words', yaxis_title='Count', plot_bgcolor='#3A3E54', paper_bgcolor='#3A3E54', font_color='#FFFFFF', autosize=True, margin=dict(l=40, r=40, t=40, b=40), yaxis_range=[0, 30])
        # Convert the figure to HTML with responsive configuration
        graph_html = pio.to_html(fig, full_html=False, config={'responsive': True})
        return render(request, 'student_report.html',  {'graph_html': graph_html})


def IndividualReport(request):
   
    sh = gc.open('July 2024')

    profile = request.user.userprofile  # Assuming the related model field is 'userprofile'
    batch_name = profile.batch_name

    batch_sheet = sh.worksheet(batch_name)

    today = date.today()
    day = today.day
    print(today.day)

    name = request.user.username

    # database logic 

    values = batch_sheet.get_all_values()
    names = []
    for i in range(1, len(values)):
        names.append(values[i][1])
    print(names)

    students = {}
    for i in range(len(names)):
        students[names[i]] = i+2

    std_num = students[name]

    transcript = batch_sheet.cell(std_num, day+2).value

    report = generate_report(transcript)

    cnt = report.choices[0].message.content
  
    

    import json
    json_str = cnt

    json_obj = json.loads(json_str)
    # json_obj = json_str
    print(type(json_obj))

    print()
    print()
    print(json_obj)
    print()
    print()
    # Getting metrics

    context = {}

    try:
        filler_words = json_obj['filler_words']
        print('filler words no issue')
        context['filler_words'] = filler_words
    except Exception as e:
        print('filler words issue')

    try:
        filler_count = json_obj['filler_words']['total']
        print("filler_count not issue")
        context['filler_count'] = filler_count
    except Exception as e:
        print("filler_count issue")

    try:
        pauses = json_obj['pauses']
        print("pauses no issue")
        context['pauses'] = pauses
    except Exception as e:
        print("pauses issue")

    try:
        coherences = json_obj['coherences']
        print('coherences no issue')
        context['coherences'] = coherences
    except Exception as e:
        print('coherences issue')

    try:
        grammar = json_obj['grammar']
        print("grammar no issue")
        context['grammars'] = grammar
    except Exception as e:
        print("grammar issue")

    print()
    print()
    print(context)
    print()
    print()

    return render(request, 'individual_report.html', context=context)


def AudioUpload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AudioUploadForm(request.POST, request.FILES)
            if form.is_valid():
                audio_file = request.FILES['audio_file']
                # Upload the audio file to Cloud Storage using Cloud Storage API
                # (Replace with the actual upload logic)
                profile = request.user.userprofile  # Assuming the related model field is 'userprofile'
                batch_name = profile.batch_name
                context = {'batch_name': batch_name}
                upload_to_cloud_storage(audio_file)  # Placeholder function
                return redirect('studentdashboard')
                return HttpResponse('Audio uploaded successfully!')  # Redirect to success page
        else:
            form = AudioUploadForm()
            return render(request, 'audio_upload.html', {'form': form})
    
    else:
        return redirect('login')
    

    




###################################################################################################

def upload_to_cloud_storage(audio_file):
    from google.cloud import storage
    import uuid

    # Create a Cloud Storage client
    client = storage.Client()

    # Get the bucket
    # GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
    # if not GS_BUCKET_NAME:
    #     raise ValueError('GS_BUCKET_NAME environment variable is not set')
    bucket = client.bucket('communication_bucket')

    # Create a unique filename for the uploaded file
    # filename = f'{uuid.uuid4()}.{audio_file.name.split(".")[-1]}'  # Generate unique filename with extension
    # filename = f'{audio_file.name.split(".")[0]}_{uuid.uuid4().hex}.{audio_file.name.split(".")[-1]}'
    filename = f'{audio_file.name}'

    # Upload the file to the bucket
    blob = bucket.blob(filename)
    blob.upload_from_string(
        audio_file.read(),
        content_type=audio_file.content_type
    )

def audio_report(batch, checkbox_data, students):
    sh = gc.open("AUDIO")
    print(sh.title)
    print(sh.url)
    print(sh.creationTime)

    # names = {
    #     'Muhammed Suhail' : 2,
    #     'Muhammed Noushad' : 3,
    #     'Aslah' : 4,
    #     'Jasir' : 5,
    #     'Devanandh' : 6,
    #     'Jayakrishnan' : 7,
    #     'Farsin' : 8,
    #    'Vaisakh' : 9,
    #     'Anil' : 10,
    #     'Shijildas' : 11,
    #     'Muhammed Afsal' : 12
    # }

    today = date.today()
    day = today.day
    print(today.day)

    for student in checkbox_data:
        batch_sheet = sh.worksheet(batch)
        std_num = students[student]
        batch_sheet.update_cell(std_num, day+2, 'Submitted')

    # for student in students:
    #     batch_sheet = sh.worksheet(batch)
    #     std_num = names[student]
    #     if student in checkbox_data:
    #         batch_sheet.update_cell(std_num, 21, 'Present')
    #     else:
    #         batch_sheet.update_cell(std_num, 21, 'Absent')

    

def session_report(batch, checkbox_data, desc):
    sh = gc.open('SESSION')
    print(sh.title)
    print(sh.url)
    print(sh.creationTime)

    batches = {
        'BCE154':2,
        'BCE161':3,
        'BCE163':4,
        'BCE173':5,
        'BCE177':6,
        'BCE179':7,
        'BCE186':8,
        'BCE148':9
    }

    today = date.today()
    day = today.day
    print(today.day)

    batch_sheet = sh.worksheet('July')
    batch_sheet.update_cell(batches[batch], day+1, desc)

    # Session Attendance

    sh1 = gc.open('SESSION_ATTENDANCE')
    print(checkbox_data)

    students = batchwise_names(batch)
    print(students)

    for student in checkbox_data:
        batch_sheet = sh1.worksheet(batch)
        std_num = students[student]
        batch_sheet.update_cell(std_num, day+2, 'Attended')



def batchwise_names(batch):
    sh = gc.open('AUDIO')
    print(sh.title)
    print(sh.url)
    print(sh.creationTime)

    batch_sheet = sh.worksheet(batch)

    values = batch_sheet.get_all_values()
    names = []
    for i in range(1, len(values)):
        names.append(values[i][1])
    print(names)
    return names

def get_batch_names_out():
    sh = gc.open('SESSION')

    sheet = sh.worksheet('temp')

    batches = sheet.col_values(1)
    
    return batches[1:]



def generate_report(transcript):
    from openai import OpenAI
    api_key = 'sk-proj-ECQHHdwHcw2AjgRsv22OT3BlbkFJWhvVPIuU9QgCFvAcDXB7'
    client = OpenAI(
        # Defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key
    )

    template = { 
        'filler_words': {
                "mention the filler word and how many times it was repeated": 2,
                "mention the filler word and how many times it was repeated": 2,
                "total (mention the count of all filler word in the transcript)": 5
            },
        'pauses': ["mention about any specific pause from the transcript"],
        'coherences':[
                "Mention about any specific coherence from the transcript",
                "Mention about any specific coherence from the transcript",
                "Mention about any specific coherence from the transcript"
                ],
        'grammar': [
                "mention about any specific grammar mistake from the transcript and it's correction",
                "mention about any specific grammar mistake from the transcript and it's correction",
                "mention about any specific grammar mistake from the transcript and it's correction",
                "mention about any specific grammar mistake from the transcript and it's correction",
                ],
        'suggestions':[
            "suggestion_to_imporve_1",
            "suggestion_to_imporve_2",
            "suggestion_to_imporve_3",
            "suggestion_to_imporve_4",
            ]

        }

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"I will provide you a transcript of an audio. Rate it using metrics like number of filler words, long pauses, coherence, and grammar. return the report in json format like this {template}. here is the transcript {transcript}. Don't mention the word transcript in the output. Make sure the data is present in a useful structure for the reader to analyse from their report. for the grammar make sure you tell them what their mistake is and the corrected version"}
            ]
    )

    
    return chat_completion




    
