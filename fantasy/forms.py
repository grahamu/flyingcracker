#!/usr/bin/env python
import datetime
from django import forms
from django.forms import formsets
from django.utils.translation import ugettext_lazy as _
from fc3.fantasy.models import Series, Event, Competitor, Guess, Result, Team


attrs_dict = { 'class': 'required' }


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        exclude = ('owner', 'invite_only', 'only_members_can_view')


class CompetitorForm(forms.ModelForm):
    series = forms.ModelChoiceField(queryset=Series.objects.all(), widget=forms.HiddenInput)
    
    class Meta:
        model = Competitor
        fields = ('name','series')
        
    def clean(self):
        name = self.cleaned_data.get('name')
        series = self.cleaned_data.get('series')
        if not name:
            raise forms.ValidationError, u'Please enter a Competitor name in the field provided'
        if self.instance.pk:
            existing = Competitor.objects.filter(name__iexact=name, series=series).exclude(pk=self.instance.pk)
            if existing:
                raise forms.ValidationError, u'Competitor "%s" already exists for this series, try another name' % name
            else:
                return self.cleaned_data
        else:
            try:
                existing = Competitor.objects.get(name__iexact=name, series=series)
            except Competitor.DoesNotExist:
                return self.cleaned_data
            else:
                raise forms.ValidationError, u'Competitor "%s" already exists for this series, try another name' % name


class EventForm(forms.ModelForm):
    series = forms.ModelChoiceField(queryset=Series.objects.all(), widget=forms.HiddenInput)
    
    class Meta:
        model = Event

    def clean(self):
        name = self.cleaned_data.get('name')
        series = self.cleaned_data.get('series')
        if self.instance.pk:
            existing = Event.objects.filter(name__iexact=name, series=series).exclude(pk=self.instance.pk)
            if existing:
                raise forms.ValidationError, u'{{ series.event_label|capfirst }} "%s" already exists for this series, try another name' % name
            else:
                return self.cleaned_data
        else:
            try:
                existing = Event.objects.get(name__iexact=name, series=series)
            except Event.DoesNotExist:
                return self.cleaned_data
            else:
                raise forms.ValidationError, u'{{ series.event_label|capfirst }} "%s" already exists for this series, try another name' % name


class GuessAndResultBaseFormset(formsets.BaseFormSet):

    def __init__(self, *args, **kwargs):
        self.competitors = kwargs.pop('competitors', None)
        super(GuessAndResultBaseFormset, self).__init__(*args, **kwargs)
    
    def _construct_form(self, i, **kwargs):
        kwargs["competitors"] = self.competitors
        return super(GuessAndResultBaseFormset, self)._construct_form(i, **kwargs)


class GuessForm(forms.Form):
    competitor = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        competitor_list = kwargs.pop('competitors', None)
        super(GuessForm, self).__init__(*args, **kwargs)
        self['competitor'].field.choices = competitor_list
        self['competitor'].field.label = 'Choose'


class TeamGuessForm(forms.Form):
    team = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        team_list = kwargs.pop('teams', None)
        super(TeamGuessForm, self).__init__(*args, **kwargs)
        self['team'].field.choices = team_list
 

class ResultForm(forms.Form):
    result = forms.CharField(required=False)
    competitor = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        competitor_list = kwargs.pop('competitors', None)
        form_num = kwargs.pop('form_num', 0)
        super(ResultForm, self).__init__(*args, **kwargs)
        self['competitor'].field.choices = competitor_list

    def clean(self):
        result = self.cleaned_data.get('result', None)
        competitor = self.cleaned_data.get('competitor', None)
        if competitor and not result:
            raise forms.ValidationError, _(u'This competitor has no result!')
        return self.cleaned_data


class EventOptionsForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ('result_locked',)


class CompetitorImportForm(forms.Form):
    series = forms.ModelChoiceField(queryset=Series.objects.all())

    def __init__(self, *args, **kwargs):
        series_qs = kwargs.pop('series_qs', [])
        super(CompetitorImportForm, self).__init__(*args, **kwargs)
        self['series'].field.queryset = series_qs
        

class TeamEditForm(forms.ModelForm):
    
    class Meta:
        model = Team
        fields = ('name', 'competitors')

    def __init__(self, *args, **kwargs):
        competitor_qs = kwargs.pop('competitor_qs', None)
        super(TeamEditForm, self).__init__(*args, **kwargs)
        if competitor_qs:
            self['competitors'].field.queryset = competitor_qs
