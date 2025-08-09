from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html")

def new_home(request):
    return render(request, "new_index.html")

def homepage(request):
    services = ["Translation Services", "Interpretation Services", "Consultation Services",
                "Administrative Support", "Procurration of Documents", "Nigerian Passport Application Support (Online Processing)", 
                "Document Preparation Services", "Financial Advice", "Business Investment & Development Opportunities", "Mentorship Program Master Class"]
    context = {"services":services}
    return render(request, "homepage.html",context)
