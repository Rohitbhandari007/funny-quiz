import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.core import serializers


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

 # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name

        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

       # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':user,
                
            }
        )

      

     


    def chat_message(self, event):
        message = event['message']
        user = event['user']

        

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user':user,
            

        }))

    def quiz_info(self, event):
        quiz = Quiz.objects.filter(id=1)
        quizname = quiz[0].name
        questions = Question.objects.filter(quiz__in=quiz)
        answers = Answer.objects.filter(question__in=questions)

        self.send(text_data=json.dumps({
            'quiz': quizname,
            'msg':'hello',
            
        }))