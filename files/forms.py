from hashlib import md5
import os

from django import forms

from .models import File


class FileForm(forms.ModelForm):
    md5 = forms.CharField(required=False)
    size = forms.CharField(required=False)

    class Meta:
        model = File
        fields = ('md5', 'file', 'size')

    def clean(self):
        cd = super().clean()

        if self._errors:
            return cd

        if not self.instance.id:
            cd['md5'] = md5(cd['file'].read(4096)).hexdigest()
            cd['file_name'] = cd['file']._name
            cd['size'] = cd['file']._size
            _, ext = os.path.splitext(cd['file']._name)
            cd['file']._name = '{}{}'.format(cd['md5'], ext)

        return cd


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    is_register = forms.BooleanField(required=False, widget=forms.HiddenInput)


class UploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)
