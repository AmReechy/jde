import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "postal_address", "password"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Type your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Type your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Input valid email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Input correct phone number'}),
            'postal_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Type correct address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))


class PersonalInfoForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""

    """class Meta:
        fields = ["surname", "first_name", "middle_name", "sex", "date_of_birth", "martial_status",
                  "occupation", "emial", "phone_number", "postal_address", "current_residential_address",
                  "state_of_origin", "lga_of_origin", "village_town_origin", "place_of_birth",
                  "lga_place_of_birth", "father_name", "mother_name", "mother_maiden_name"]
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'middle_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'postal_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'current_residential_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'state_of_origin': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'lga_of_origin': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
        }"""


class BasicInfoForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        required=False,
        choices=[('', "-----"), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter a valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter an active phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter a correct postal address'}),
    )

    """class Meta:
        fields = ["surname", "first_name", "middle_name", "sex", 
                  "emial", "phone_number", "postal_address"]
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'middle_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'sex': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
            'postal_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}),
        }"""


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

"""class ImageForm(forms.ModelForm):
    photo = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Image
        fields = ['photo', ]
"""

class DocumentsForm(forms.Form):
    documents = MultipleFileField(
        label="Upload All Relevant Documents",
        #widget=forms.FileInput(attrs={'multiple': True}),
        required=False
    )

    def clean_documents(self):
        files = self.files.getlist('documents')
        if len(files) > 10:
            raise forms.ValidationError("You can upload at most 10 files.")
        return files


class FileUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload File",
        widget=forms.ClearableFileInput(attrs={'class': 'file-input'})
    )


class IdentityDocumentsForm(forms.Form):
    birth_certificate = forms.FileField(
        label="Birth Certificate",
        required=True
    )
    passport_data_page = forms.FileField(
        label="Passport Data Page",
        required=True
    )
    passport_photo_identity = forms.FileField(
        label="Passport Photo Identity",
        required=True
    )


class PassportDocumentsForm(forms.Form):
    birth_certificate = forms.FileField(
        label="Birth Certificate",
        required=True
    )
    passport_data_page = forms.FileField(
        label="Passport Data Page",
        required=True
    )
    certificate_of_state_of_origin = forms.FileField(
        label="Certificate of State of Origin (if applicable)",
        required=False
    )
    nin_slip = forms.FileField(
        label="NIN Slip (if applicable)",
        required=False
    )
    passport_size_photo = forms.FileField(
        label="Passport Size Photograph (if applicable)",
        required=False
    )


class AttestationExtraForm(forms.Form):
    highest_education = forms.CharField(
        label="Highest Education Qualification", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What\' your highest education'}),
    )
    id_passport_num = forms.CharField(
        label="ID Passport Number", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your passport ID number'}),
    )
    nin = forms.CharField(
        label="NIN", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your NIN digits'}),
    )


"""class DetailInfoForm(forms.Form):
    detail_info = forms.Textarea(
        label="Please provide further details, explanation, or some relevant information that might be useful to us to know",
        required=False,
        widget=forms.Textarea(attrs={})
    )
"""

class ExtraDetailInfoForm(forms.Form):
    extra_detail_info = forms.CharField(
        label="Additional Information / Reason",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": 'form-input',
                "rows": 6,
                #"style": "width:100%;",   # makes it take full width
                "placeholder": "Please provide further details, reason for the service request, or some relevant information that you think might be useful to us to know here ..."
            }
        )
    )


class ExtraDeathInfoForm(forms.Form):
    date_of_death = forms.DateField(
        label="Date of Death",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    age_at_death = forms.IntegerField(
        label="Age of the Deceased",
        min_value=0,   # Minimum allowed value
        max_value=150,   # Maximum allowed value
        widget=forms.NumberInput(attrs={
            "class": "form-input",
            "placeholder": "0 - 150"
        })
    )
    place_of_death = forms.CharField(
        label="Place of Death", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'place of death'}),
    )
    deceased_address = forms.CharField(
        label="Full Residential Address of the Deceased", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Deceased full address'}),
    )
    name_of_declarant = forms.CharField(
        label="Full Name of Declarant", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name of declarant'}),
    )
    death_certificate = forms.FileField(
        label="Medical Death Certificate (if any)",
        required=False
    )


class ProcureAffidavitForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
        required=False
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""
    reason_for_request = forms.CharField(
        label="Reason for the Affidavit",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": 'form-input',
                "rows": 6,
                #"style": "width:100%;",   # makes it take full width
                "placeholder": "Kindly provide a brief explanation for why you are requesting for the affidavit ..."
            }
        )
    )


class ProcureAuthenticationForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False,
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""


class ProcureAttestationBirthForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False,
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""


class ProcureBachelorhoodSpinsterhoodForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False,
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""


class ProcureDeathCertificateForm(forms.Form):
    surname = forms.CharField(
        label="Surname of the Deceased", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name of the Deceased", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name of the Deceased", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False
    )
    
    sex = forms.ChoiceField(
        label="Sex of the Deceased",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth of the Deceased",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    email = forms.CharField(
        label="Email Address of Declarant",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number of Declarant", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address of Declarant", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    """state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )"""


class ProcureNewspaperPublicationForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False,
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""


class ProcurePoliceReportForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False,
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    reason_for_request = forms.CharField(
        label="Reason for the Police Report",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": 'form-input',
                "rows": 6,
                #"style": "width:100%;",   # makes it take full width
                "placeholder": "Kindly provide a brief explanation for why you are requesting for the police report ..."
            }
        )
    )


class ProcureStateOriginForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""


class ProcureAttestationNotificationForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    nin = forms.CharField(
        label="NIN (if any)", max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter NIN if you have it '}),
    )


class ProcureEbirthCertificateForm(forms.Form):
    surname = forms.CharField(
        label="Surname", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Surname or last name'}),
    )
    first_name = forms.CharField(
        label="First Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        label="Middle Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Middle name'}),
        required=False
    )
    
    sex = forms.ChoiceField(
        label="Sex ",
        choices=[('', '----'), ('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Gender'})  # can also use forms.Select if you prefer dropdown
    )
    
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    
    marital_status = forms.ChoiceField(
        label="Marital Status",
        choices=[('', '----'), ('single', 'Single'), ('married', 'Married'), ('widowed', "Widowed"), ("divorced", "Divorced"), ("separated", "Separated")],
        widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'marital status'})
    )
    occupation = forms.CharField(
        label="Occupation", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your job or occupation'}),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Valid email'}),
    )
    phone_number = forms.CharField(
        label="Phone Number", max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
    )
    postal_address = forms.CharField(
        label="Postal Address", max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your postal address'}),
    )
    state_of_origin = forms.CharField(
        label="State Of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What state are you from'}),
    )
    lga_of_origin = forms.CharField(
        label="LG Area Of Origin ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is your local government area'}),
    )
    village_town_origin = forms.CharField(
        label="Village or Town of Origin", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What or town are you from'}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Where were you born ?'}),
    )
    lga_place_of_birth = forms.CharField(
        label="LG Area (for Place of Birth)", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'LGA of where you were born'}),
    )
    father_name = forms.CharField(
        label="Father's Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your father\'s name'}),
    )
    mother_name = forms.CharField(
        label="Mother's Name ", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name'}),
    )
    """mother_maiden_name = forms.CharField(
        label="Mother's Maiden Name", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your mother\'s name before she married'}),
    )"""
    parent_nin = forms.CharField(
        label="NIN of Parent (if any)", max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter NIN of parent if available'}),
    )

