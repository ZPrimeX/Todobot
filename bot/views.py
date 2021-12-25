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

        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            print(e) # TODO: remove after testing
            return JsonResponse({'ok': "POST request processed"})


        text = text.lstrip("/")
        if text == '+':
            chat = TodoItem(todo_text = text, chat_id = t_chat['id'])
            chat.save()
            self.send_message(chat.todo_text, t_chat['id'])

    @staticmethod
    def send_message(message, chat_id):
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
        response = requests.post(f'{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage', data = data)

    # {'update_id': 541295583,
    #  'message': {'message_id': 2, 'from': {'id': 67706481, 'is_bot': False, 'first_name': 'M.S.', 'username': 'e_Brain', 'language_code': 'en'},
    #  'chat': {'id': 67706481, 'first_name': 'M.S.', 'username': 'e_Brain', 'type': 'private'}, 'date': 1640434536, 'text': '+'}}