from django import template
from audit.models import DesignAnswer

register = template.Library()

@register.filter(name='get_answer_for_question')
def get_answer_for_question(answers, question_id):
    """Returns the answer for a given question ID."""
    try:
        answer = answers.filter(question_id=question_id).first()
        return answer.answer if answer else None
    except DesignAnswer.DoesNotExist:
        return None

@register.filter(name='get_explanation_for_question')
def get_explanation_for_question(answers, question_id):
    """Returns the explanation for a given question ID."""
    try:
        answer = answers.filter(question_id=question_id).first()
        return answer.explanation if answer else None
    except DesignAnswer.DoesNotExist:
        return None
    

