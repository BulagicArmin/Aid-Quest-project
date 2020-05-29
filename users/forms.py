from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Donator
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'staff', 'admin', 'autentifikacija')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserRegistrerForm(UserCreationForm):
    email = forms.EmailField()
    staff = forms.BooleanField(label="Humanitarna organizacija", required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'staff']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):

    img = forms.ImageField(label="Logo organizacije")
    naziv = forms.CharField(label="Naziv organizacije")
    predstavnik = forms.CharField(label="Ovlašteni predstavnik")
    skr_naziv = forms.CharField(label="Skraćeni naziv")
    reg_ured = forms.CharField(label="Registracioni ured")
    sjediste = forms.CharField(label="Sjedište")
    tel_num = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                               label="Broj telefona", required=False)


    class Meta:
        model = Profile
        fields = ['img','naziv', 'predstavnik', 'skr_naziv', 'reg_ured', 'sjediste', 'tel_num']

class DonatorUpdateForm(forms.ModelForm):
    tel_num = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                       label= "Broj telefona", required=False)
    img = forms.ImageField(label = "Profilna slika")
    full_name = forms.CharField(label="Ime i prezime")
    birth_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ), label="Datum rođenja"
    )


    class Meta:
        model = Donator
        fields = ['img','full_name', 'birth_date', 'adress', 'tel_num']
