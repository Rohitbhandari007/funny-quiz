from django.db import models



class Room(models.Model):
    room_name = models.CharField(max_length=200)


class Quiz(models.Model):
    name = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()


    def __str__(self):
        return f"{self.name}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quizes'


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"