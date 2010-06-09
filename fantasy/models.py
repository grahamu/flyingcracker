from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models import permalink
from datetime import date, datetime
from django.utils.translation import ugettext_lazy as _
from scoresys.models import ScoringSystem
from fantasy import managers


class Series(models.Model):
    '''
    A series of one or more events, i.e. Formula One 2009.
    
    '''
    name                    = models.CharField(max_length=100, unique=True)
    description             = models.CharField(max_length=100, blank=True, null=True)
    start_date              = models.DateField()
    end_date                = models.DateField()
    competitor_label        = models.CharField(help_text='How competitors are referred to, i.e. "Driver" or "Rider".', max_length=50, default='Driver')
    event_label             = models.CharField(help_text='How series events are referred to, i.e. "Race" or "Stage".', max_length=50, default='Race')
    num_guesses             = models.PositiveIntegerField('# guesses', help_text='The number of competitors a user can pick for each event.', default=1)
    guess_once_per_series   = models.BooleanField('Pick competitors once for entire series', default=False)
    allow_late_guesses      = models.BooleanField('Allow late guesses', help_text='Late guesses will not count in Series standings', default=False)
    late_entry_footnote     = models.CharField(max_length=100, default="player entered late picks", blank=True)
    invite_only             = models.BooleanField('Users must be invited', default=False)
    only_members_can_view   = models.BooleanField('Only members can view results')
    users_enter_competitors = models.BooleanField('Users can add competitors', default=True)
    scoring_system          = models.ForeignKey(ScoringSystem, blank=True, null=True)
    HIDDEN_STATUS = 'H'
    ACTIVE_STATUS = 'A'
    COMPLETE_STATUS = 'C'
    STATUS_TYPES = (
        (HIDDEN_STATUS, 'HIDDEN - only admin can view'),
        (ACTIVE_STATUS, 'ACTIVE - ready for use'),
        (COMPLETE_STATUS, 'COMPLETE - series is finished'),
    )
    status                  = models.CharField(max_length=1, choices=STATUS_TYPES, default=HIDDEN_STATUS, blank=False)
    owner                   = models.ForeignKey(User)
    guesses                 = generic.GenericRelation('Guess')

    class Meta:
        verbose_name = 'series'
        verbose_name_plural = 'series'
        ordering = ('name',)

    def guesser_list(self):
        '''
        Returns a list of Users who have guesses in this Series.
        
        '''
        if self.guess_once_per_series:
            guessers = [g.user for g in self.guesses.all()]
        else:
            events = Event.objects.filter(series=self)
            guessers = []
            for event in events:
                guessers.extend([g.user for g in event.guesses.all()])
        # make our list of guessers contain only unique entries
        return list(set(guessers))

    def guess_deadline_elapsed(self):
        return self.guess_cutoff() < datetime.utcnow()

    def guess_cutoff(self):
        qs = Event.objects.filter(series=self).order_by('guess_deadline')
        return qs[0].guess_deadline
        
    def is_admin(self, user):
        return user == self.owner or user.is_staff
    
    def is_hidden(self):
        return self.status == self.HIDDEN_STATUS
    
    def is_complete(self):
        return self.status == self.COMPLETE_STATUS
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return ('fantasy-event-list', [self.pk])
    get_absolute_url = permalink(get_absolute_url)


class Event(models.Model):
    '''
    An event in a series, i.e. Monaco Grand Prix.
    
    '''
    name            = models.CharField(max_length=100)
    description     = models.CharField(max_length=100, blank=True, null=True)
    start_date      = models.DateField()
    start_time      = models.TimeField(help_text='in UTC (Greenwich time)')
    guess_deadline  = models.DateTimeField('Guess cutoff date & time', help_text='(format: YYYY-MM-DD HH:MM) in UTC (Greenwich time)', blank=True, null=True)
    location        = models.CharField(max_length=100, blank=True, null=True)
    series          = models.ForeignKey(Series)
    result_locked   = models.BooleanField('Lock results', default=False, help_text='If unlocked, users are allowed to enter results.')
    guesses         = generic.GenericRelation('Guess')
    
    objects = managers.EventManager()
    
    class Meta:
        ordering = ['start_date']
        unique_together = ('name', 'series')

    def guess_cutoff(self):
        '''
        For display only.
        
        '''
        if self.guess_deadline:
            return self.guess_deadline
        else:
            return self.series.guess_cutoff()

    def guess_deadline_elapsed(self):
        if self.guess_deadline:
            return self.guess_deadline < datetime.utcnow()
        else:
            return self.series.guess_deadline_elapsed()

    def start_time_elapsed(self):
        return datetime.combine(self.start_date, self.start_time) < datetime.utcnow()

    def guess_generics(self):
        if self.series.guess_once_per_series:
            ctype = ContentType.objects.get_for_model(Series)
            obj_id = self.series.pk
        else:
            ctype = ContentType.objects.get_for_model(Event)
            obj_id = self.pk
        return ctype, obj_id

    def guesser_list(self):
        if self.series.guess_once_per_series:
            return self.series.guesser_list()
        else:
            guessers = [g.user for g in self.guesses.all()]
        # make our list of guessers contain only unique entries
        return list(set(guessers))

    def guess_list(self):
        '''
        Returns a queryset of Guesses for this Event.
        '''
        if self.series.guess_once_per_series:
            return self.series.guesses()
        else:
            guesses = [{'timestamp': g.timestamp, 'player':g.user}
                       for g in self.guesses.all().order_by('timestamp')]
        return guesses
        
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return ('fantasy-event-detail', [self.pk])
    get_absolute_url = permalink(get_absolute_url)


class Competitor(models.Model):
    name        = models.CharField(max_length=100)
    series      = models.ForeignKey(Series)
    team        = models.ForeignKey('Team', blank=True, null=True)
    
    class Meta:
        unique_together = ('name', 'series')
        ordering = ['name']
    
    def __unicode__(self):
        return u'%s' % self.name

    def name_and_team(self):
        if self.team:
            return u'%s - %s' % (self.name, self.team.short())
        else:
            return u'%s' % self.name


class Team(models.Model):
    series          = models.ForeignKey(Series)
    name            = models.CharField(max_length=100)
    short_name      = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return u'%s' % self.name
    
    def short(self):
        if self.short_name:
            return u'%s' % self.short_name
        else:
            return self.__unicode__()


class Result(models.Model):
    competitor  = models.ForeignKey(Competitor)
    event       = models.ForeignKey(Event)
    result      = models.CharField(max_length=50)
    entered_by  = models.ForeignKey(User, blank=True, null=True)
    
    class Meta:
        ordering = ['result']
        unique_together = ('competitor','event', 'result')
    
    def __unicode__(self):
        return u'%s: %s: %s' % (self.event, self.result, self.competitor)

    def guessers(self):
        ctype, obj_id = self.event.guess_generics()
        guessers = Guess.objects.filter(content_type=ctype, object_id=obj_id, competitor=self.competitor)
        return [g.user for g in guessers]

    def points_for_result(self):
        return self.event.series.scoring_system.points(self.result)
    
    
class Guess(models.Model):
    user            = models.ForeignKey(User)
    competitor      = models.ForeignKey(Competitor)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    guess_for       = generic.GenericForeignKey()
    late_entry      = models.BooleanField(default=False)
    timestamp       = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'guesses'
    
    def __unicode__(self):
        return u'%s: %s by %s' % (self.guess_for, self.competitor, self.user)

    def save(self, **kwargs):
        if not self.id:
            self.timestamp = datetime.now()
        super(Guess, self).save()