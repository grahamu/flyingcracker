import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from fantasy.models import Series, Event, Competitor, Guess, Result, Team

def root(request):
    active_queryset = Series.objects.filter(
        ~Q(status=Series.COMPLETE_STATUS)).distinct()
    if request.user.is_authenticated():
        if not request.user.is_staff:
            active_queryset = active_queryset.filter(
                ~Q(status=Series.HIDDEN_STATUS) | \
                Q(owner=request.user)).distinct()
    else:
        active_queryset = active_queryset.filter(
            ~Q(status=Series.HIDDEN_STATUS)).distinct()

    completed_queryset = Series.objects.filter(status=Series.COMPLETE_STATUS)

    # BUGBUG
    # filter to:
    #   series for which I am admin
    # plus
    #   series which have 1+ associated Event and 2+ associated Athletes
    c = RequestContext(request, {
        'active_series': active_queryset,
        'completed_series': completed_queryset,
    })
    return render_to_response('fantasy/series_list.html', c)


@login_required
def series_edit(request, id=None):
    '''
    Create a new Series or edit an existing Series.

    '''
    from fc3.fantasy.forms import SeriesForm

    if id:
        series = get_object_or_404(Series, pk=id)
        if not series.is_admin(request.user):
            # cannot edit Series if you're not an admin
            return HttpResponseRedirect(reverse('fantasy-root'))
    else:
        series = Series(owner=request.user)

    if request.method == 'POST':
        series_form = SeriesForm(data=request.POST, instance=series)
        if series_form.is_valid():
            series = series_form.save()
            messages.success(request, 'Saved series "%s".' % str(series))
            return HttpResponseRedirect(reverse('fantasy-root'))
    else:
        series_form = SeriesForm(instance=series)

    c = RequestContext(request, {
        'series_form': series_form,
        'series': series,
    })
    return render_to_response('fantasy/series_edit.html', c)



def series_dashboard(request, id):
    '''
    A list of Events associated with a Series.
    Includes user picks and event winners.

    '''
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
        
    series = get_object_or_404(Series, pk=id)
    qs = Event.objects.filter(series=series)
    next = Event.objects.get_next_in(series)
    current = Event.objects.get_current_in(series)
    next_guesses = None
    events = []
    row_class = 'race-complete'
    for event in qs:
        results = Result.objects.filter(event=event)
        if event.start_time_elapsed() and results:
            row_class = 'race-complete'
        else:
            row_class = 'race-future'
            
        if user:
            ctype, obj_id = event.guess_generics()
            picks = Competitor.objects.filter(guess__content_type=ctype,
                                              guess__object_id=obj_id,
                                              guess__user=user)
            if not picks:
                guesses = None
            else:
                guesses = []
                for pick in picks:
                    result_qs = Result.objects.filter(event=event,
                                                      competitor=pick)
                    if not result_qs:
                        guesses.append(pick)
                    else:
                        result_text = ' & '.join([r.result for r in result_qs])
                        guesses.append(u'(%s) ' % result_text + unicode(pick))
            events.append({'event': event,
                           'guesses': guesses,
                           'row_class': row_class})
            if event == next:
                next_guesses = picks
        else:
            events.append({'event': event,
                           'guesses': None,
                           'row_class': row_class})
            
    # Get context vars for event 'current_event' and
    # add them to this context.
    if current:
        current_event = event_result_context(request, current, user)
    else:
        current_event = None
    if next:
        next_event = event_guess_context(request, next, user)
    else:
        next_event = None
        
    c = RequestContext(request, {
        'series': series,
        'event_list': events,
        'current_event': current_event,
        'next_event': next_event,
        'next_guesses': next_guesses,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(user),
    })
        
    return render_to_response('fantasy/series_home.html', c)


