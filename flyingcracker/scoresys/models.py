from django.db import models


class ScoringSystem(models.Model):
    '''
    Associated with one or more ResultPoints.

    '''
    name = models.CharField('Scoring system name',
                            max_length=100, unique=True)
    num_places = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name

    def points(self, result):
        '''
        Return points associated with a specific result.

        '''
        try:
            rp = ResultPoints.objects.get(system=self, result=result)
        except ResultPoints.DoesNotExist:
            return 0
        return rp.points

    def results(self):
        '''
        Returns list of all 'result's from associated ResultPoints.

        '''
        qs = ResultPoints.objects.filter(system=self)
        return [rp.result for rp in qs]

    def sort_by_result(self, seq, attr=None):
        rp_dict = dict((rp.result, rp.rank)
                       for rp in ResultPoints.objects.filter(system=self))
        if attr:
            intermed = [(rp_dict.get(getattr(obj, attr), 999), obj)
                        for obj in seq]
        else:
            intermed = [(rp_dict.get(obj, 999), obj) for obj in seq]
        intermed.sort()
        return [r[-1] for r in intermed]


class ResultPoints(models.Model):
    result = models.CharField(max_length=50)
    points = models.IntegerField()
    system = models.ForeignKey(ScoringSystem, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return u'%s: %s=%d' % (str(self.system), self.result, self.points)

    class Meta:
        verbose_name_plural = 'Result points'
        ordering = ['rank']