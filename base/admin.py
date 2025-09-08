from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    ServiceCategory,
    ServiceType,
    ProcurementServiceRequest,
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# ==============================
# Custom User Admin
# ==============================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "phone_number", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "postal_address")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "phone_number", "password1", "password2"),
            },
        ),
    )

# ==============================
# Service Type Admin
# ==============================
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("description", "service_category", "fee")
    search_fields = ("description",)
    list_filter = ("service_category",)


class ServiceTypeInline(admin.TabularInline):  # or StackedInline if you prefer
    model = ServiceType
    extra = 1  # how many empty forms to display by default
    show_change_link = True  # allow clicking to open ServiceType page

    
# ==============================
# Service Category Admin
# ==============================
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "fee", "require_file_uploads", "require_payment")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("require_file_uploads", "require_payment")
    inlines = [ServiceTypeInline]  # 👈 this makes ServiceTypes editable under ServiceCategory


# ==============================
# Procurement Service Request Admin
# ==============================
"""@admin.register(ProcurementServiceRequest)
class ProcurementServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "surname",
        "first_name",
        "service_type",
        "service_category",
        "payment_status",
        "submitted_at",
    )
    list_filter = ("payment_status", "service_category", "service_type", "submitted_at")
    search_fields = (
        "reference_id",
        "surname",
        "first_name",
        "middle_name",
        "email",
        "phone_number",
    )
    readonly_fields = ("submitted_at",)

    fieldsets = (
        ("Request Info", {"fields": ("reference_id", "service_type", "service_category", "payment_status")}),
        ("Personal Info", {
            "fields": (
                "surname", "first_name", "middle_name", "sex", "date_of_birth", "marital_status",
                "occupation", "email", "phone_number", "postal_address", "current_residential_address",
                "state_of_origin", "lga_of_origin", "village_town_origin",
                "place_of_birth", "lga_place_of_birth",
                "father_name", "mother_name", "mother_maiden_name",
            )
        }),
        ("Attestation / Extra", {
            "fields": (
                "highest_education", "id_passport_num", "nin", "parent_nin",
            )
        }),
        ("Service Fee", {
            "fields": (
                "initial_payment_required", "computed_service_fee", "finalized_service_fee",
            )
        }),
        ("Timestamps", {"fields": ("submitted_at",)}),
    )
"""

# Define a resource for the model
class ProcurementServiceRequestResource(resources.ModelResource):
    class Meta:
        model = ProcurementServiceRequest
        fields = (
            "id",
            "reference_id",
            "surname",
            "first_name",
            "email",
            "phone_number",
            "service_type__description",
            "service_category__title",
            "payment_status",
            "submitted_at",
        )
        export_order = fields  # keep order in exported file


# Use ImportExportModelAdmin instead of normal ModelAdmin
@admin.register(ProcurementServiceRequest)
class ProcurementServiceRequestAdmin(ImportExportModelAdmin):
    resource_class = ProcurementServiceRequestResource
    list_display = (
        "reference_id",
        "surname",
        "first_name",
        "service_type",
        "service_category",
        "payment_status",
        "submitted_at",
    )
    list_filter = ("payment_status", "service_category", "service_type", "submitted_at")
    search_fields = ("reference_id", "surname", "first_name", "email", "phone_number")
    readonly_fields = ("submitted_at",)
    fieldsets = (
        ("Request Info", {"fields": ("reference_id", "service_type", "service_category", "payment_status")}),
        ("Personal Info", {
            "fields": (
                "surname", "first_name", "middle_name", "sex", "date_of_birth", "marital_status",
                "occupation", "email", "phone_number", "postal_address", "current_residential_address",
                "state_of_origin", "lga_of_origin", "village_town_origin",
                "place_of_birth", "lga_place_of_birth",
                "father_name", "mother_name", "mother_maiden_name",
            )
        }),
        ("Attestation / Extra", {
            "fields": (
                "highest_education", "id_passport_num", "nin", "parent_nin",
            )
        }),
        ("Service Fee", {
            "fields": (
                "initial_payment_required", "computed_service_fee", "finalized_service_fee",
            )
        }),
        ("Timestamps", {"fields": ("submitted_at",)}),
    )
