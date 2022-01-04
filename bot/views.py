from django.shortcuts import render
import json
import os
import requests
from django.http import JsonResponse, response
from django.views import View
from .models import TodoItem
TELEGRAM_URL = "https://api.telegram.org/bot"
TELEGRAM_BOT_TOKEN = "5032541894:AAEGzR8qEreVX2MvJGcfAl8ZUrJDSBqDDrY"


class BotView(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        t_message = t_data["message"]
        t_chat = t_message['chat']
        print(t_data)
        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            print(e) # TODO: remove after testing
            return JsonResponse({'ok': "POST request processed"})

        text = text.lstrip("/")
        print(text)
        if text == 'start':
            self.send_message("Welcome to TodoBot!\nTo add a todo just simply type it in.\nFor example, 'Finish the homework'.", t_chat['id'])
        if not text == '':
            if text!= 'all' and text!='start':
                if text!= 'remove':                
                    chat = TodoItem(todo_text = text, chat_id = t_chat['id'])
                    chat.save()
                    self.send_message('Done ' + '\U00002714' ,t_chat['id'])
        
        if text == 'remove':
            content = self.all_items()
            self.send_message(f"Which todo do you want to remove?\nProvide an id of a todo.\n\n{content}", t_chat['id'])
        
        if text == 'all':
            content = self.all_items()
            self.send_message(f"{content}", t_chat['id'])
        
        if type(int(text)) == 'int':
            print(type(text))
            todo = TodoItem.objects.filter(id=int(text)).delete()
            todo.save()
            self.send_message('Done ' + '\U00002714' ,t_chat['id'])
        return JsonResponse({"ok": "POST request processed"})
    
    
    @staticmethod
    def all_items():
        todos = TodoItem.objects.all()
        text = []
        for i in todos:
            text.append(f"{i.id}, {i.todo_text}")
        text_string = '\n'.join(text)
        return text_string

    @staticmethod
    def send_message(message, chat_id):
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
        response = requests.post(f'{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage', data = data)

    # {'update_id': 541295583,
    #  'message': {'message_id': 2, 'from': {'id': 67706481, 'is_bot': False, 'first_name': 'M.S.', 'username': 'e_Brain', 'language_code': 'en'},
    #  'chat': {'id': 67706481, 'first_name': 'M.S.', 'username': 'e_Brain', 'type': 'private'}, 'date': 1640434536, 'text': '+'}}
    
    
    #https://api.telegram.org/bot5032541894:AAEGzR8qEreVX2MvJGcfAl8ZUrJDSBqDDrY/setWebhook?url=https://todobot99.herokuapp.com/webhooks/bot/
