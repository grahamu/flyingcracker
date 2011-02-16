from datetime import datetime
from django.db import models
from django.shortcuts import get_object_or_404


class EventManager(models.Manager):
    
    def get_next_in(self, series):
        '''
        Returns the next chronological Event.
        '''
        from fantasy.models import Series
        
        assert isinstance(series, Series)
        qs = self.filter(guess_deadline__gt=datetime.utcnow())
        if qs:
            return qs[0]
        else:
            return None
        
    def get_current_in(self, series):
        '''
        Returns the previous chronological Event.
        '''
        from fantasy.models import Series
        
        assert isinstance(series, Series)
        qs = self.filter(guess_deadline__lt=datetime.utcnow()). \
           order_by("-start")
        if qs:
            return qs[0]
        else:
            return None
        
 