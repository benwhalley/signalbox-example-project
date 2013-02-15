"""Admin setup for Questionnaire app"""

from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import Permission
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from ask.models import AskPage, QuestionAsset, QuestionInAskPage, Instrument, Choice, ShowIf, Asker, Question, ChoiceSet, QuestionInInstrument
import ask.models.fields

from utilities.linkedinline import LinkedInline

from ask.lookups import QuestionLookup
import selectable.forms as selectable


class ShowIfForm(forms.ModelForm):
    previous_question = selectable.AutoCompleteSelectField(lookup_class=QuestionLookup,
        required=False)

    def clean(self, *args, **kwargs):
        """Check that all the values entered are valid for the question's choiceset."""

        super(ShowIfForm, self).clean(*args, **kwargs)
        cln = self.cleaned_data
        vals = set([int(i) for i in cln['values'].split(",") if i])

        if cln.get('previous_question', None) and cln['previous_question'].choices():
            possibles = set([int(c[0]) for c in cln['previous_question'].choices()])
            if not vals.issubset(possibles):
                raise forms.ValidationError("""Valid choices for this questions: %s""" % ("; ".join(possibles), ))
        return cln

    class Meta(object):
        model = ShowIf


class ShowIfAdmin(admin.ModelAdmin):
    form = ShowIfForm
    save_on_top = True


class InstrumentInline(admin.StackedInline):
    model = AskPage.instruments.through
    extra = 0


class QuestionInAskPageAdminForm(forms.ModelForm):
    question = selectable.AutoCompleteSelectField(
        lookup_class=QuestionLookup, allow_new=True,)

    class Meta(object):
        model = QuestionInAskPage

from django.forms import widgets
from django.db import models

class QuestionInline(LinkedInline):
    model = AskPage.questions.through
    form = QuestionInAskPageAdminForm
    order_by = ['order']
    extra = 1
    admin_model_path = "question"


class QuestionInlineForInstruments(QuestionInline):
    model = Instrument.questions.through


class AskPageAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['internal_name', ]
    list_display = ['internal_name', 'asker', 'page_number']
    list_filter = ['asker']
    inlines = [QuestionInline, InstrumentInline]

    def response_change(self, request, obj):
        """Return to the Questionnaire after saving."""

        if request.POST.get("_continue", None):
            return HttpResponseRedirect("")  # redirect back to current page
        else:
            return HttpResponseRedirect(reverse("admin:ask_asker_change",
                args=(str(obj.asker.id), )))


class AskPageInline(LinkedInline):
    model = AskPage
    ordering = ['order']
    extra = 1


class AskerAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['reference', 'page_title', ]
    inlines = [AskPageInline]
    fieldsets = (
        ("Main details", {
            'fields': ('reference', 'page_title', 'show_progress', 'hide_menu')
        }),
    )


class InstrumentAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['name', 'citation']
    inlines = [QuestionInlineForInstruments]


class ChoiceInline(admin.TabularInline):
    model = Choice
    ordering = ['order']
    extra = 3


class ChoiceSetAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['name', 'prompt_wording', 'choice__label']
    inlines = [ChoiceInline]
    list_display = ['name', 'choices_as_string']


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'variable_label': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'help_text': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }


class QuestionAssetInline(admin.TabularInline):
    model = QuestionAsset
    ordering = ['slug']
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    save_on_top = True
    save_as = True
    date_hierarchy = 'last_modified'
    search_fields = ['text', 'variable_name', 'variable_label']
    list_display = ['variable_name', 'text', 'q_type']
    actions = ['make_instrument', ]
    inlines = [QuestionAssetInline]

    fieldsets = (
        ( "Question data", {
        'fields': ( 'q_type', 'text', 'variable_name', 'variable_label', 'always_required', 'choiceset')
        }),
        ( "Additional info", {
        'fields': ( 'help_text', 'audio')
        }),
        ("Advanced", {
        'classes': ('collapse',),
        'fields': (
            'scoresheet', 'field_kwargs', 'widget_kwargs'
        )
        }
    ))

    def make_instrument(self, request, queryset):
        """Creates an Instrument with the queryset of questions passed in.

        Redirects to edit the Instrument.
        Allows users to select questions from a change_list and create a new
        instrument which contains them.
        """
        name = "new instrument includeing %s created %s" % ( queryset[0].variable_name, datetime.now(),)
        inst = Instrument(name = name)
        inst.save()
        questionininstruments = [QuestionInInstrument(question=q, instrument=inst) for q in queryset]
        [i.save() for i in questionininstruments]

        return HttpResponseRedirect("/admin/ask/instrument/%s" % inst.id)

    make_instrument.short_description = "Create new instrument with these questions."

admin.site.register(Permission,)
admin.site.register(ShowIf, ShowIfAdmin)
admin.site.register(Asker, AskerAdmin)
admin.site.register(AskPage, AskPageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(ChoiceSet, ChoiceSetAdmin)
