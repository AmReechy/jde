from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.apps import apps
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .forms import AttestationExtraForm, BasicInfoForm, DocumentsForm, ExtraDetailInfoForm, \
    IdentityDocumentsForm, PassportDocumentsForm, PersonalInfoForm, \
        UserRegisterForm, UserLoginForm, FileUploadForm
from .forms import ProcureAffidavitForm, ProcureAttestationBirthForm, ProcureAttestationNotificationForm,\
    ProcureNewspaperPublicationForm, ProcureEbirthCertificateForm, ProcureAuthenticationForm, \
        ProcureDeathCertificateForm, ProcurePoliceReportForm, ProcureStateOriginForm, \
            ProcureBachelorhoodSpinsterhoodForm, ExtraDeathInfoForm

from .models import PassportServiceRequest, ProcurementServiceRequest, ProcurementDeathServiceRequest, \
    GeneralServiceRequest, ProcureRequestUploadedFile, GeneralRequestUploadedFile, ServiceCategory, ServiceType, CustomUser, IyeWaka
import uuid, json
# Create your views here.

 
services = [
        {"title":"Translation Services", "image":"new_translation_service_img.jpg", "fee":"From €40 per page", "slug":"translation-services", "temp": "translation_temp.html", "septemp":"",
         "files_upload":"True", "payment_required":"True", "hidden_first": "true",
         "items":[
                  {"text":'Birth Certificate / Attestation of Birth'}, 
                  {"text":'Spinsterhood / Bachelorhood Certificate'}, 
                  {"text":'Marriage Certificate'}, 
                  {"text":'Divorce Certificate'}, 
                  {"text":'Adoption Certificate'}, 
                  {"text":'Police Character Certificate / Report'}, 
                  {"text":'Legal Document'}, 
                  {"text":'Court Affidavit'}, 
                  {"text":'Transcript / Diploma'}, 
                  {"text":'Driving License'},
                  {"text":"Others"}],
         "desc": "Certified translations of legal, academic, personal, and professional documents. Includes quality review and optional follow-up."},
        {"title": "Interpretation Services", "image":  "new_interpretation_service_img.jpg", "fee":"Based on request", "slug":"translation-services", "temp": "interpretation_temp.html", "septemp":"",
         "hidden_first": "true", "files_upload":"True", "payment_required":"",
          "desc":"Live interpretation, in-person, via phone or video. Ideal for meetings, legal appointments, interviews, or cross-cultural communication. Clear, accurate, and confidential.",
          "items":[{"text":"Administrative -  (Marriage, Prefecture, Association)"},
                   {"text":"Legal - (Court, CNDA, OFPRA, etc.)"}, {"text":"Others"}]},
        {"title": "Consultancy Services", "image": "new_consultation_service_img.jpg", "fee": "Based on duration", "slug":"translation-services", "temp": "consultation_temp.html", "septemp":"True",
         "hidden_first": "true", "payment_required":"True",
          "desc": "We provide business and administrative advice, available by phone or in-person at our office",
          "items": [
              {"text":"30minutes to 45minutes", "fee": "50"},
              {"text":"50minutes to 1hour 30minutes", "fee": "100"},
              {"text":"1hour 30minutes to 2hours maximum", "fee": "150"},
              ]
          },
        {"title": "Administrative Support", "image": "new_administrative_suppot_img.jpg", "fee": "Based on request", "slug":"translation-services", "temp": "admin_support_temp.html", "septemp":"", "hidden_first": "true",
          "desc": "Document handling, scheduling, form filling, and organizational support for individuals or businesses. Reliable, multilingual assistance.",
          "files_upload":"True", "payment_required":"",
          "items": [{"text":"Writing and formatting administrative letters, CVs, memos, reports etc. for applicants."},
                    {"text":"Assisting with official forms and applications filling e.g.: (French Nationality, CAF, Pole Emploi, URSSAF, Prefecture, Asylum, CNDA, OFPRA, etc…)"},
                    {"text":"Proofreading, editing and formatting of all documents"},
                    {"text":"Entering and managing data"}, 
                    {"text":"Preparing presentations and proposals for professional use"},
                    {"text":"Managing emails and correspondence"}]},

        {"title": "Procurement of Official Nigerian Documents", "image": "nigeria_national_logo.png", "fee": "Based on document type", "slug":"translation-services", "temp": "doc_procure_temp.html", "septemp":"True",
         "hidden_first": "true", "files_upload":"", "payment_required":"True",
          "desc": "We help clients obtain birth certificates, transcripts, police reports, CAC documents, and more from Nigeria — fast, legally, and securely.",
          "items":[
              {"desc":"All types of Affidavits (Correction of name(s), Correction of date of birth, etc), sworn from any court in Nigeria.", "tot_fee":100, 
               "form":ProcureAffidavitForm,
               "cost_items":[{'item': 'Affidavit', 'cost': 20}, {'item': 'Service charge', 'cost': 40}, {'item': 'Translation cost', 'cost': 40}]
               },
               {"desc":"Authentification of any official document - (Ministry of Foreign Affairs)", "tot_fee":90,
               "form":ProcureAuthenticationForm,
               "cost_items":[{'item': 'Authentification of document (Ministry of Foreign Affaires)', 'cost': 10}, {'item': 'Service charge', 'cost': 40}, {'item': 'Translation cost', 'cost': 40}]
               },
               {"desc":"Attestation of Birth letter /Certificate of Birth (NPC), (from your State of birth)", "tot_fee":130, 
               "form":ProcureAttestationBirthForm,
               "cost_items":[{'item': 'Attestation of Birth letter /Certificate of Birth (NPC)', 'cost': 40}, {'item': 'Authentification of document (Ministry of Foreign Affaires)', 'cost': 10}, 
                             {'item': 'Service charge', 'cost': 40}, {'item': 'Translation cost', 'cost': 40}]
               },
               {"desc":"Bachelorhood / Spinsterhood Certificate (from your State)", "tot_fee":130, 
               "form":ProcureBachelorhoodSpinsterhoodForm,
               "cost_items":[{'item': 'Bachelorhood/ Spinsterhood Certificate', 'cost': 40}, {'item': 'Authentification of document (Ministry of Foreign Affaires)', 'cost': 10}, 
                             {'item': 'Service charge', 'cost': 40}, {'item': 'Translation cost', 'cost': 40}]
               },
               {"desc":"Death Certificate", "tot_fee":130, 
               "form":ProcureDeathCertificateForm,
               "cost_items":[{'item': 'Death Certificate', 'cost': 40}, {'item': 'Authentification of document (Ministry of Foreign Affaires)', 'cost': 10}, 
                             {'item': 'Service charge', 'cost': 40}, {'item': 'Translation cost', 'cost': 40}]
               },
               {"desc":"Newspaper publication for any purpose from Nigeria", "tot_fee":100, 
               "form":ProcureNewspaperPublicationForm,
               "cost_items":[{'item': 'Newspaper publication', 'cost': 60}, {'item': 'Service charge', 'cost': 40}]
               },
               {"desc":"Police Character Report / Certificate", "tot_fee":225, 
               "form": ProcurePoliceReportForm,
               "cost_items":[{'item': 'Police Character Report / Certificate.', 'cost': 75}, {'item': 'Authentification of document (Ministry of Foreign Affaires)', 'cost': 10}, 
                             {'item': 'Service charge', 'cost': 100}, {'item': 'Translation cost', 'cost': 40}]
               },
               {"desc":"State of Origin / Identification Certificate.", "tot_fee":130, 
               "form":ProcureStateOriginForm,
               "cost_items":[{'item': 'State of Origin/Identification Certificate.', 'cost': 90}, {'item': 'Service charge', 'cost': 40}]
               },
               {"desc":"Attestation Notification for ADULT NIN enrollment purpose", "tot_fee":70, 
               "form":ProcureAttestationNotificationForm,
                "dhl_excluded":"True",
               "cost_items":[{'item': 'Obtaining of Certificate.', 'cost': 30}, {'item': 'Service charge', 'cost': 40}]
               },
               {"desc":"e-Birth Certificate /Birth Notification for Minor NIN enrollment purpose", "tot_fee":70, 
               "form":ProcureEbirthCertificateForm,
                "dhl_excluded":"True",
               "cost_items":[{'item': 'Obtaining of e-Birth Certificate.', 'cost': 30}, {'item': 'Service charge', 'cost': 40}]
               }
          ],
          "items2":[{"text":" All types of Affidavits  from any court in Nigeria", "fee1": "70", "fee2": "100"},
                   {"text":" Authentification of any official document - (Ministry)", "fee1": "50", "fee2": "90"},
                   {"text":" Attestation of Birth letter (NPC)/Certificate of Birth (NPC) ", "fee1": "80", "fee2": "110"},
                   {"text":"Bachelorhood Certificate.", "fee1": "80", "fee2": "110"},
                   {"text":" Spinsterhood certificate", "fee1": "70", "fee2": "110"},
                   {"text":" Death Certificate", "fee1": "100", "fee2": "130"},
                   {"text":" News paper publication for any purpose from Nigeria", "fee1": "100", "fee2": ""},
                   {"text":"Police Character Certificate", "fee1": "135", "fee2": "225", "fee2_info": "plus authentification & translation"},
                   {"text":" State of Origin/Identification Certificate", "fee1": "100", "fee2": ""},
                   {"text":" Attestation Notification for NIN enrollment purpise - (online processing alone)", "fee1": "70", "fee2": ""}]},
        {"title": "Nigerian Passport Application Support", "image":  "new_nigeria_passport_service_img.jpg", "fee": "Based on request", "slug":"translation-services", "temp": "naija_passport_temp.html", 
         "septemp":"", "files_upload":"", "payment_required":"",
          "desc": "Step-by-step guidance for online passport applications, renewals, or replacements — including profile creation and appointment booking."},
        #{"title": "Document Preparation Services", "image": "office_two_people.jpg",
        #"desc": "We assist individuals or businesses in drafting, formatting, and organizing official documents, including administrative forms, letters, report, certificates, declarations and more."},
        {"title":"Double Legalisation of Documents", "image":"new_double_legal_img.jpg", "fee": "Based on request", "slug":"translation-services", "temp": "double_legal_temp.html", "septemp":"True",
         "files_upload":"True", "payment_required":"", "hidden_first": "true",
         "desc":"Assistance with multi-stage document legalisation (e.g. Ministry of Foreign Affairs + French Embassy/ Consular legalization) for international use. We coordinate each step for compliance and recognition.",
         "items": [{"text":'Birth certificate'}, {"text":'Bacherlorhood certificate '}, {"text":'Spinsterhood '}, {"text":'Marriage certificate '}, {"text":'Others'}]},
        {"title": "Business Investment & Development Opportunities", "image": "new_image_biz_investment.jpg", "fee": "NOT PROVIDED", "slug":"translation-services", "temp": "biz_investment_temp.html", "septemp":"True",
          "desc": "We guide Nigerians in the Diaspora — especially those in France — on how to invest safely and profitably in Nigeria."},
        {"title": "Mentorship Program Master Class", "image": "new_master_class_img.jpg", "fee": "NOT PROVIDED", "slug":"translation-services", "temp": "translation_temp.html", "septemp":"",
          "desc": "Detailed description of this service category is not yet provided"}

]

