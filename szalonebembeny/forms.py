import django.forms as forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from szalonebembeny.models import Category


class ProductAddForm(forms.Form):
    name = forms.CharField(label='Nazwa produktu', max_length=64)
    description = forms.CharField(label='Opis', widget=forms.Textarea)
    category = forms.ModelChoiceField(label='Kategoria', queryset=Category.objects.all())
    price = forms.DecimalField(label='Cena', max_digits=8, decimal_places=2, min_value=0)
    stock = forms.IntegerField(label='Ilość na stanie', min_value=0)

    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


def validate_username_is_not_taken(value):
    if User.objects.filter(username=value):
        raise ValidationError("Ten login jest już zajęty")


class RegisterForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=50, validators=[validate_username_is_not_taken])
    pass1 = forms.CharField(label='Hasło', max_length=100, widget=forms.PasswordInput)
    pass2 = forms.CharField(label='Powtórz hasło', max_length=100, widget=forms.PasswordInput)
    first_name = forms.CharField(label='Imię', max_length=50)
    last_name = forms.CharField(label='Nazwisko', max_length=50)
    email = forms.EmailField(label='Adres e-mail')
    phone_number = forms.CharField(label='Numer telefonu', max_length=9)
    address = forms.CharField(label='Adres', max_length=128)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['pass1'] != cleaned_data['pass2']:
            raise ValidationError('Hasła muszą być takie same')
        return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ResetPasswordForm(forms.Form):
    pass1 = forms.CharField(label='Nowe hasło', max_length=100, widget=forms.PasswordInput)
    pass2 = forms.CharField(label='Powtórz hasło', max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['pass1'] != cleaned_data['pass2']:
            raise ValidationError('Hasła muszą być takie same')
        return cleaned_data


class CommentAddForm(forms.Form):
    content = forms.CharField(label='Treść komentarza', widget=forms.Textarea)
    score = forms.DecimalField(label='Ocena', max_digits=3, decimal_places=1, max_value=10, min_value=0)

    def __init__(self, *args, **kwargs):
        super(CommentAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(label='Imię', max_length=50)
    last_name = forms.CharField(label='Nazwisko', max_length=50)
    email = forms.EmailField(label='Adres e-mail')
    phone_number = forms.CharField(label='Numer telefonu', max_length=9)
    address = forms.CharField(label='Adres', max_length=128)

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
