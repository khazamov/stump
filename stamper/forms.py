from django import forms
from pyuploadcare.dj.forms import ImageField


class ImgForm(forms.Form):
    picImg =  ImageField()
