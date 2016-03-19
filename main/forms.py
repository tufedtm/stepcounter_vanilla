# coding:utf8
from django import forms


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя', 'required': True}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'required': True}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Город', 'required': True}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Возраст', 'required': True}))
    # photo = forms.ImageField()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 3:
            raise forms.ValidationError(u'Слишком короткое Имя - не меньше 3 символов')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 3:
            raise forms.ValidationError(u'Слишком короткая Фамилия - не меньше 3 символов')
        return last_name

    def clean_city(self):
        city = self.cleaned_data['city']
        if len(city) < 3:
            raise forms.ValidationError(u'Слишком короткое название города - не меньше 3 символов')
        return city

    def clean_age(self):
        age = self.cleaned_data['age']
        if age > 150:
            raise forms.ValidationError(u'Ошибка - не больше 150')
        return age