ts_and_cs = [{'num': '1', 'title': ' Scope of Services', 'prepoint': 'JDE CONSULTE SAS provides:', 
              'points': ['Document Processing, Verification & Legalization in Nigeria and abroad.', 
                         'Administrative Assistance for official correspondence, records, and procedural support.', 
                         'Consultancy Services — professional advice and guidance, with appointment booking available online.',
                           'NIN Enrollment — as an accredited center, facilitating official registration in accordance with Nigerian government guidelines.', 
                           'Nigerian Passport Services — online payment of government passport fees, guidance through the application process, and document preparation.', 
                           'French Nationality File Assistance — support in assembling required documents for submission to French authorities.', 
                           'Secure Online Payments — acceptance of credit and debit card payments for service fees via approved payment gateways.', 
                           'We act as a facilitator and adviser — final decisions always rest with the relevant government or legal authority.']
            }, 
            {'num': '2', 'title': ' Client Responsibilities', 'prepoint': '', 
             'points': ['Provide complete, accurate, and authentic documents and information.', 
                        'For NIN and passport services, ensure all required preliminary steps are completed before visiting our center or requesting payment processing.', 
                        'For French nationality files, supply all required supporting documents and understand that acceptance depends on French administrative authorities.', 
                        'Attend scheduled consultancy or enrollment appointments on time; late arrivals may require rescheduling.'
                        ]
            }, 
            {'num': '3', 'title': ' Fees and Payments', 'prepoint': '', 
             'points': ['Our service fees cover facilitation, administrative support, consultancy, and enrollment assistance.', 
                        'Government, consular, legal, and other third-party fees are separate from our service charges.', 
                        'All fees must be paid in full before services commence, unless otherwise agreed in writing.', 
                        'Online card payments are processed securely via trusted payment gateways. We do not store your card details beyond what is required to complete the transaction.', 
                        'Additional costs (e.g., express handling, courier services, extra documentation) will be billed separately.'
                        ]
            }, 
            {'num': '4', 'title': ' Appointment Bookings', 'prepoint': '', 
             'points': ['Consultancy and enrollment appointments can be booked online or in person.', 
                        'Cancellations or rescheduling requests must be made at least 24 hours in advance.', 
                        'Missed appointments without notice may require a new booking and payment.'
                        ]
            }, 
            {'num': '5', 'title': ' Non-Refundable Fees', 'prepoint': '', 
             'points': ['Government, consular, and legal fees are non-refundable.', 
                        'Service fees are non-refundable once work has started, except where required by law.', 
                        'If an application or process is denied, delayed, or withdrawn, no refund will be issued for services already rendered.'
                        ]
            }, 
            {'num': '6', 'title': ' Processing Times', 'prepoint': '', 
             'points': ['No guaranteed completion times are offered — all timelines depend on the relevant authorities.', 
                        'Delays caused by government systems, public holidays, strikes, or incomplete submissions are beyond our control.', 
                        'Time estimates are for guidance only.'
                        ]
            }, 
            {'num': '7', 'title': ' Limitation of Liability', 'prepoint': '', 
             'points': ['We are not responsible for final decisions by government, consular, or legal authorities.', 
                        'We are not liable for technical failures of government systems, payment platforms, or third-party services.', 
                        'For consultancy, our liability is limited to the amount paid for the specific service.', 
                        'For NIN, passport, or nationality services, our role is purely facilitative.'
                        ]
            }, 
            {'num': '8', 'title': ' Confidentiality & Data Protection', 'prepoint': '', 
             'points': ['All client data is treated with strict confidentiality.', 
                        'For NIN enrollment, passport, and nationality services, sensitive personal data is handled in compliance with applicable data protection laws.', 
                        'We only share your information with third parties as required to complete your service or as mandated by law.'
                        ]
            }, 
            {'num': '9', 'title': ' Force Majeure', 'prepoint': 'We are not liable for delays or non-performance caused by events beyond our reasonable control, including natural disasters, strikes, system outages, political unrest, or similar disruptions.', 
             'points': []
            }, 
            {'num': '10', 'title': ' Consultancy Disclaimer', 'prepoint': '', 
             'points': ['Advice is given in good faith, based on the information available at the time.',
                        'Implementation of recommendations and final decisions remain the client’s responsibility.'
                        ]
            }, 
            {'num': '11', 'title': ' Amendments to Terms', 'prepoint': 'We may update these Terms and Conditions at any time. Updates will be posted on our website and take effect immediately for new services.', 
             'points': []
            }, 
            {'num': '12', 'title': ' Dispute Resolution & Governing Law', 'prepoint': '', 
             'points': ['We aim to resolve disputes amicably.', 
                        'If unresolved, disputes will be handled by the competent courts in France.', 
                        'These Terms are governed by French law.']
            }
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
                "partner_afjumbo.jpg", "partner_cpss_training.jpg", "partner_knowledge.png","new_partner_gtco_logo_square.png",
                "new_partner_idee_paris_logo_squared.png", "new_partner_societe_gen_logo2.png"]
    context = {"services":services, "partners":partners, "current_page":"home"}
    return render(request, "homepage.html",context)


