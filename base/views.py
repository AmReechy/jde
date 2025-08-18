from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify

# Create your views here.


services = [
        {"title":"Translation Services", "image":"new_translation_service_img.jpg", "fee":"From €40 per page", "slug":"translation-services",
         "desc": "Certified translations of legal, academic, personal, and professional documents. Includes quality review and optional follow-up."},
        {"title": "Interpretation Services", "image":  "new_interpretation_service_img.jpg", "fee":"Based on request", "slug":"translation-services",
          "desc":"Live interpretation, in-person, via phone or video. Ideal for meetings, legal appointments, interviews, or cross-cultural communication. Clear, accurate, and confidential."},
        {"title": "Consultancy Services", "image": "new_consultation_service_img.jpg", "fee": "Based on duration", "slug":"translation-services",
          "desc": "We provide business and administrative advice, available by phone or in-person at our office"},
        {"title": "Administrative Support", "image": "new_administrative_suppot_img.jpg", "fee": "€70 per 60minutes duration", "slug":"translation-services",
          "desc": "Document handling, scheduling, form filling, and organizational support for individuals or businesses. Reliable, multilingual assistance."},

        {"title": "Procurement of Official Nigerian Documents", "image": "new_document_procurement_from_naija.jpg", "fee": "Based on document type", "slug":"translation-services",
          "desc": "We help clients obtain birth certificates, transcripts, police reports, CAC documents, and more from Nigeria — fast, legally, and securely."},
        {"title": "Nigerian Passport Application Support", "image":  "new_nigeria_passport_service_img.jpg", "fee": "Based on request", "slug":"translation-services",
          "desc": "Step-by-step guidance for online passport applications, renewals, or replacements — including profile creation and appointment booking."},
        #{"title": "Document Preparation Services", "image": "office_two_people.jpg",
        #"desc": "We assist individuals or businesses in drafting, formatting, and organizing official documents, including administrative forms, letters, report, certificates, declarations and more."},
        {"title":"Double Legalisation of Documents", "image":"new_double_legal_img.jpg", "fee": "Based on request", "slug":"translation-services",
         "desc":"Assistance with multi-stage document legalisation (e.g. Ministry of Foreign Affairs + French Embassy/ Consular legalization) for international use. We coordinate each step for compliance and recognition."},
        {"title": "Business Investment & Development Opportunities", "image": "new_image_biz_investment.jpg", "fee": "NOT PROVIDED", "slug":"translation-services",
          "desc": "Detailed description of this service category is not yet provided"},
        {"title": "Mentorship Program Master Class", "image": "new_master_class_img.jpg", "fee": "NOT PROVIDED", "slug":"translation-services",
          "desc": "Detailed description of this service category is not yet provided"}

]


def home(request):
    return render(request, "index.html")

def new_home(request):
    return render(request, "new_index.html")
 
def homepage(request):
    # services = ["Translation Services", "Interpretation Services", "Consultation Services",
    #             "Administrative Support", "Procurration of Documents", "Nigerian Passport Application Support (Online Processing)", 
    #             "Document Preparation Services", "Business Investment & Development Opportunities", 
    #             "Mentorship Program Master Class"]
    
    
    partners = ["partner_ambassade_de_france.jpg", "partner_consulat_france.jpg", "partner_federal_gov_nigeria.jpg",
                "nimc_square_image.jpg", "partner_ministry_foreign_logo.png", "partner_immigration_squared_logo.png", "partner_dawari_consult.jpg",
                "partner_afjumbo.jpg", "partner_cpss_training.jpg", "new_partner_gtco_logo_square.png",
                "new_partner_idee_paris_logo_squared.png", "new_partner_societe_gen_logo2.png"]
    context = {"services":services, "partners":partners, "current_page":"home"}
    return render(request, "homepage.html",context)

def service_page(request, service_cat):
    service_info = ''
    for service in services:
        if slugify(service['title']) == service_cat:
            service_info = service
            break
    if not service_info:
        return redirect("base:homepage")
    
    if service_cat == "translation-services":
        service_info["current_page"] = "services"
        context = {"service": service_info}
        return render(request, "service_detail.html", context)
    
    else:
        return HttpResponse(f"""Hello there!
                            \rThe detailed page for {service_cat} is not available yet.
                            \rBye!""")

def iye_waka(request):
    return render(request, "iye_waka.html")