def series_points_list(series, include_late_entries=False,
                       include_timely_entries=True):
    '''
    Returns a list of usernames and their accumulated points in a Series.
    
    '''
    import copy
    
    points_list = []
    
    if not series.scoring_system:
        return points_list
    
    scoresys_results = series.scoring_system.results()
    result_blank = dict.fromkeys(scoresys_results, 0)
    
    event_blank = {}
    # create a list of dictionaries of all events, ordered by date
    # where the key is the event itself and the value is either
    # zero (for events that have occurred) or some other character.
    events = Event.objects.filter(series=series)
    for event in events:
        elapsed = event.start_time_elapsed()
        if elapsed:
            event_blank[event] = 0
        else:
            event_blank[event] = '-'
        
    result_keys = result_blank.keys()
    result_keys = series.scoring_system.sort_by_result(result_keys)
    event_keys = events # Event queryset should already be properly sorted

    user_list = series.guesser_list()
    for u in user_list:
        late_guess_events = Event.objects.filter(guesses__user=u,
                                                 guesses__late_entry=True,
                                                 series=series)
        late_guess_series = Series.objects.filter(guesses__user=u,
                                                  guesses__late_entry=True,
                                                  pk=series.pk)
        if not include_late_entries:
            if late_guess_events or late_guess_series:
                continue
            
        if not include_timely_entries:
            if not late_guess_events and not late_guess_series:
                continue

        if series.guess_once_per_series:
            result_qs = Result.objects.filter(event__series=series,
                            event__series__guesses__user=u,
                            event__series__guesses__competitor=F('competitor'))
        else:
            result_qs = Result.objects.filter(event__series=series,
                            event__guesses__user=u,
                            event__guesses__competitor=F('competitor'))
        points = 0
        result_totals = copy.copy(result_blank)
        event_points = copy.copy(event_blank)
        for r in result_qs:
            result_points = series.scoring_system.points(r.result)
            points += result_points
            
            # number of times user's guess resulted in points for each place
            if r.result in scoresys_results:
                result_totals[r.result] += 1
                
            # total points for each event
            event_points[r.event] += result_points
            
        # Figure the cumulative points for this user
        cumulative_points = []
        last = 0
        for e in event_keys:
            epoints = event_points[e]
            if type(epoints) is int:
                total = epoints + last
            else:
                break
            cumulative_points.append(total)
            last = total
            
        points_list.append({'name': str(u.username),
                            'points': points,
                            'late': late_guess_events or late_guess_series,
                            'place_totals': \
                                [{'key':key, 'val':result_totals[key]} \
                                 for key in result_keys],
                            'event_points': \
                                [{'key':key, 'val':event_points[key]} \
                                 for key in event_keys],
                            'cumulative_points': cumulative_points,
                           })
        
    import operator
    points_list.sort(key=operator.itemgetter('points'), reverse=True)
    
    # Return an empty list if there are no points
    if points_list and points_list[0]['points'] == 0:
        points_list = []
    return points_list


def series_provisional(series):
    if Result.objects.filter(event__series=series, event__result_locked=False):
        return True
    else:
        return False
    
    
