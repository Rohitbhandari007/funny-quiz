import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.core import serializers
from channels.db import database_sync_to_async
import random

from .utils import QuestionFunction, QuestionCheck, QuestionConfirm


#some global code


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

        if request_type=='answer':
            user_answer = text_data_json['user_answer']
            user_name = text_data_json['user_name']

            

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'answer_data',
                    'user_answer':user_answer,
                    'user_name':user_name
                    
                    
                }
            )
        if request_type=='next':
                
            user_name=text_data_json['user_name']
            pattern=text_data_json['pattern']
            qid=text_data_json['qid']
            


            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'next_question',
                    'user_name':user_name,
                    'pattern':pattern,
                    'qid':qid
                            
                
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

    def get_random_question(self):
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

        
        return single_question, question_id, answers,pattern

    

    def get_next_question(self):
        
       
        quiz = Quiz.objects.filter(id=1)
        questions = Question.objects.filter(quiz__in=quiz)
  

        

        return questions

    async def quiz_info(self, event):
        quiz = await database_sync_to_async(self.get_data_models)()
        q = await database_sync_to_async(self.get_random_question)()
        quest = q[0]
        qid=q[1]
        ans = q[2]
        pattern = q[3]
        

        # questions = Question.objects.filter(quiz__in=quiz)
        # answers = Answer.objects.filter(question__in=questions)

        await self.send(text_data=json.dumps({
            'info' :'quiz',
            'msg':'hello',
            'quizname': quiz,
            'question':quest,
            'answer':ans,
            'pattern':pattern,
            'qid':qid,
            
        }))
    
    async def answer_data(self, event):

        user_name = event['user_name']

        await self.send(text_data=json.dumps({
            'info':'answer',
            'message':'correct answer',
            'user_name': user_name
        }))
    

    async def next_question(self, event):
        questions =  await database_sync_to_async(self.get_next_question)()
        pattern=event['pattern']
        arr = pattern
        print(arr)
        qid=event['qid']




        print(qid, pattern)

        for x in arr:
            print (x)
            # if arr[x] == qid:
            #     print('false')
            # return 'never gonna happen'

        
        # if qid in arr:
        #     for x in arr:
        #         print(x)

        # # question = q_obj

        
        # for x in pattern:
        #     q_obj=questions[x]
        
        # new_quest = q_obj

        # print(new_quest)

        

     
        user_name = event['user_name']
        await self.send(text_data=json.dumps({
            'info':'next',
            'message': 'this is next quest',
            'user_name':user_name,
            'pattern':pattern
            
        }))