
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "base"

urlpatterns = [
        #path("old", views.home, name="home"),
        #path("new", views.new_home, name="new-home"),
        path("", views.homepage, name="homepage"),
        path("jde-consulte", views.homepage, name="homepage"),
        path("iye-waka", views.iye_waka, name="iye-waka"),
        path("service/<str:service_cat>", views.general_service_form_page, name="service-page"),
        path("service/<str:service_cat>/doc-type-selection", views.doc_procure_select_page, name="doc-procure-select"),
        path("service/<str:service_cat>/doc-<int:doc_type_index>", views.doc_procure_form_page, name="doc-procure-form-page"),
        path("service/<str:service_cat>/form-success-and-payment/<str:reference_id>", views.service_payment, name="service-payment"),
        path("service/<str:service_cat>/form-success/<str:reference_id>", views.service_payment, name="service-form-success"),
        path("account/auth/", views.auth_view, name="auth"),
        path("account/logout/", views.user_logout, name="logout"),
        path("about/", views.about_jde, name="about-jde"),
        path("services/", views.all_services, name="all-services"),
        path("contact-us/", views.contact_us, name="contact-us"),
        path("terms-and-conditions/", views.terms, name="terms"),
        #path("submit-procure-form/<str:service_cat>/doc-<int:doc_type_index>", views.process_procurement_request_submission, name="procure-form-submit"),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
 
