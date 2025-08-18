from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, UserLoginForm

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
    
    #if service_cat == "translation-services":
    fee_text = service_info["fee"].strip()
    payment_required = "€" in fee_text
    fee = fee_text[fee_text.index('€')+1:fee_text.index(" ", fee_text.index("€"))] if payment_required else "€0"
    service_info["current_page"] = "services"
    service_info["service_cat"] = service_cat
    service_info["payment_required"] = payment_required
    service_info["fee_amount"] = fee
    service_info["fee_text"] = fee_text
    context = {"service": service_info}
    return render(request, "service_detail.html", context)
    
    #else:
        #return HttpResponse(f"""Hello there!
                            #\rThe detailed page for {service_cat} is not available yet.
                            #\rBye!""")

def iye_waka(request):
    return render(request, "iye_waka.html")




def auth_view(request):
    if request.method == "POST":
        if "register" in request.POST:
            reg_form = UserRegisterForm(request.POST)
            login_form = UserLoginForm()

            if reg_form.is_valid():
                user = reg_form.save(commit=False)
                user.set_password(reg_form.cleaned_data["password"])
                user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("base:auth")  # same page
            else:
                messages.error(request, "Please correct the errors below.")

        elif "login" in request.POST:
            login_form = UserLoginForm(request, data=request.POST)
            reg_form = UserRegisterForm()

            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect("base:homepage")  # change to dashboard/homepage
            else:
                messages.error(request, "Invalid login credentials.")
    else:
        reg_form = UserRegisterForm()
        login_form = UserLoginForm()

    return render(request, "auth.html", {"reg_form": reg_form, "login_form": login_form})

