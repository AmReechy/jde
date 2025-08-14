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
        {"title": "Interpretation Services", "image":  "headphone.jpg", "fee":"Based on request",
          "desc":"Live interpretation via phone or video. Ideal for meetings, legal appointments, interviews, or cross-cultural communication. Clear, accurate, and confidential."},
        {"title": "Consultancy Services", "image": "office_consultancy.jpg", "fee": "Based on duration",
          "desc": "We provide business and administrative advice, available by phone or in-person at our office"},
        {"title": "Administrative Support", "image": "france_landscape.jpg", "fee": "€70 per 60minutes duration",
          "desc": "Document handling, scheduling, form filling, and organizational support for individuals or businesses. Reliable, multilingual assistance."},

        {"title": "Procurement of Official Nigerian Documents", "image": "beautiful_nature1.png", "fee": "Based on document type",
          "desc": "We help clients obtain birth certificates, transcripts, police reports, CAC documents, and more from Nigeria — fast, legally, and securely."},
        {"title": "Nigerian Passport Application Support", "image":  "partner_federal_gov_nigeria.jpg", "fee": "Based on request",
          "desc": "Step-by-step guidance for online passport applications, renewals, or replacements — including profile creation and appointment booking."},
        #{"title": "Document Preparation Services", "image": "office_two_people.jpg",
        #"desc": "We assist individuals or businesses in drafting, formatting, and organizing official documents, including administrative forms, letters, report, certificates, declarations and more."},
        {"title":"Double Legalisation of Documents", "image":"office_consultancy.jpg", "fee": "Based on request",
         "desc":"Assistance with multi-stage document legalisation (e.g. Ministry of Foreign Affairs + French Embassy/ Consular legalization) for international use. We coordinate each step for compliance and recognition."},
        {"title": "Business Investment & Development Opportunities", "image": "business.jpg", "fee": "NOT PROVIDED",
          "desc": "Detailed description of this service category is not yet provided"},
        {"title": "Mentorship Program Master Class", "image": "masterclass.jpg", "fee": "NOT PROVIDED",
          "desc": "Detailed description of this service category is not yet provided"}

    ]
    partners = ["partner_ambassade_de_france.jpg", "partner_consulat_france.jpg", "partner_federal_gov_nigeria.jpg",
                "nimc_square_image.jpg", "partner_ministry_foreign_logo.png", "partner_immigration_squared_logo.png", "partner_dawari_consult.jpg",
                "partner_afjumbo.jpg", "partner_cpss_training.jpg"]
    context = {"services":services, "partners":partners, "current_page":"home"}
    return render(request, "homepage.html",context)

def service_page(request, service_category):
    if service_category == "translation-services":
        return render(request, "service_detail.html", {"current_page":"services"})
