from django.forms import Form, ModelForm, DateTimeField, IntegerField
from django.forms.widgets import TextInput, DateTimeInput, HiddenInput
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import widgets
from . import models


class RoomForm(ModelForm):
    end_date = gift_date = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = models.Room
        fields = ('name', 'description', 'end_date', 'gift_date', 'is_public')
        labels = {
            'name': _('Nome'),
            'description': _('Descrizione'),
            'end_date': _('Data estrazione'),
            'gift_date': _('Data scambio'),
            'is_public': _('Stanza pubblica'),
        }


class RoomMemberForm(Form):
    room_id = IntegerField(widget=HiddenInput())
    user_id = IntegerField(widget=HiddenInput())

    class Meta:
        fields = ('room_id', 'user_id')
