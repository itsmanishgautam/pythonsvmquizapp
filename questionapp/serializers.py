from .models import Answer,Question,TestAttempt,UserQuestionAttempt
from rest_framework import serializers


class RightAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
         'answer',
         'is_right'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    answers = RightAnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = [
            'id',
            'question','answers'

        ]