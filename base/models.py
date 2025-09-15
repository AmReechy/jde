from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
from django.utils.text import slugify



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=False)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name","phone_number"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


from django.db import models

class UserApplication(models.Model):
    # Personal Info
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=200)
    current_residential_address = models.CharField(max_length=200)
    state_of_origin = models.CharField(max_length=100)
    lga_of_origin = models.CharField(max_length=100)
    village_town_origin = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=100)
    lga_place_of_birth = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_maiden_name = models.CharField(max_length=100)

    # Identity Documents
    birth_certificate = models.FileField(upload_to="documents/")
    passport_data_page = models.FileField(upload_to="documents/")
    passport_photo_identity = models.FileField(upload_to="documents/")

    # Attestation / Extra
    highest_education = models.CharField(max_length=100)
    id_passport_num = models.CharField(max_length=100)
    nin = models.CharField(max_length=100)
    parent_nin = models.CharField(max_length=100)


    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.surname} {self.first_name}"


class UploadedFile(models.Model):
    """For handling dynamically uploaded extra files."""
    application = models.ForeignKey(UserApplication, on_delete=models.CASCADE, related_name="extra_files")
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return f"File for {self.application} - {self.file.name}"



class ServiceCategory(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    fee = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(upload_to="documents/", null=True, blank=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    temp = models.CharField(max_length=100, blank=True, null=True)
    has_sep_temp = models.BooleanField(default=False)
    require_file_uploads = models.BooleanField(default=False)
    require_payment = models.BooleanField(default=False)
    form_hidden_first = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not already set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class ServiceType(models.Model):
    description = models.CharField(max_length=250)
    service_category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    fee = models.IntegerField(null=True, blank=True)


    def __str__(self):
            return f"{self.description}"
        

# require separate : procure Death, Other procure, Passport, OtherServices
class ProcurementServiceRequest(models.Model):
    """
    Model for procurement service requests"""
    # Personal Info
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    #service_type = models.ForeignKey(ServiceType, null=True, blank=True, on_delete=models.SET_NULL)
    service_options = models.ManyToManyField(ServiceType)
    service_category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    reference_id = models.CharField(max_length=50, unique=True)
    payment_status = models.BooleanField(default=False)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=200)
    #current_residential_address = models.CharField(max_length=200)
    state_of_origin = models.CharField(max_length=100)
    lga_of_origin = models.CharField(max_length=100)
    village_town_origin = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=100)
    lga_place_of_birth = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    #mother_maiden_name = models.CharField(max_length=100)

    # Attestation / Extra
    highest_education = models.CharField(max_length=100)
    id_passport_num = models.CharField(max_length=100)
    nin = models.CharField(max_length=100)
    parent_nin = models.CharField(max_length=100)

    # Service Fee
    initial_payment_required = models.BooleanField(default=False)
    computed_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    finalized_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    reason_for_request = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_category.title} | requested by - {self.surname} {self.first_name} | reference_id = {self.reference_id}"


class ProcureRequestUploadedFile(models.Model):
    """For handling dynamically uploaded extra files for procurement service requests."""
    procurement_request = models.ForeignKey(ProcurementServiceRequest, on_delete=models.CASCADE, related_name="extra_files")
    file = models.FileField(upload_to="procurement_request_uploads/")

    def __str__(self):
        return f"File for {self.procurement_request.service_category.title} | reference_id = {self.service_request.reference_id} | {self.file.name}"
    

class GeneralServiceRequest(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    #service_type = models.ForeignKey(ServiceType, null=True, blank=True, on_delete=models.SET_NULL)
    service_options = models.ManyToManyField(ServiceType)
    service_category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    reference_id = models.CharField(max_length=50, unique=True)
    payment_status = models.BooleanField(default=False)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=200)

    # Service Fee
    initial_payment_required = models.BooleanField(default=False)
    computed_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    finalized_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    # Extra Detail Info
    extra_detail_info = models.TextField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_category.title} | requested by - {self.surname} {self.first_name} | reference_id = {self.reference_id}"



class GeneralRequestUploadedFile(models.Model):
    """For handling dynamically uploaded extra files for general service requests."""
    service_request = models.ForeignKey(GeneralServiceRequest, on_delete=models.CASCADE, related_name="extra_files")
    file = models.FileField(upload_to="general_request_uploads/")

    def __str__(self):
        return f"File for {self.service_request.service_category.title} | reference_id = {self.service_request.reference_id} | {self.file.name}"
    

class ProcurementDeathServiceRequest(models.Model):
    """
    Model for procurement death certificate service requests"""
    # Personal Info
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    #service_type = models.ForeignKey(ServiceType, null=True, blank=True, on_delete=models.SET_NULL)
    service_options = models.ManyToManyField(ServiceType)
    service_category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    reference_id = models.CharField(max_length=50, unique=True)
    payment_status = models.BooleanField(default=False)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = models.DateField()

    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=200)
    #current_residential_address = models.CharField(max_length=200)
    #state_of_origin = models.CharField(max_length=100)
    #lga_of_origin = models.CharField(max_length=100)
    #village_town_origin = models.CharField(max_length=100)
    #place_of_birth = models.CharField(max_length=100)
    #lga_place_of_birth = models.CharField(max_length=100)
    #father_name = models.CharField(max_length=100)
    #mother_name = models.CharField(max_length=100)
    #mother_maiden_name = models.CharField(max_length=100)

    # Death Request / Extra
    date_of_death = models.DateField()
    age_at_death = models.IntegerField()
    place_of_death = models.CharField(max_length=100)
    deceased_address = models.CharField(max_length=100)
    name_of_declarant = models.CharField(max_length=100)
    #parent_nin = models.CharField(max_length=100)
    death_certificate = models.FileField(upload_to="procure_death_request_files/")

    # Service Fee
    initial_payment_required = models.BooleanField(default=False)
    computed_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    finalized_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Death Certificte Request by - {self.surname} {self.first_name}  | reference_id = {self.reference_id}"
    

class PassportServiceRequest(models.Model):
    # Personal Info
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    #service_type = models.ForeignKey(ServiceType, null=True, blank=True, on_delete=models.SET_NULL)
    service_options = models.ManyToManyField(ServiceType)
    service_category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    reference_id = models.CharField(max_length=50, unique=True)
    payment_status = models.BooleanField(default=False)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=200)
    #current_residential_address = models.CharField(max_length=200)
    state_of_origin = models.CharField(max_length=100)
    lga_of_origin = models.CharField(max_length=100)
    village_town_origin = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=100)
    lga_place_of_birth = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    #mother_maiden_name = models.CharField(max_length=100)

    # Passport Extra Files
    birth_certificate = models.FileField(upload_to="passport_request_files/")
    passport_data_page = models.FileField(upload_to="passport_request_files/")
    certificate_of_state_of_origin = models.FileField(upload_to="passport_request_files/")
    nin_slip = models.FileField(upload_to="passport_request_files/")
    passport_size_photo = models.FileField(upload_to="passport_request_files/")

    # Service Fee
    initial_payment_required = models.BooleanField(default=False)
    computed_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    finalized_service_fee = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    submitted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Passport Certificte Request by - {self.surname} {self.first_name} | reference_id = {self.reference_id}"


class IyeWaka(models.Model):
    title = models.CharField(max_length=250, blank="True", null="True")
    detail_description = models.TextField()
    url = models.CharField(max_length=250)
    position = models.IntegerField(default=100)
    show = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["position", "-added_at"]


class SocialLink(models.Model):
    facebook = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    tiktok = models.URLField(max_length=500, blank=True, null=True)
    x = models.URLField(max_length=500, blank=True, null=True)

