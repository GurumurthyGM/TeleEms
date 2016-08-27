__author__ = "Gurumurthy"

import sys
import time
import urllib
import urllib2

import telepot

server_ip = '0'
past_time = time.time()
present_time = time.time()


def timer(t2, t1):
    if t2 - t1 > 10:
        global server_ip
        server_ip = '0'


def serverlist():
    f = open('servers.txt', 'r+')
    lists = f.read().strip()
    f.close()
    lists = lists.split('\n')
    slen = len(lists)
    keys = [[''] for i in range(slen)]
    for i in range(slen):
        keys[i][0] = lists[i].strip()
    return keys


def server_access(ip, command):
    ip = ip
    cmd = command
    url = "http://" + ip + "/cgi-bin/py.cgi"
    q_args = {'cmd': cmd}
    data = urllib.urlencode(q_args)
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req).read()
    resp1 = resp.replace('\t', '->')
    print resp1
    return resp1


def handle(msg):
    global present_time, past_time, server_ip
    present_time = time.time()
    timer(present_time, past_time)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    keys = serverlist()
    kb = {'keyboard': keys, 'one_time_keyboard': True}

    if content_type == 'text':
        txt = msg['text']
        if txt == '/start':
            resp1 = server_access('192.168.3.204', txt)
            bot.sendMessage(chat_id, resp1 + str(server_ip), reply_markup=kb)
            server_ip = txt
        else:
            bot.sendMessage(chat_id, 'Please Enter Commands only', reply_markup=kb)

    past_time = present_time


TOKEN = '217271588:AAGniXAC780j3FSkPu_mzIeKE9-G0iSLSKo'  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
