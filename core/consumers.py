import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import *
from django.core import serializers
from channels.db import database_sync_to_async
import random



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
        a_obj = Answer.objects.all()

        q_arr = []
        qids = []
        q_obj=[]


        ans_arr=[]
        ans_correct=[]

        #getting all answers 
        new_ans_arr =[]
        new_ans_parent = []
        new_ans_correct = []
        new_ans_arr_obj=[]

        for ans in a_obj:
            new_ans_arr.append(ans.text)
            new_ans_parent.append(ans.question)
            new_ans_correct.append(ans.correct)
            new_ans_arr_obj.append(ans)

            


        q_n = []
        a=0
        for x in questions:
            a=a+1
            q_arr.append(x.text)
            qids.append(x.id)
            q_obj.append(x)
            question = x
            
            answers = Answer.objects.filter(question=question)

        for answer in answers:
            ans_arr.append(answer.text)
            ans_correct.append(answer.correct)
            q_n.append(answer.question)
        
        ans_new_dict = dict(zip(ans_arr, ans_correct))
  
        return q_obj, q_arr, qids, ans_new_dict, q_n, new_ans_arr_obj


    def get_answer_next(self):
        answers = Answer.objects.all()
        nice = 0

        return answers, nice

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
        q_objects =  await database_sync_to_async(self.get_next_question)()
        pattern=event['pattern']
        qid=event['qid']

        p=pattern.replace(',','')
        p = list(p)
        
        objs=q_objects[0]

        
        if qid in p:
            p.remove(qid)
            for x in p:
                x=int(x)
                q_obj = objs[x]
                q_name= objs[x].text
                q_id=objs[x].id
            
        for q_id in p:
            q_id =q_id

        
        print(q_id)
        q_name = objs[int(q_id)].text
        q_obj = objs[int(q_id)]


        new_ans_obj = q_objects[5]


        new_ans_text = []
        new_ans_correct = []

        for ans_obj in new_ans_obj:
            
            ans_parent = ans_obj.question

            if ans_parent == q_obj:
                new_ans_text.append(ans_obj.text)
                new_ans_correct.append(ans_obj.correct)
        
                ans_new_dict = dict(zip(new_ans_text, new_ans_correct))


        
        print(q_name)
        print(ans_new_dict)
     
        user_name = event['user_name']
        await self.send(text_data=json.dumps({
            'info':'next',
            'message': 'this is next quest',
            'user_name':user_name,
            'pattern':pattern,
            'new_pattern':p,
            'q_name':q_name,
            'q_id':q_id,
            'answers':ans_new_dict,
            
        }))