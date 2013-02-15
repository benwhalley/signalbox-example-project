from __future__ import division

from django.db import models
from collections import defaultdict
from statlib import stats


def float_or_none(string):
    """Try to turn a string into a float, but return None if this fails."""
    
    try:
        return float(string)
    except ValueError:
        return None


class ScoreSheet(models.Model):
    name = models.CharField(blank=True, max_length=80)
    description = models.TextField(blank=True)
    variables = models.ManyToManyField('ask.Question', related_name="varsinscoresheet")
    FUNCTIONS = [(i, i) for i in "sum mean".split(" ")]
    function = models.CharField(max_length=200, choices=FUNCTIONS)
    
    
    def min_number_variables(self):
        return self.variables.all().count()
    
    def score_function(self):
        FUNCTION_LOOKUP = {'sum': sum, 'mean': stats.mean }
        return FUNCTION_LOOKUP[self.function]
    
    def compute(self, answers):
        """Returns a dictionary containing score, scoresheet and a message."""
        
        ret = defaultdict(lambda: None)
        ret['scoresheet'] = self
        
        variable_names = [q.variable_name for q in self.variables.all()]
        answers = [a for a in answers if a.question]
        answers_to_use = [a for a in answers if a.question.variable_name in variable_names]
        
        if len(answers_to_use) != len(variable_names):
            ret['message'] = "Error: only %s answers available, %s needed" % (
                len(answers_to_use), len(variable_names), )
        
        try:
            scores = [float_or_none(a.answer) for a in answers_to_use]
            scores = [a for a in scores if a]
            if len(scores) < self.min_number_variables():
                ret['message'] = "Score based on only %s variables submitted" % len(scores)
            ret['score'] = self.score_function()(scores)
        
        except Exception as e:
            ret['message'] = str(e)
        
        return ret
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.function)
        
    
    class Meta:
        app_label = "signalbox"

