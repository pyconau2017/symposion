from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from account.decorators import login_required

from symposion.proposals.models import ProposalBase
from symposion.speakers.forms import SpeakerForm
from symposion.speakers.models import Speaker

from symposion.reviews.models import NotificationTemplate
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

@login_required
def speaker_create(request):
    try:
        return redirect(request.user.speaker_profile)
    except ObjectDoesNotExist:
        pass

    if request.method == "POST":
        try:
            speaker = Speaker.objects.get(invite_email=request.user.email)
            found = True
        except Speaker.DoesNotExist:
            speaker = None
            found = False
        form = SpeakerForm(request.POST, request.FILES, instance=speaker)

        if form.is_valid():
            speaker = form.save(commit=False)
            speaker.user = request.user
            if not found:
                speaker.invite_email = None
            speaker.save()
            messages.success(request, _("Speaker profile created."))
            return redirect("dashboard")
    else:
        form = SpeakerForm(initial={"name": request.user.get_full_name()})
    return render(request, "symposion/speakers/speaker_create.html", {
        "speaker_form": form,
    })


@login_required
def speaker_create_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    if not request.user.is_staff:
        raise Http404

    try:
        return redirect(user.speaker_profile)
    except ObjectDoesNotExist:
        pass

    if request.method == "POST":
        form = SpeakerForm(request.POST, request.FILES)

        if form.is_valid():
            speaker = form.save(commit=False)
            speaker.user = user
            speaker.save()
            messages.success(request, _("Speaker profile created."))
            return redirect("user_list")
    else:
        form = SpeakerForm(initial={"name": user.get_full_name()})

    return render(request, "symposion/speakers/speaker_create.html", {
        "speaker_form": form,
    })


def speaker_create_token(request, token):
    speaker = get_object_or_404(Speaker, invite_token=token)
    request.session["pending-token"] = token
    if request.user.is_authenticated():
        # check for speaker profile
        try:
            existing_speaker = request.user.speaker_profile
        except ObjectDoesNotExist:
            pass
        else:
            del request.session["pending-token"]
            additional_speakers = ProposalBase.additional_speakers.through
            additional_speakers._default_manager.filter(
                speaker=speaker
            ).update(
                speaker=existing_speaker
            )
            messages.info(request, _("You have been associated with all pending "
                                     "talk proposals"))
            return redirect("dashboard")
    else:
        if not request.user.is_authenticated():
            return redirect("account_login")
    return redirect("speaker_create")


@login_required
def speaker_edit(request, pk=None):
    if pk is None:
        try:
            speaker = request.user.speaker_profile
        except Speaker.DoesNotExist:
            return redirect("speaker_create")
    else:
        if request.user.is_staff:
            speaker = get_object_or_404(Speaker, pk=pk)
        else:
            raise Http404()

    if request.method == "POST":
        form = SpeakerForm(request.POST, request.FILES, instance=speaker)
        if form.is_valid():
            form.save()
            messages.success(request, "Speaker profile updated.")
            return redirect("dashboard")
    else:
        form = SpeakerForm(instance=speaker)

    return render(request, "symposion/speakers/speaker_edit.html", {
        "speaker_form": form,
    })


def speaker_profile(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    presentations = speaker.all_presentations
    if not presentations and not request.user.is_staff:
        raise Http404()

    return render(request, "symposion/speakers/speaker_profile.html", {
        "speaker": speaker,
        "presentations": presentations,
    })



@login_required
def speaker_communique(request, pk=None):
    """
    This puts up a page that lets an admin / staff person compose and send an email
    to all speakers.  During CFP period, this will go out to all who have submitted
    proposals.
    """
    if not request.user.is_staff:
        raise Http404

    # Sending a message already composed?
    if request.method == "POST":

        if settings.DEBUG:
            recipients = [ '"%s" <%s>"' % (sp.name, sp.user.email) for sp in Speaker.objects.filter(user__is_staff=True).all()]
        else:
            recipients = [ '"%s" <%s>"' % (sp.name, sp.user.email) for sp in Speaker.objects.all()]

        recipients = filter(lambda x: x is not None and x.user is not None, recipients)
        if recipients:
            em = EmailMessage(from_email=settings.DEFAULT_FROM_EMAIL,
                          to=[settings.DEFAULT_FROM_EMAIL],
                          bcc=recipients,
                          subject=request.POST['msg_title'],
                          body=request.POST['msg_body'])

            em.send()
        return redirect("dashboard")

    ctx = dict()
    return render(request, "symposion/speakers/communique.html", ctx)



