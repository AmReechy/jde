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
        #{"title":"Translation Services", "image":"translation_image.jpg"},
        {"title": "Interpretation Services", "image":  "headphone.jpg",
          "desc":"Live in-person interpretation during your meetings, interviews, calls and administrative appointments, available in English, French and Igbo languages"},
        {"title": "Consultancy Services", "image": "office_consultancy.jpg",
          "desc": "We provide business and administrative advice, available by phone or in-person at our office"},
        {"title": "Administrative Support", "image": "france_landscape.jpg",
          "desc": "We offer hands-on administrative support tohelp individuals and businesses stay organized,efficient,and compliant. This service is ideal for those who need help managing documents, tasks, or operations across borders or languages."},
        {"title": "Procurement of Documents", "image": "beautiful_nature1.png",
          "desc": "We assist clients in obtaining various kinds of official documents from Nigeria. We ensure the process is handled with discretion and accuracy, in a legal and professional manner."},
        {"title": "Nigerian Passport Application Support (Online Processing)", "image":  "partner_federal_gov_nigeria.jpg",
          "desc": "We assist clients in filling, paying,  taking appointment and submitting online application for Nigerian passports. Wether it’s your first passport, renewal or lost passport replacement, we guide you through the official process step-by-step"},
        {"title": "Document Preparation Services", "image": "office_two_people.jpg",
          "desc": "We assist individuals or businesses in drafting, formatting, and organizing official documents, including administrative forms, letters, report, certificates, declarations and more."},
        {"title": "Business Investment & Development Opportunities", "image": "business.jpg",
          "desc": "Detailed description of this service category is not yet provided"},
        {"title": "Mentorship Program Master Class", "image": "masterclass.jpg",
          "desc": "Detailed description of this service category is not yet provided"}

    ]
    partners = ["partner_ambassade_de_france.jpg", "partner_consulat_france.jpg", "partner_federal_gov_nigeria.jpg",
                "nimc_square_image.jpg", "partner_ministry_foreign_logo.png", "partner_immigration_squared_logo.png", "partner_dawari_consult.jpg",
                "partner_afjumbo.jpg", "partner_cpss_training.jpg"]
    context = {"services":services, "partners":partners}
    return render(request, "homepage.html",context)
