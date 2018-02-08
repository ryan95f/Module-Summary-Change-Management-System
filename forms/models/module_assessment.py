from django.db import models
from core.models import Module
from django.core.validators import MaxValueValidator

HAND_OUT_IN_OPTIONS = (
    ('1A', 'Autumn Week 1'),
    ('2A', 'Autumn Week 2'),
    ('3A', 'Autumn Week 3'),
    ('4A', 'Autumn Week 4'),
    ('5A', 'Autumn Week 5'),
    ('6A', 'Autumn Week 6'),
    ('7A', 'Autumn Week 7'),
    ('8A', 'Autumn Week 8'),
    ('9A', 'Autumn Week 9'),
    ('10A', 'Autumn Week 10'),
    ('11A', 'Autumn Week 11'),
    ('1S', 'Spring Week 1'),
    ('2S', 'Spring Week 2'),
    ('3S', 'Spring Week 3'),
    ('4S', 'Spring Week 4'),
    ('5S', 'Spring Week 5'),
    ('6S', 'Spring Week 6'),
    ('7S', 'Spring Week 7'),
    ('8S', 'Spring Week 8'),
    ('9S', 'Spring Week 9'),
    ('10S', 'Spring Week 10'),
    ('11S', 'Spring Week 11'),
)

SEMESTER_OPTIONS = (
    ('Autumn Semester', 'Autumn Semester'),
    ('Spring Semester', 'Spring Semester'),
)

class ModuleAssessment(models.Model):
    """
    Model which represents the assessment details of a module
    """

    assessment_id = models.AutoField(primary_key=True)
    assessment_title = models.CharField(max_length=100)
    assessment_type = models.CharField(max_length=50)
    assessment_weight = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    assessment_duration = models.PositiveSmallIntegerField()
    assessment_hand_out = models.CharField(choices=HAND_OUT_IN_OPTIONS, max_length=15)
    assessment_hand_in = models.CharField(choices=HAND_OUT_IN_OPTIONS, max_length=15)
    assessment_semester = models.CharField(choices=SEMESTER_OPTIONS, max_length=15)
    learning_outcomes_covered = models.CharField(max_length=500)
    module_code = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "Assessment for {}".format(self.module_code)