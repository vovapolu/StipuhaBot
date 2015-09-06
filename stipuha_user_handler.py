
# -*- coding: utf-8 -*-

import telegram
import logging
from stipuha_user import *
from stipuha_messages import *

class StipuhaUserHandler:

    def __init__(self, bot, user_id):
        self.bot = bot
        self.user_id = user_id
        self.user = StipuhaUser.get_user_by_id(self.user_id)

    def handle_stipuha_amount(self, stipuha_message):
        try:
            stipuha = int(stipuha_message)
            self.user.set_stipuha(stipuha)
            self.user.set_state(StipuhaUser.WITH_STIPUHA)
            self.bot.sendMessage(chat_id=self.user_id, text='Я все понял, студент.')
            self.get_stipuha()
        except ValueError:
            logging.warn("{} is not a number.".format(stipuha_message))
            self.get_stipuha_amount()

    def get_stipuha_amount(self):
        self.bot.sendMessage(chat_id=self.user_id, text='Напиши-ка свою стипуху в рублях (одно число).')
        self.user.set_state(StipuhaUser.GETTING_STIPUHA)

    def get_stipuha(self):
        if self.user.get_state() != StipuhaUser.WITH_STIPUHA:
            self.bot.sendMessage(chat_id=self.user_id,
                                 text='Воу. Воу. Сначала укажи свою стипуху.')
        else:
            self.bot.sendMessage(chat_id=self.user_id,
                                 text=StipuhaMessages.generate_stipuha_message(self.user.get_stipuha()))

    def get_help(self):
        self.bot.sendMessage(chat_id=self.user_id,
                             text="Этот бот показывает твою стипуху в долларах и то, что ты можешь купить на нее.\n\n" +
                                  "/setstipuha - указать стипуху\n" +
                                  "/stipuha - показать стипуху")

    commands = {"/setstipuha": get_stipuha_amount,
                "/stipuha": get_stipuha,
                "/help": get_help}
    next_handlers = {StipuhaUser.INIT: None,
                     StipuhaUser.GETTING_STIPUHA: handle_stipuha_amount,
                     StipuhaUser.WITH_STIPUHA: None}

    def receive_message(self, message):
        if message in StipuhaUserHandler.commands:
            StipuhaUserHandler.commands[message](self)
        else:
            if StipuhaUserHandler.next_handlers[self.user.get_state()] is not None:
                StipuhaUserHandler.next_handlers[self.user.get_state()](self, message)
            else:
                logging.warn('"{}" message is skipped'.format(message))
