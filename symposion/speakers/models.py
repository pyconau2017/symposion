from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from symposion.markdown_parser import parse


@python_2_unicode_compatible
class Speaker(models.Model):

    SESSION_COUNT_CHOICES = [
        (1, "One"),
        (2, "Two")
    ]

    user = models.OneToOneField(User, null=True, related_name="speaker_profile", verbose_name=_("User"))
    name = models.CharField(verbose_name=_("Name"), max_length=100,
                            help_text=_("As you would like it to appear in the"
                                        " conference programme."))
    biography = models.TextField(
        blank=True,
        help_text=_("This will appear on the conference website and in the "
                    "programme.  Please write in the third person, eg 'Alice "
                    "is a Moblin hacker...', 150-200 words. Edit using "
                    "<a href='http://warpedvisions.org/projects/"
                    "markdown-cheat-sheet/' target='_blank'>"
                    "Markdown</a>."),
        verbose_name=_("Biography"),
    )
    biography_html = models.TextField(blank=True)
    experience = models.TextField(
        blank=True,
        help_text=_("Have you had any experience presenting elsewhere? If so, "
                    "we'd like to know. Anything you put here will only be "
                    "seen by the organisers and reviewers; use it to convince "
                    "them why they should accept your proposal. Edit using "
                    "<a href='http://warpedvisions.org/projects/"
                    "markdown-cheat-sheet/' target='_blank'>"
                    "Markdown</a>."),
        verbose_name=_("Speaking experience"),
    )
    experience_html = models.TextField(blank=True)
    photo = models.ImageField(upload_to="speaker_photos", blank=True, verbose_name=_("Photo"))
    telephone = models.CharField(
        max_length=15,
        help_text=_(u"The conference team will need this to contact you "
                    "during the conference week. If you don't have one, or do "
                    "not wish to provide it, then enter NONE in this field.")
    )
    homepage = models.URLField(
        blank=True,
        help_text=_(u"Your home page, if you have one")
    )
    twitter_username = models.CharField(
        max_length=15,
        blank=True,
        help_text=_(u"Your Twitter account")
    )
    accessibility = models.TextField(
        blank=True,
        help_text=_("Please describe any special accessibility requirements "
        "that you may have. Edit using "
        "<a href='http://warpedvisions.org/projects/"
        "markdown-cheat-sheet/' target='_blank'>Markdown</a>."),
        verbose_name=_("Accessibility requirements"))
    accessibility_html = models.TextField(blank=True)
    travel_assistance = models.BooleanField(
        blank=True,
        default=False,
        help_text=_("Check this box if you require assistance to travel to to the conference to "
                    "present your proposed sessions."),
        verbose_name=_("Travel assistance required"),
    )
    accommodation_assistance = models.BooleanField(
        blank=True,
        default=False,
        help_text=_("Check this box if you require us to provide you with student-style "
                    "accommodation in order to present your proposed sessions."),
        verbose_name=_("Accommodation assistance required"),
    )
    agreement = models.BooleanField(
        default=False,
        help_text=_("I agree to the terms and conditions of attendance, and "
                    "I have read, understood, and agree to act according to "
                    "the standards set forth in our Code of Conduct ")
    )

    annotation = models.TextField(verbose_name=_("Annotation"))  # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True, verbose_name=_("Invite_email"))
    invite_token = models.CharField(max_length=40, db_index=True, verbose_name=_("Invite token"))
    created = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
        verbose_name=_("Created")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")
        permissions = (('can_view_contact_details', 'Can View Contact Details'),)

    def save(self, *args, **kwargs):
        self.biography_html = parse(self.biography)
        self.experience_html = parse(self.experience)
        self.accessibility_html = parse(self.accessibility)
        return super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return self.name
        else:
            return "?"

    def get_absolute_url(self):
        return reverse("speaker_edit")

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email

    @property
    def all_presentations(self):
        presentations = []
        if self.presentations:
            for p in self.presentations.all():
                presentations.append(p)
            for p in self.copresentations.all():
                presentations.append(p)
        return presentations
