from datetime import date
from django.db import models
from django.shortcuts import get_object_or_404


class EventManager(models.Manager):
    
    def get_next_in(self, series):
        '''
        Returns the next chronological Event.
        '''
        from fantasy.models import Series
        
        assert isinstance(series, Series)
        qs = self.filter(start_date__gt=date.today())
        if qs:
            return qs[0]
        else:
            return None
 