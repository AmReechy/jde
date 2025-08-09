from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html")

def new_home(request):
    return render(request, "new_index.html")

def homepage(request):
    # services = ["Translation Services", "Interpretation Services", "Consultation Services",
    #             "Administrative Support", "Procurration of Documents", "Nigerian Passport Application Support (Online Processing)", 
    #             "Document Preparation Services", "Business Investment & Development Opportunities", 
    #             "Mentorship Program Master Class"]
    
    services = [
        {"title":"Translation Services", "image":"translation_image.jpg"},
        {"title": "Interpretation Services", "image":  "headphone.jpg"},
        {"title": "Consultancy Services", "image": "office_consultancy.jpg" },
        {"title": "Administrative Support", "image": "france_landscape.jpg" },
        {"title": "Procurration of Documents", "image": "beautiful_nature1.png" },
        {"title": "Nigerian Passport Application Support (Online Processing)", "image":  "office_administrative"},
        {"title": "Document Preparation Services", "image": "office_two_people.jpg" },
        {"title": "Business Investment & Development Opportunities", "image": "business.jpg" },
        {"title": "Mentorship Program Master Class", "image": "masterclass.jpg" }

    ]
    context = {"services":services}
    return render(request, "homepage.html",context)
