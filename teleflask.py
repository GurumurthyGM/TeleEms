#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from flask import Flask, redirect, url_for, request

botapi = '217271588:AAGniXAC780j3FSkPu_mzIeKE9-G0iSLSKo' #<Token>

updater = Updater(token=botapi)
dispatcher = updater.dispatcher

global bot
bot = telegram.Bot(token=botapi)

app = Flask(__name__)

#HTTP API http://ip:5000/teleflask?text=<msg>&id=<groupid/userid>
@app.route('/teleflask',methods = ['GET'])
def teleflask():
	text = request.args.get('text')
	chat_id = request.args.get('id')
	try:
		text = text.encode('utf-8')
		txt=text.replace(',','\n')
		txt=txt.replace('false','\xF0\x9F\x94\xB4')
		text=txt.replace('true','\xE2\x9C\x85')
		keyboard = [[InlineKeyboardButton("UnAck", callback_data='1')]]
		reply_markup = InlineKeyboardMarkup(keyboard)
		bot.sendMessage(chat_id=chat_id, text=text, reply_markup=reply_markup)
	except Exception as err:
		print err
	return 'ok'

def button(bot, update):
	try:
		query = update.callback_query
		if query.data == '1':
			ack = "Ack-By-" + update.callback_query.from_user.first_name
			keyboard = [[InlineKeyboardButton(ack, callback_data='0')]]
			reply_markup = InlineKeyboardMarkup(keyboard)
		else :
			keyboard = [[InlineKeyboardButton('UnAck', callback_data='1')]]
			reply_markup = InlineKeyboardMarkup(keyboard)
		bot.editMessageReplyMarkup(chat_id=query.message.chat_id, message_id = query.message.message_id, reply_markup=reply_markup)

	except Exception as err:
		print err

def main():

	button_handler = CallbackQueryHandler(button)
	dispatcher.add_handler(button_handler)

	updater.start_polling()

	app.run(debug = True)

if __name__ == '__main__':
	main()
