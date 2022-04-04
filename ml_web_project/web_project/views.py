from re import search
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DetailForm, ContactForm
import ml_project.views as calculate_output
from django.contrib.auth.decorators import login_required
from ml_web_project.settings import SESSION_COOKIE_AGE
from web_project.models import Calculations
from . import cookies

@login_required
def home(request):

    context = {"pred": 0, "session_time_out": SESSION_COOKIE_AGE, "last_searches": cookies.RECENT_SEARCHES}

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
            
            # TODO: setting relative path instead of absoulte
            core_cpi_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\core_cpi_predict.pickle"
            year_gni_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\year_gni_predict.pickle"
            price_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\price_predict.pickle" 

            values = Calculations.objects.filter(year=year, month=month, area=area, flat_type=flat_type)
 
            # TODO: querying the database to get the prediction if it exists in the database.
            if len(values) != 0:
                values[0].search_frequency += 1
                values[0].save()
                context['pred'] = format(values[0].prediction, ".2f")

            else:
                price = calculate_output.HousePrice()
                pred = price.calculate(f_date, flat_type, area, core_cpi_file, year_gni_file, price_file)

                prediction = format(pred[0], ".2f")

                context["pred"] = prediction

                calc = Calculations(year=year, month = month, area=area, flat_type =flat_type, prediction= pred)
                calc.save()
            
            search_history_empty = False

            if not search_history_empty:
                curr_value: int
                next_value: int
                for index in range(len(context["last_searches"])):
                    searches = context["last_searches"]

                    if index == 0:
                        curr_value = searches[index]
                        searches[index] = context["pred"]
                        next_value = searches[index+1]
                    
                    else:
                        searches[index]= curr_value
                        curr_value = next_value
                        if index != len(searches)-1:
                            next_value = searches[index+1]

    else:
        form = DetailForm()

    context['form'] = form
    # return render(request, 'web_project/home.html', {'form': form}, context)
    return render(request, 'web_project/home.html', context)

def about(request):
    return render(request, 'web_project/about.html')

def contact(request):
    c_form = ContactForm()
    context = {"form": c_form}
    if request.method == 'POST':
        if c_form.is_valid():
            messages.success(request, f'Data Submitted Succesfully')
    return render(request, 'web_project/contact.html', context)


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