def doc_procure_select_page(request, service_cat):
    service = {}
    for s in services:
        if 'procurement' in s["title"].lower():
            service = s
            break

    return render(request, "doc_procure_select.html", {"service":service}) 


def doc_procure_form_page2(request, service_cat, doc_type_index):

    service = {}
    for s in services:
        if 'procurement' in s["title"].lower():
            service = s
            break
    if service:
        selected_doc_type = service["items"][doc_type_index]["desc"]
        form = service["items"][doc_type_index]["form"]
        #extra_death_info_form = ExtraDeathInfoForm()
        dhl_included = "dhl_excluded" not in service["items"][doc_type_index].keys()
        service_total_fee = service["items"][doc_type_index]["tot_fee"] 
        service_dhl_total = (service_total_fee + 120) if dhl_included else service_total_fee
    context = {
            "service":service,
            "dhl_included": dhl_included,
            "procure_form": form(),
            "extra_death_info_form": ExtraDeathInfoForm(),
            "selected_doc_type": selected_doc_type,
            "service_total_fee": service_total_fee,
            "service_dhl_total": service_dhl_total,
            "selected_doc_type_index": doc_type_index
            }

    return render(request, "doc_procure_form.html", context) 


def validate_file_size(uploaded_file):
    """Check file size based on type (image vs other)."""
    max_size_image = 5 * 1024 * 1024   # 5MB
    max_size_other = 3 * 1024 * 1024   # 3MB

    content_type = uploaded_file.content_type
    if content_type.startswith("image/"):  # Images
        if uploaded_file.size > max_size_image:
            raise ValidationError(f"Image file {uploaded_file.name} exceeds 5MB limit.")
    else:  # Non-images
        if uploaded_file.size > max_size_other:
            raise ValidationError(f"File {uploaded_file.name} exceeds 3MB limit.")


