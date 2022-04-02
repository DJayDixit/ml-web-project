from django.shortcuts import render
from django.contrib import messages
from .forms import DetailForm
import ml_project.views as calculate_output
from django.contrib.auth.decorators import login_required
# posts = [
#     {
#         "author": "CoreyMs",
#         "title": "Post 1",
#         "content": "First Post Content",
#         "date_posted": "August 3, 2018"
#     }, 
#     {
#         "author": "Ujd",
#         "title": "Post 2",
#         "content": "Second Post Content",
#         "date_posted": "August 3, 2018"
#     }, 
# ]

# def home(request):
#     context = {
#         "posts": posts
#     }
#     return render(request, 'web_project/home.html', context)

@login_required
def home(request):

    context = {"pred": 0}

    if request.method == 'POST':
        form = DetailForm(request.POST)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            area = form.cleaned_data.get('area_sqm')
            f_type = form.cleaned_data.get('f_type')

            str_date = year+"."+month
            f_date = float(str_date)

            flat_type = int(f_type)

            messages.success(request, f'Data Submitted Succesfully')
            
            core_cpi_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\core_cpi_predict.pickle"
            year_gni_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\year_gni_predict.pickle"
            price_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\price_predict.pickle" 

            price = calculate_output.HousePrice()
            pred = price.calculate(f_date, flat_type, area, core_cpi_file, year_gni_file, price_file)

            context["pred"] = pred[0]
            
            

    else:
        form = DetailForm()

    context['form'] = form
    # return render(request, 'web_project/home.html', {'form': form}, context)
    return render(request, 'web_project/home.html', context)

def about(request):
    return render(request, 'web_project/about.html')
