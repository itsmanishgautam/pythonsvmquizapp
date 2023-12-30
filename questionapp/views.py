from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question,UserQuestionAttempt,TestAttempt,Test
from .serializers import QuestionSerializer
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def questionPage(request):
    context = {}
    return render(request,'questionapp/questionpage.html',context)


class GetQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, test_id):
        user = request.user
        test_attempt, created = TestAttempt.objects.get_or_create(user=user,completed=False)
        # Get the list of questions already answered by the user for the given test
        answered_questions_ids = UserQuestionAttempt.objects.filter(
            user=user,
            test_attempt=test_attempt
        ).values_list('question_id', flat=True)

        # Get the next random unanswered question for the user
        test = Test.objects.get(id=test_id)
        
        # next_question = Question.objects.filter(
        #     test_id=test_id
        # ).exclude(
        next_question = test.questions.all().exclude(
            id__in=answered_questions_ids
        ).order_by('?').first()  # Randomly select one unanswered question

        serializer = QuestionSerializer(next_question)
        data = {
            'attempt_id':test_attempt.id,
            'question':serializer.data
        }
        return Response(data)


class QuestionSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.data)
        userattempt = UserQuestionAttempt(user = request.user,test_attempt_id=request.data['test_attempt_id'],question_id=request.data['question'],answer_id=request.data.get('answer'),time_taken=request.data.get('timetaken'),right_attempt=request.data.get('right_attempt'))
        userattempt.save()

        return Response({'status':'ok'})