def doc_procure_form_page(request, service_cat, doc_type_index):
    service = {}
    current_page = "services"
    for s in services:
        if 'procurement' in s["title"].lower():
            service = s
            break
    if service:
        selected_doc_type = service["items"][doc_type_index]["desc"]
        selected_type_exits = ServiceType.objects.filter(description=selected_doc_type).exists()
        if selected_type_exits:
            selected_type_object = ServiceType.objects.filter(description=selected_doc_type).first()
        else:selected_type_object = ServiceType.objects.none()
        selected_service_cat_object = ServiceCategory.objects.get(title=service['title'])
        form = service["items"][doc_type_index]["form"]()
        #extra_death_info_form = ExtraDeathInfoForm()
        dhl_included = "dhl_excluded" not in service["items"][doc_type_index].keys()
        service_total_fee = service["items"][doc_type_index]["tot_fee"] 
        service_dhl_total = (service_total_fee + 120) if dhl_included else service_total_fee
        death_extra_form = ExtraDeathInfoForm()

    if request.method == "POST":
        reference_id = str(uuid.uuid4()).replace("-", "")[:12]
        payment_required = bool(request.POST.get("payment-required", False))
        computed_payment = request.POST.get("computed-service-fee", '0')
        computed_payment = int(computed_payment.strip(" €"))
        if request.user.is_authenticated:
            user = request.user
        else:
            user = CustomUser.objects.none().first()
        context = {
                    "service":service,
                    "service_cat": service_cat,
                    "selected_service_type": selected_doc_type,
                    "total_payment":computed_payment
                }
        if "death" in selected_doc_type.lower():
            #model = ProcurementDeathServiceRequest
            form = service["items"][doc_type_index]["form"](request.POST, request.FILES)
            death_extra_form = ExtraDeathInfoForm(request.POST, request.FILES)
            if form.is_valid() and death_extra_form.is_valid():
                service_request = ProcurementDeathServiceRequest.objects.create(
                    user=user,
                    service_type=selected_type_object,
                    service_category=selected_service_cat_object,
                    reference_id=reference_id,
                    computed_service_fee=computed_payment,
                    initial_payment_required = payment_required,
                    **form.cleaned_data,
                    **death_extra_form.cleaned_data
                )
                death_cert = request.FILES.get("death_certificate")
                if death_cert:
                    service_request.death_certificate = death_cert
                    service_request.save(update_fields=["death_certificate"])
                messages.success(request, "Service request form submitted successfully!")
                request.session["request_service_model"] = "ProcurementDeathServiceRequest"
                return redirect("base:service-payment", service_cat=service_cat, reference_id=reference_id)
                #return render(request, "service_payment.html", context) 
            else:
                messages.error(request, "Please correct the errors in the form.")
        
        else:
            model = ProcurementServiceRequest
            form = service["items"][doc_type_index]["form"](request.POST, request.FILES)
            if form.is_valid():
                service_request = ProcurementServiceRequest.objects.create(
                    user=user,
                    reference_id=reference_id,
                    service_type=selected_type_object,
                    service_category=selected_service_cat_object,
                    computed_service_fee=computed_payment,
                    initial_payment_required = payment_required,
                    **form.cleaned_data
                )

                # Handle dynamically uploaded files
                extra_files = request.FILES.getlist("file")
                for f in extra_files:
                    try:
                        validate_file_size(f)  # Check file size
                        ProcureRequestUploadedFile.objects.create(procurement_request=service_request, file=f)
                    except ValidationError as e:
                        messages.error(request, str(e))
                        service_request.delete()  # Rollback if invalid file
                        #return redirect("base:doc-procure-form-page")
                        break
                else:
                    messages.success(request, "Service request form submitted successfully!")
                    request.session["request_service_model"] = "ProcurementServiceRequest"
                    
                    return redirect("base:service-payment", service_cat=service_cat, reference_id=reference_id)
                    #return render(request, "service_payment.html", context) 
            else:
                messages.error(request, "Please correct the errors in the form.")
    
    context = {
            "service":service,
            "dhl_included": dhl_included,
            "procure_form": form,
            "extra_death_info_form": death_extra_form,
            "selected_doc_type": selected_doc_type,
            "service_total_fee": service_total_fee,
            "service_dhl_total": service_dhl_total,
            "selected_doc_type_index": doc_type_index
            }
    #print(death_extra_form.as_p())

    return render(request, "doc_procure_form.html", context) 

