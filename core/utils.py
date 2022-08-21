from .models import Quiz, Answer, Question
import random, json


quiz = Quiz.objects.filter(id=1)
questions = Question.objects.filter(quiz__in=quiz)
q_count = questions.count()

anss=[]
correct=[]
all_random_questions = []

        
pattern = random.sample(range(0, q_count), q_count)
for x in pattern:
    single_question= questions[x].text
    question_id = questions[x].id
    question_obj = questions[x]
    all_random_questions.append(question_obj)
for answer in Answer.objects.filter(question=question_obj):
    anss.append(answer.text)
    correct.append(answer.correct)

        
ans_dict = dict(zip(anss, correct))
answers = json.dumps(ans_dict)

print(question_obj)

def QuestionFunction():

    quiz = Quiz.objects.filter(id=1)
    questions = Question.objects.filter(quiz__in=quiz)
    q_count = questions.count()

#craeting array for answers and cirrect
    anss=[]
    correct=[]

        
    pattern = random.sample(range(0, q_count), q_count)
    for x in pattern:
        single_question= questions[x].text
        question_id = questions[x].id
        question_obj = questions[x]
     

    for answer in Answer.objects.filter(question=question_obj):
        anss.append(answer.text)
        correct.append(answer.correct)

        
    ans_dict = dict(zip(anss, correct))
    answers = json.dumps(ans_dict)

        
    return single_question, question_id, answers, question_obj



def QuestionCheck():
    quiz = Quiz.objects.filter(id=1)
    questions = Question.objects.filter(quiz__in=quiz)


    # rand_question = QuestionFunction()
    # question_obj= rand_question[3]
    
    # validation_array=[question_obj]

    # print(question_obj)
    # validation_array.append(question_obj)

    # print(validation_array)

    q = all_random_questions

    for x in all_random_questions:
        x = x
    
    

    qonly = x
    a = answers
    print(qonly, answers)



    return 'working'



def QuestionConfirm():
    checked_q = QuestionCheck()

    return 'go'