from django import forms

from module.models import User
# from django.contrib.auth.models import User


class AddRepoData(forms.Form):
    owner = forms.CharField(max_length=100, label='Введите имя владельца (логин в Gitlab)')
    repo = forms.CharField(max_length=100, label='Введите название репозитория')


class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput,
                                help_text="Повторите пароль", min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'middle_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='')