import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.core import serializers
from channels.db import database_sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name


 # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name

        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        request_type = text_data_json.get('request_type', None)

        print(request_type)

    #    Send message to room group
        if request_type=='chat':
            message = text_data_json['message']
            user = text_data_json['user']
            command = text_data_json['command']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user':user,
                    'command':command
                    
                    
                }
            )

        #send command ok    
        if request_type=='quiz':
            newmsg = text_data_json['newmsg']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'quiz_info',
                    'newmsg':newmsg
                    
                    
                }
            )


    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        command = event['command']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'info' :'chat',
            'user':user,
            'command':command
            

        }))

    def get_data_models(self):
        quiz = Quiz.objects.filter(id=1)
        quizname = quiz[0].name
        return quizname

    def get_questions(self):
        quiz = Quiz.objects.filter(id=1)
        questions = Question.objects.filter(quiz__in=quiz)
        single_question= questions[0].text
        return single_question
    
    def get_answers(self):
        quiz = Quiz.objects.filter(id=1)
        questions = Question.objects.filter(quiz__in=quiz).values()
        quest = Question.objects.get(id=1)
        print(quest)
        answer = Answer.objects.filter(question=quest)
        
        return "answer"
    
    def get_ans(self):
        quest = Question.objects.get(id=1)

        anss = []
        correct=[]

        for answer in Answer.objects.filter(question=quest):
            # answers.update['text'] = answer.text
            anss.append(answer.text)
            correct.append(answer.correct)
            # answer['correct'] = answer.correct

        # self.get_ans = [
        #     {
        #         'one':x.text,
        #         'two':x.text,
        #         'three':x.text,
        #         'four':x.text
        #     }
        #     for x in Answer.objects.filter(question=quest)
        # ]

        print(anss)

        ans_dict = dict(zip(anss, correct))
        answers = json.dumps(ans_dict)
        return answers

    async def quiz_info(self, event):
        quiz = await database_sync_to_async(self.get_data_models)()
        question = await database_sync_to_async(self.get_questions)()
        answer = await database_sync_to_async(self.get_ans)()
        
        # questions = Question.objects.filter(quiz__in=quiz)
        # answers = Answer.objects.filter(question__in=questions)

        await self.send(text_data=json.dumps({
            'info' :'quiz',
            'msg':'hello',
            'quizname': quiz,
            'question':question,
            'answer':answer
            
        }))