def service_payment(request, service_cat, reference_id):
    service_request_model_string = request.session["request_service_model"]
    service_request_model = apps.get_model("base", service_request_model_string)
    service_request = service_request_model.objects.get(reference_id=reference_id)
    return render(request, "service_payment.html", {"service_request":service_request}) 


def submission_success(request, service_cat, reference_id):
    service_request_model_string = request.session["request_service_model"]
    service_request_model = apps.get_model("base", service_request_model_string)
    service_request = service_request_model.objects.get(reference_id=reference_id)
    return render(request, "request_submission_success.html", {"service_request":service_request})


def general_service_request_page(request, service_cat, service_type_index=-1):
    if 'procurement' in service_cat:
        return redirect("base:doc-procure-select", service_cat=service_cat)

    current_page = "services"
    service_info = ''
    info_form = PersonalInfoForm()
    basic_info_form = BasicInfoForm()
    #documents_form = DocumentsForm()
    #identity_doc_form = IdentityDocumentsForm()
    passport_doc_form = PassportDocumentsForm()
    #attest_extra_form = AttestationExtraForm()
    extra_form = ExtraDetailInfoForm()
    file_upload_form = FileUploadForm()
    for service in services:
        if slugify(service['title']) == service_cat:
            service_info = service
            break
    if not service_info:
        return redirect("base:homepage")
    
    #if service_cat == "translation-services":
    fee_text = service_info["fee"].strip()
    """payment_required = "€" in fee_text
    fee = fee_text[fee_text.index('€')+1:fee_text.index(" ", fee_text.index("€"))] if payment_required else "€0"
    service_info["payment_required"] = payment_required
    service_info["fee_amount"] = fee
    """
    service_info["current_page"] = "services"
    service_info["service_cat"] = service_cat
    service_info["fee_text"] = fee_text
    context = {"service": service_info, 
               "current_page":current_page,
               "long_info_form":info_form,
               "passport_doc_form":passport_doc_form,
               "extra_info_form":extra_form,
               "file_form":file_upload_form,
               "basic_info_form":basic_info_form}

    return render(request, "service_detail.html", context)
    
    #else:
        #return HttpResponse(f"""Hello there!
                            #\rThe detailed page for {service_cat} is not available yet.
                            #\rBye!""")

