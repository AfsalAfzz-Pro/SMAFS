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



credential_path = 'sam_sir_project/app1/credentials.json'
# credentials, project = google.auth.default()
# credentials = service_account.Credentials.from_service_account_file(
#     credential_json)
scopes = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
gc = gspread.service_account(filename='C:/Users/Hp/Documents/Organized Folders/Automation & APIs/Sam Sir Automation Web/Management_Project/app1/credentials.json', scopes=scopes)


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
             # Create a new user with password hashing
            user = User.objects.create_user(username=uname, password=pass1)
            
            # Create a UserProfile instance
            profile = UserProfile.objects.create(user=user, batch_name=batch_name)

            # new_user.save()
            return redirect('login')

            # Redirect to a page indicating that an OTP has been sent
            # return redirect('generate_otp')

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
            return HttpResponse('Invalid credentials')

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
    return render(request, 'dailyreport2.html')


def BatchChoice(request):
    
    
    batches = ['BCE154','BCE148','BCE161','BCE163','BCE173','BCE177','BCE179','BCE186']
    context = {'batches': batches}
    return render(request, 'batchchoice.html', context=context)


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
    filler_words = {
        "actually": 1,
        "i_mean": 1,
        "so": 3,
        "see": 3,
        "total": 8
      }
    
    filler_count = 0
    for word in filler_words:
        filler_count += filler_words[word]

    pauses = {
        "pause_1": "after 'Mother's Day'",
        "pause_2": "before 'I will say about the video'",
        "total": 2
      }
    
    pause_count = 0
    for pause in pauses:
        pause_count += 1
    
    coherences =  [
          "The speaker seems to struggle to maintain a coherent flow, jumping between thoughts.",
          "Repetition of ideas without clear transitions.",
          "The message about not needing a specific day to celebrate mothers is clear, but it could be more succinct."
        ]

    grammars = [
          "'It is basically a YouTube video that talk about Mother's Day.' should be 'talks about Mother's Day.'",
          "'I will say about the video.' should be 'I will talk about the video.'",
          "'She expressed that how, what she wants to become in the future and she explains, I mean, she represents so many professions but at last she wants to be like her mother.' is awkward and could be clearer.",
          "'She loves to be her mother.' should be 'She loves to be like her mother.'",
          "'See, every person has her, has her first role more or less, her' is incomplete and confusing.",
          "'We doesn't need any specific day' should be 'We don't need any specific day.'",
          "'We should love her, we should care her all the day.' should be 'We should love her, we should care for her every day.'",
          "'That was special to us in our life too.' is unclear and could be 'She has been special to us in our life too.'"
        ]
    
    suggestions =  [
      "Organize thoughts before speaking to ensure a logical flow.",
      "Reduce filler words by practicing the speech multiple times.",
      "Review grammar rules or consider writing out the speech to identify and correct errors.",
      "Focus on delivering a clear and concise message, avoiding unnecessary repetition."
    ]

    context = {'filler_words': filler_words, 'filler_count': filler_count, 'pauses': pauses, 'coherences': coherences, 'grammars': grammars, 'suggestions': suggestions}

    return render(request, 'individual_report.html', context=context)


# def AudioUpload(request):
#     if request.method == 'POST':
#         audio_file = request.FILES.get('audio_file')
        
#         # Check if a file was uploaded
#         # if not audio_file:
#         #     return JsonResponse({'error': 'No audio file uploaded'}, status=400)
        
#         print(audio_file)

#         # Return information about the uploaded file
#         return JsonResponse({
#         'filename': audio_file.name,
#         'size': audio_file.size,
#         'content_type': audio_file.content_type,
#         })
#     else:
#         # Handle other HTTP methods (optional)
#         return render(request, 'audio_upload.html')




###################################################################################################


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

    batch_sheet = sh.worksheet('June')
    batch_sheet.update_cell(batches[batch], day+1, desc)


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

