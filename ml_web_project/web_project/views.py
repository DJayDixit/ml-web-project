from django.shortcuts import render

posts = [
    {
        "author": "CoreyMs",
        "title": "Post 1",
        "content": "First Post Content",
        "date_posted": "August 3, 2018"
    }, 
    {
        "author": "Ujd",
        "title": "Post 2",
        "content": "Second Post Content",
        "date_posted": "August 3, 2018"
    }, 
]

def home(request):
    
    return render(request, 'web_project/home.html')

def about(request):
    return render(request, 'web_project/about.html')