def general_service_form_page(request, service_cat):
    if 'procurement' in service_cat:
        return redirect("base:doc-procure-select", service_cat=service_cat)
    service = {}
    current_page = "services"
    for s in services:
        if slugify(s['title']) == service_cat:
            service = s
            break
    if service:
        
        #form = service["items"][doc_type_index]["form"]()
        #extra_death_info_form = ExtraDeathInfoForm()
        #dhl_included = "dhl_excluded" not in service["items"][doc_type_index].keys()
        #service_total_fee = service["items"][doc_type_index]["tot_fee"] 
        #service_dhl_total = (service_total_fee + 120) if dhl_included else service_total_fee
        #death_extra_form = ExtraDeathInfoForm()

        info_form = PersonalInfoForm()
        basic_info_form = BasicInfoForm()
        passport_doc_form = PassportDocumentsForm()
        extra_form = ExtraDetailInfoForm()
        file_upload_form = FileUploadForm()

        service["current_page"] = "services"
        service["service_cat"] = service_cat

    if request.method == "POST":
        selected_service_index = int(request.POST.get("selected-service-index", 1000))
        try:
            selected_doc_type = service["items"][selected_service_index]["text"]
        except:
            selected_doc_type = ''
        selected_type_exits = ServiceType.objects.filter(description=selected_doc_type).exists()
        if selected_type_exits:
            selected_type_object = ServiceType.objects.filter(description=selected_doc_type).first()
        else:selected_type_object = ServiceType.objects.none().first()
        selected_service_cat_object = ServiceCategory.objects.filter(title=service['title']).first()

        reference_id = str(uuid.uuid4()).replace("-", "")[:12]
        payment_required = bool(request.POST.get("payment-required", False))
        try:
            computed_payment = request.POST.get("total-payment", '')
            computed_payment = int(computed_payment.strip(" €"))
        except:
            computed_payment = 0

        if request.user.is_authenticated:
            user = request.user
        else:
            user = CustomUser.objects.none().first()
        
        if "passport" in service_cat:
            #model = ProcurementDeathServiceRequest
            info_form = PersonalInfoForm(request.POST, request.FILES)
            passport_doc_form = PassportDocumentsForm(request.POST, request.FILES)
            if info_form.is_valid() and passport_doc_form.is_valid():
                service_request = PassportServiceRequest.objects.create(
                    user=user,
                    service_type=selected_type_object,
                    service_category=selected_service_cat_object,
                    reference_id=reference_id,
                    computed_service_fee=computed_payment,
                    initial_payment_required = payment_required,
                    **info_form.cleaned_data,
                    **passport_doc_form.cleaned_data
                )

                messages.success(request, "Service request form submitted successfully!")
                request.session["request_service_model"] = "PassportServiceRequest"
                if payment_required:
                    return redirect("base:service-payment", service_cat=service_cat, reference_id=reference_id)
                else:
                    return redirect("base:submission-success", service_cat=service_cat, reference_id=reference_id)

                #return render(request, "service_payment.html", context) 
            else:
                messages.error(request, "Please correct the errors in the form.")
        
        else:
            basic_info_form = BasicInfoForm(request.POST)
            extra_form = ExtraDetailInfoForm(request.POST)
            #file_upload_form = FileUploadForm()
            if basic_info_form.is_valid() and extra_form.is_valid():
                service_request = GeneralServiceRequest.objects.create(
                    user=user,
                    reference_id=reference_id,
                    service_type=selected_type_object,
                    service_category=selected_service_cat_object,
                    computed_service_fee=computed_payment,
                    initial_payment_required = payment_required,
                    **basic_info_form.cleaned_data,
                    **extra_form.cleaned_data
                )

                # Handle dynamically uploaded files
                extra_files = request.FILES.getlist("file")
                for f in extra_files:
                    try:
                        validate_file_size(f)  # Check file size
                        GeneralRequestUploadedFile.objects.create(service_request=service_request, file=f)
                    except ValidationError as e:
                        messages.error(request, str(e))
                        service_request.delete()  # Rollback if invalid file
                        #return redirect("base:doc-procure-form-page")
                        break
                else:
                    messages.success(request, "Service request form submitted successfully!")
                    request.session["request_service_model"] = "GeneralServiceRequest"
                    if payment_required:
                        return redirect("base:service-payment", service_cat=service_cat, reference_id=reference_id)
                    else:
                        return redirect("base:submission-success", service_cat=service_cat, reference_id=reference_id)
                    #return render(request, "service_payment.html", context) 
            else:
                if not basic_info_form.is_valid():
                    print("Basic info not valid" *10)
                if not extra_form.is_valid():
                    print("Extra form not valid" *10)
                messages.error(request, "Please correct the errors in the form.")
    
    context = {"service": service, 
               "current_page":current_page,
               "long_info_form":info_form,
               "passport_doc_form":passport_doc_form,
               "extra_info_form":extra_form,
               "file_form":file_upload_form,
               "basic_info_form":basic_info_form}

    return render(request, "service_detail.html", context)