def leaderboard(request, id):
    '''
    A list of user scores for events in the series.
    
    '''
    series = get_object_or_404(Series, pk=id)
    user_list = series.guesser_list()
    points_list = series_points_list(series, include_late_entries=False)
    provisional = series_provisional(series)
    late_points_list = series_points_list(series, include_late_entries=True,
                                          include_timely_entries=False)
    scoresys_results = series.scoring_system.results()
    #scoresys_results = sorted(series.scoring_system.results(), key=int)
    c = RequestContext(request, {
        'series': series,
        'points_list': points_list,
        'provisional': provisional,
        'late_points_list': late_points_list,
        'scoresys_results': scoresys_results,
        'user_list': user_list,
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/leaderboard.html', c)


@login_required
def competitor_list(request, id):
    '''
    List all competitors associated with this Series.
    
    '''
    from fc3.fantasy.forms import CompetitorForm
    
    series = get_object_or_404(Series, pk=id)
    if not series.is_admin(request.user):
        # cannot edit Series data if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))
    competitor = Competitor(series=series)
    team_qs = Team.objects.filter(series=series)
        
    if request.method == 'POST':
        competitor_form = CompetitorForm(data=request.POST, team_qs=team_qs,
                                         instance=competitor)
        if competitor_form.is_valid():
            competitor = competitor_form.save()
            messages.success(request, 'Added "%s".' % str(competitor))
            next = request.GET.get('next', None)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('fantasy-competitor-list',
                                                    args=[series.pk]))
            
    else:
        competitor_form = CompetitorForm(team_qs=team_qs, instance=competitor)
    
    competitor_qs = Competitor.objects.filter(series=series)
    
    c = RequestContext(request, {
        'series': series,
        'competitor_list': competitor_qs,
        'competitor_form': competitor_form,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/competitor_list.html', c)


@login_required
def competitor_edit(request, id):
    '''
    Edit the specified Competitor.
    
    '''
    from fc3.fantasy.forms import CompetitorForm

    competitor = get_object_or_404(Competitor, pk=id)
    series = competitor.series
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))
    team_qs = Team.objects.filter(series=series)
    
    if request.method == 'POST':
        competitor_form = CompetitorForm(data=request.POST,
                                         instance=competitor,
                                         team_qs=team_qs,
                                         initial={'series_pk': series.pk})
        if competitor_form.is_valid():
            competitor = competitor_form.save()
            messages.success(request, 'Saved "%s".'
                             % str(competitor))
            return HttpResponseRedirect(reverse('fantasy-competitor-list',
                                                args=[series.pk]))
    else:
        competitor_form = CompetitorForm(instance=competitor,
                                         team_qs=team_qs,
                                         initial={'series_pk': series.pk})

    c = RequestContext(request, {
        'competitor_form': competitor_form,
        'series': series,
        'competitor': competitor,
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/competitor_edit.html', c)


@login_required
def competitor_delete(request, id):
    '''
    Delete the specified Competitor from its Series.
    
    '''
    competitor = get_object_or_404(Competitor, pk=id)
    series = competitor.series
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    results = Result.objects.filter(competitor=competitor)
    if results:
        c = RequestContext(request, {
            'series': series,
            'competitor': competitor,
            'result_list': results,
            'is_admin': series.is_admin(request.user),
        })
        return render_to_response('fantasy/competitor_delete.html', c)
    else:
        competitor.delete()
        return HttpResponseRedirect(reverse('fantasy-competitor-list',
                                            args=[series.pk]))

    
@login_required
def competitor_export(request, id):
    '''
    Export all competitors associated with this Series.
    
    '''
    import csv
    from django.utils.encoding import smart_str, smart_unicode

    series = get_object_or_404(Series, pk=id)
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = \
            'attachment; filename=competitor_list_series_%d.csv' % series.pk
    writer = csv.writer(response)
    
    writer.writerow(['name'])
    qs = Competitor.objects.filter(series=series)
    for competitor in qs:
        writer.writerow([smart_str(competitor.name)])
    return response


@login_required
def competitor_import(request, id):
    '''
    Import Competitors from other Series into the specified Series.
    
    '''
    from fc3.fantasy.forms import CompetitorImportForm

    series = get_object_or_404(Series, pk=id)
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    qs = Series.objects.filter(only_members_can_view=False)
    #
    # BUGBUG - Add private Series, for which I am admin, to this queryset
    #
    if request.method == 'POST':
        import_form = CompetitorImportForm(data=request.POST, series_qs=qs)
        if import_form.is_valid():
            import_series = import_form.cleaned_data['series']
            if import_series:
                my_comps = Competitor.objects.filter(series=series)
                my_names = [c.name.lower() for c in my_comps]
                import_comps = Competitor.objects.filter(series=import_series)
                new_names = [c.name for c in import_comps if c.name.lower() \
                             not in my_names]
                for name in new_names:
                    new_competitor = Competitor(name=name, series=series)
                    new_competitor.save()
                c = RequestContext(request, {
                    'series': series,
                    'competitor_list': Competitor.objects.filter(
                        name__in=new_names, series=series),
                    'is_admin': series.is_admin(request.user),
                })
                messages.success(request,
                                 '%d competitors were successfully imported.' \
                                 % new_names.count())
                return render_to_response('fantasy/competitors_imported.html',
                                          c)
            else:
                return HttpResponseRedirect(reverse('fantasy-competitor-list',
                                                    args=[series.pk]))
    else:
        import_form = CompetitorImportForm(series_qs=qs)

    c = RequestContext(request, {
        'import_form': import_form,
        'series': series,
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/competitor_import.html', c)


@login_required
def event_add(request, series_id):
    '''
    Add a new event to the specified Series.
    
    '''
    from fc3.fantasy.forms import EventForm

    series = get_object_or_404(Series, pk=series_id)
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))
    event = Event(series=series)

    if request.method == 'POST':
        event_form = EventForm(data=request.POST, instance=event)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.series = series
            event.save()
            messages.success(request, 'Added event "%s".' % event)
            return HttpResponseRedirect(reverse('fantasy-series-home',
                                                args=[series.pk]))
    else:
        event_form = EventForm(instance=event)

    c = RequestContext(request, {
        'event_form': event_form,
        'series': series,
        'event': event,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/event_edit.html', c)



@login_required
def event_edit(request, id):
    '''
    Edit the specified Event.
    
    '''
    from fc3.fantasy.forms import EventForm

    event = get_object_or_404(Event, pk=id)
    series = event.series
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    if request.method == 'POST':
        event_form = EventForm(data=request.POST, instance=event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, 'Saved %s "%s".' % \
                             (series.event_label, event))
            return HttpResponseRedirect(reverse('fantasy-series-home',
                                                args=[series.pk]))
    else:
        event_form = EventForm(instance=event)

    c = RequestContext(request, {
        'event_form': event_form,
        'series': series,
        'event': event,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/event_edit.html', c)


@login_required
def event_delete(request, id):
    '''
    Delete the specified Event from the Series.
    
    '''
    event = get_object_or_404(Event, pk=id)
    series = event.series
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    results = Result.objects.filter(event=event)
    if results:
        c = RequestContext(request, {
            'series': series,
            'event': event,
            'result_list': results,
            'points_list': series_points_list(series)[:10],
            'provisional': series_provisional(series),
            'is_admin': series.is_admin(request.user),
        })
        return render_to_response('fantasy/event_delete.html', c)
    else:
        event.delete()
        return HttpResponseRedirect(series.get_absolute_url)

    
def event_detail(request, id):
    '''
    Shows either the results of a event
    or
    Allows user to select one or more Competitors he thinks will
    perform well, or possibly enter a new Competitor.
    
    '''
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
        
    event = get_object_or_404(Event, pk=id)
    series = event.series
    ctype, obj_id = event.guess_generics()
    
    cv = event_guess_context(request, event, user)
    if cv['guess_deadline_elapsed']:
        if series.allow_late_guesses:
            if cv['guesses']:
                return event_result(request, id)
        else:
            return event_result(request, id)
    
    if request.method == 'POST' and cv['formset'].is_valid():
        selected_competitors = []
        for guess in cv['formset'].cleaned_data:
            if guess.get('competitor', None):
                selected_competitors.append(Competitor.objects \
                                            .get(pk=guess['competitor']))
                
        cv['curr_guesses'].delete()   # delete user's guesses for this event
        for competitor in selected_competitors:
            g = Guess.objects.create(content_type=ctype,
                                     object_id=obj_id,
                                     user=user,
                                     competitor=competitor,
                                     late_entry=cv['guess_deadline_elapsed'])
            
        if cv['options_form'].is_valid() and \
           cv['options_form'].cleaned_data['remaining_events']:
            # Remove guesses for incomplete events
            # and substitute these picks.
            qs = Event.objects.filter(series=series,
                            guess_deadline__gt=datetime.datetime.today()) \
               .exclude(pk=event.pk)
            for incomplete_event in qs:
                ctype, obj_id = incomplete_event.guess_generics()
                curr_guesses = Guess.objects.filter(content_type=ctype,
                                                    object_id=obj_id,
                                                    user=user)
                curr_guesses.delete()
                for competitor in selected_competitors:
                    g = Guess.objects.create(content_type=ctype,
                                             object_id=obj_id,
                                             user=user,
                                             competitor=competitor)

            messages.success(request, "Saved %s for "
                             "%d upcoming %ss." % (", ". \
                                join([str(c) for c in selected_competitors]),
                                (len(qs)+1), event.series.event_label))
        else:
            messages.success(request, "Saved %s for %s." % (", ". \
                                join([str(c) for c in selected_competitors]),
                                event))
            
        next = request.GET.get('next', None)
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect(reverse('fantasy-event-detail',
                                            args=[event.pk]))
        
    c = RequestContext(request, {'wrapper': cv,
                                 'is_admin': series.is_admin(request.user),
                                 'series': series,
                                 'event': event,
                                 })
    return render_to_response('fantasy/event_guess.html', c)

def event_guess_context(request, event, user):
    '''
    Returns a dictionary of context variables for event guess.
    '''
    from fantasy.forms import GuessForm, GuessAndResultBaseFormset, \
         TeamGuessForm, PickOptionsForm
    from django.forms.formsets import formset_factory
    from django.utils.encoding import smart_str
    
    series = event.series
    # Create un-saved instance for adding a new Competitor
    competitor = Competitor(series=series)
    
    ctype, obj_id = event.guess_generics()
    curr_guesses = Guess.objects.filter(content_type=ctype, object_id=obj_id,
                                        user=user)
    guesses = [{'competitor': r.competitor.pk} for r in curr_guesses]
    
    guess_deadline_elapsed = event.guess_deadline_elapsed()
    late_entry = False
    if guess_deadline_elapsed:
        if series.allow_late_guesses:
            if not guesses:
                late_entry = True

    GuessFormset = formset_factory(GuessForm, GuessAndResultBaseFormset,
                                    max_num=series.num_guesses,
                                    extra=series.num_guesses)

    competitor_choices = [('', '------')]
    competitor_choices.extend([(c.pk, smart_str(c.name_and_team())) \
                               for c in Competitor.objects.filter \
                               (series=series, active=True)])

    team_choices = [('', '------')]
    # This value for each Team choice consists of a comma-separated list
    # Competitor pks for Competitors who are members of the Team.
    team_choices.extend([(",".join([str(c.pk) \
                                    for c in t.competitor_set.all()]),
                          smart_str(t.short())) for t in Team.objects.filter( \
                              series=series).order_by('short_name', 'name')])

    formset = GuessFormset(data=request.POST or None, initial=guesses,
                           competitors=competitor_choices)
    options_form = PickOptionsForm(data=request.POST or None)

    team_form = TeamGuessForm(data=request.POST or None, teams=team_choices)

    guess_list = event.guess_list()
    guesses = []
    # We want just one Guess per guesser
    players = []
    for g in guess_list:
        if g['player'] not in players:
            guesses.append(g)
            players.append(g['player'])

    if curr_guesses:
        guess_timestamp = curr_guesses[0].timestamp
    else:
        guess_timestamp = None
    
    return {
        'series': event.series,
        'event': event,
        'is_admin': series.is_admin(user),
        'late_entry': late_entry,
        'formset': formset,
        'options_form': options_form,
        'team_form': team_form,
        'guesses': guesses,        
        'guess_timestamp': guess_timestamp,
        'guess_deadline_elapsed': guess_deadline_elapsed,
        'curr_guesses': curr_guesses,
        'add_competitor_ok': False, # series.users_enter_competitors,
    }


def event_result(request, id):
    '''
    Shows the results of an event.
    
    '''
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    event = get_object_or_404(Event, pk=id)
    series = event.series

    if not event.guess_deadline_elapsed():
        messages.info(request, "The guess deadline has not been reached!")
        return HttpResponseRedirect(reverse('fantasy-series-home',
                                            args=[series.pk]))

    context_vars = event_result_context(request, event, user)
        
    c = RequestContext(request, context_vars)
    return render_to_response('fantasy/event_result.html', c)


def event_result_context(request, event, user):
    '''
    Returns a dictionary of context variables for event result.
    '''
    series = event.series
    user_guesses = []
    guess_qs = event.guesses.filter(user=user)
    if guess_qs:
        for guess in guess_qs:
            try:
                result = Result.objects.get(competitor=guess.competitor,
                                            event=event)
            except Result.DoesNotExist:
                result = 'X'
            else:
                result = str(result.result)
            user_guesses.append({'result': result,
                                 'competitor': guess.competitor})
        guess_timestamp = guess_qs[0].timestamp
    else:
        guess_timestamp = None

    result_qs = Result.objects.filter(event=event,
                                    result__in=series.scoring_system.results())
    ordered_results = series.scoring_system.sort_by_result(list(result_qs),
                                                           'result')
    
    # Get the content_type and object_id
    # for referencing guesses made for this Event.
    ctype, obj_id = event.guess_generics()

    bad_guess_list = []
    # list of results for this event where the place yielded no points.
    no_points_list = Result.objects.filter(~Q(result__in=
                                              series.scoring_system.results()),
                                           event=event).order_by('result')
    for result in no_points_list:
        guessers = Guess.objects.filter(content_type=ctype, object_id=obj_id,
                                        competitor=result.competitor)
        bad_guess_list.append({'competitor': result.competitor,
                               'result': result.result,
                               'guessers': [g.user for g in guessers]})

    # list of competitors guessed for this event
    # who have no result... FOR THE EVENT!
    all_guesses_qs = Competitor.objects.filter(guess__content_type=ctype,
                                            guess__object_id=obj_id).distinct()
    no_result_list = all_guesses_qs.exclude(result__event=event)
    for bad_guess in no_result_list:
        guessers = Guess.objects.filter(content_type=ctype, object_id=obj_id,
                                        competitor=bad_guess)
        bad_guess_list.append({'competitor': bad_guess, 'result': '?',
                               'guessers': [g.user for g in guessers]})

    found_results = False
    late_guesses = False
    event_points_list = []
    guesser_list = series.guesser_list()
    for u in guesser_list:
        guess_qs = Guess.objects.filter(content_type=ctype, object_id=obj_id,
                                        user=u)
        if not guess_qs:
            late_entry = False
            all_result_qs = []
        else:
            late_entry = guess_qs[0].late_entry
            if late_entry:
                late_guesses = True
            if series.guess_once_per_series:
                all_result_qs = Result.objects.filter(event=event,
                            event__series__guesses__user=u,
                            event__series__guesses__competitor=F('competitor'))
            else:
                all_result_qs = Result.objects.filter(event=event,
                            event__guesses__user=u,
                            event__guesses__competitor=F('competitor'))
        points = 0
        if all_result_qs:
            found_results = True
        for r in all_result_qs:
            result_points = series.scoring_system.points(r.result)
            points += result_points
            
        event_points_list.append({'name': str(u.username),
                                  'points': points,
                                  'late': late_entry,
                                 })
        
    import operator
    event_points_list.sort(key=operator.itemgetter('points'), reverse=True)
    if not found_results:
        event_points_list = None

    guess_list = event.guess_list()
    guesses = []
    # We want just one Guess per guesser
    players = []
    for g in guess_list:
        if g['player'] not in players:
            guesses.append(g)
            players.append(g['player'])
        
    return {
        'series': event.series,
        'event': event,
        'result_list': ordered_results,
        'bad_guess_list': bad_guess_list,
        'event_points_list': event_points_list,
        'late_guesses': late_guesses,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(user),
        'user_guesses': user_guesses,
        'guess_timestamp': guess_timestamp,
        'guesses': guesses,
    }

    
@login_required
def result_edit(request, id):
    '''
    Edit the results for a event.
    
    '''
    from fc3.fantasy.forms import ResultForm, GuessAndResultBaseFormset, \
         EventOptionsForm
    from django.forms.formsets import formset_factory
    
    event = get_object_or_404(Event, pk=id)
    series = event.series
    if (not series.is_admin(request.user) and event.result_locked):
        messages.info(request, "Sorry, results are locked for this event.")
        return HttpResponseRedirect(reverse('fantasy-series-home',
                                            args=[series.pk]))
    if not event.guess_deadline_elapsed():
        messages.error(request, "The guess deadline has not been reached!")
        return HttpResponseRedirect(reverse('fantasy-series-home',
                                            args=[series.pk]))
    
    all_competitors = Competitor.objects.filter(series=series)
    competitor_choices = [('', '------')]
    competitor_choices.extend([(a.pk, str(a)) for a in all_competitors])
    
    event_results = Result.objects.filter(event=event)
    ordered_results = series.scoring_system.sort_by_result(list(event_results),
                                                           'result')
    
    all_result_list = series.scoring_system.results()

    # Create a list of results for this Event
    if not ordered_results:
        unassigned_results = results = initial_results = \
                           [{'result': s} for s in all_result_list]
        entered_by = None
    else:
        entered_by = ordered_results[0].entered_by
        results = [{'result': r.result, 'competitor': r.competitor.pk}  
                   for r in ordered_results]
        curr_result_list = [r.result for r in ordered_results]
        unassigned_results = series.scoring_system. \
                           sort_by_result(list(set(all_result_list) - 
                                               set(curr_result_list)))
        initial_results = results + [{'result': s} for s in unassigned_results]

    ResultFormset = formset_factory(ResultForm, GuessAndResultBaseFormset,
                                    max_num=len(ordered_results) +
                                            len(unassigned_results) + 1)

    if request.method == 'POST':
        formset = ResultFormset(request.POST, initial=initial_results,
                                competitors=competitor_choices)
        options_form = EventOptionsForm(data=request.POST, instance=event)
        if formset.is_valid() and options_form.is_valid():
            event = options_form.save()
            
            # Create a list in the same format as 'results'.
            # If nothing has changed, don't erase and resave!
            form_results = [{'result': result['result'],
                             'competitor': int(result['competitor'])}
                            for result in formset.cleaned_data
                            if result and result['result']
                                and result['competitor']]
            form_results.sort()
            results.sort()
            if form_results != results:
                event_results.delete()   # delete user's results for this event
                
                for result in form_results:
                    r = Result(event=event,
                               result=result['result'],
                               competitor=Competitor.objects.get(
                                   pk=result['competitor']),
                               entered_by=request.user)
                    r.save()
            messages.success(request, '%s results have been saved.'
                             % str(series.event_label))
            return HttpResponseRedirect(reverse('fantasy-series-home',
                                                args=[series.pk]))
    else:
        formset = ResultFormset(initial=initial_results,
                                competitors=competitor_choices)
        options_form = EventOptionsForm(instance=event)

    c = RequestContext(request, {
        'series': event.series,
        'event': event,
        'formset': formset,
        'options_form': options_form,
        'entered_by': entered_by,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/result_edit.html', c)


@login_required
def team_add(request, series_id):
    '''
    Enter a new Team.
    
    '''
    from fc3.fantasy.forms import TeamEditForm

    series = get_object_or_404(Series, pk=series_id)
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    team = Team(series=series)
    competitor_qs = Competitor.objects.filter(series=series, team=None)
    
    if request.method == 'POST':
        team_form = TeamEditForm(data=request.POST,
                                 instance=team,
                                 competitor_qs=competitor_qs)
        if team_form.is_valid():
            team = team_form.save()
            messages.success(request, 'Added new team "%s".' % team)
            return HttpResponseRedirect(reverse('fantasy-team-list',
                                                args=[series.pk]))
    else:
        team_form = TeamEditForm(instance=team,
                                 competitor_qs=competitor_qs)

    c = RequestContext(request, {
        'team_form': team_form,
        'series': series,
        'team': team,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/team_edit.html', c)


@login_required
def team_edit(request, id):
    '''
    Edit a Team.
    
    '''
    from fc3.fantasy.forms import TeamEditForm

    team = get_object_or_404(Team, pk=id)
    series = team.series
    
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))
    
    competitor_qs = Competitor.objects.filter(series=series)
    members = [str(c.pk) for c in Competitor.objects.filter(team=team)]
    
    if request.method == 'POST':
        team_form = TeamEditForm(data=request.POST,
                                 instance=team,
                                 competitor_qs=competitor_qs,
                                 initial={'members': members},
                                )
        if team_form.is_valid():
            team = team_form.save()
            messages.success(request, 'Saved team "%s".' % str(team))
            return HttpResponseRedirect(reverse('fantasy-team-list',
                                                args=[series.pk]))
    else:
        team_form = TeamEditForm(instance=team,
                                 competitor_qs=competitor_qs,
                                 initial={'members': members})

    c = RequestContext(request, {
        'team_form': team_form,
        'series': series,
        'team': team,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/team_edit.html', c)


@login_required
def team_list(request, series_id):
    '''
    List all Teams for a Series.
    
    '''
    series = get_object_or_404(Series, pk=series_id)
    team_qs = Team.objects.filter(series=series)

    c = RequestContext(request, {
        'series': series,
        'team_list': team_qs,
        'points_list': series_points_list(series)[:10],
        'provisional': series_provisional(series),
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/team_list.html', c)


@login_required
def team_detail(request, id):
    '''
    Show detail on the specified Team.
    
    '''
    team = get_object_or_404(Team, pk=id)
    series = team.series
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    c = RequestContext(request, {
        'series': series,
        'team': team,
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/team_detail.html', c)


@login_required
def team_delete(request, id):
    '''
    Delete the specified Team from the Series.
    
    '''
    team = get_object_or_404(Team, pk=id)
    series = team.series
    if not series.is_admin(request.user):
        # cannot edit Series if you're not an admin
        return HttpResponseRedirect(reverse('fantasy-root'))

    for competitor in team.competitor_set.all():
        competitor.team = None
        competitor.save()
    team.delete()
    return HttpResponseRedirect(reverse('fantasy-team-list', args=[series.pk]))


@login_required
def series_email(request, id):
    '''
    Email all users associated with a Series.
    
    '''
    from fc3.fantasy.forms import EmailSeriesForm
    from django.conf import settings
    from django.core.mail import EmailMessage

    series = get_object_or_404(Series, pk=id)
    if not series.is_admin(request.user):
        return HttpResponseRedirect(reverse('fantasy-root'))

    if request.method == 'POST':
        email_form = EmailSeriesForm(data=request.POST)
        if email_form.is_valid():
            cd = email_form.cleaned_data
            # remove newlines from subject
            subject = ''.join(cd['subject'].splitlines())
            body = cd['body']
            guessers = series.guesser_list()
            # Email messages
            mail_from = request.user.email or settings.DEFAULT_FROM_EMAIL
            bcc_recipients = [user.email for user in guessers if user.email]
            if mail_from in bcc_recipients:
                bcc_recipients.remove(mail_from)
            msg = EmailMessage(subject=subject, body=body,
                               from_email=mail_from, to=[mail_from],
                               bcc=bcc_recipients)
            msg.send()
            
#            send_mail(subject, body, mail_from, recipients)

            messages.success(request, 'Your email has been sent.')
            return HttpResponseRedirect(reverse('fantasy-series-home',
                                                args=[series.pk]))
    else:
        email_form = EmailSeriesForm()

    c = RequestContext(request, {
        'email_form': email_form,
        'series': series,
        'is_admin': series.is_admin(request.user),
    })
    return render_to_response('fantasy/series_email.html', c)
