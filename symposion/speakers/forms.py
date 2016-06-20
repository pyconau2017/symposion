from __future__ import unicode_literals
from django import forms

from symposion.speakers.models import Speaker


class SpeakerForm(forms.ModelForm):

    class Meta:
        model = Speaker
        fields = [
            "name",
            "biography",
            "experience",
            "photo",
            "telephone",
            "homepage",
            "twitter_username",
            "accessibility",
            "travel_assistance",
            "accommodation_assistance",
            "agreement",
        ]

    def __init__(self, *a, **k):
        super(SpeakerForm, self).__init__(*a, **k)
        self.fields['agreement'].required = True

    def clean_twitter_username(self):
        value = self.cleaned_data["twitter_username"]
        if value.startswith("@"):
            value = value[1:]
        return value