def iye_waka(request):
    current_page = "iye-waka"
    videos = IyeWaka.objects.filter(show=True)
    return render(request, "iye_waka.html", {"current_page":current_page, "videos":videos})


def about_jde(request):
    current_page = "about"
    return render(request, "about.html", {"current_page":current_page})


def all_services(request):
    current_page = "services"
    return render(request, "all_services.html", {"current_page":current_page, "services":services})

def contact_us(request):
    current_page = "contact-us"
    return render(request, "contact_us.html", {"current_page":current_page})

def auth_view(request):
    action = "login"
    current_page = "login-register"
    if request.method == "POST":
        if "register" in request.POST:
            action = "register"
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
            next_url = request.GET.get("next", "")
            action = "login"
            login_form = UserLoginForm(request, data=request.POST)
            reg_form = UserRegisterForm()
            

            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                if next_url:
                    return redirect(next_url)
                return redirect("base:homepage")  # change to dashboard/homepage
            else:
                messages.error(request, "Invalid login credentials.")
    else:
        reg_form = UserRegisterForm()
        login_form = UserLoginForm()

    return render(request, "auth.html", 
                  {"reg_form": reg_form, 
                   "login_form": login_form,
                   "action":action, 
                   "current_page":current_page})


def user_logout(request):
    logout(request)
    messages.error(request, "You have logged out of your Account!")
    return redirect('base:homepage')

def terms(request):
    return render(request, "terms_and_conditions.html", {"terms_n_conditions":ts_and_cs})
