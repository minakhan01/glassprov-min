import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse
import time
import subprocess
import datetime

client_name = ""
current_time = datetime.datetime.today()
last_fire_time = datetime.datetime.today()
refire_threshold = datetime.timedelta(seconds=3)
adb = "adb"
yes_list = [adb, 'shell', 'input', 'touchscreen', 'swipe', '200', '500', '500', '500', '300']
no_list = [adb, 'shell', 'input', 'touchscreen', 'swipe', '500', '500', '200', '500', '300']
back_button_list = [adb, 'shell', 'input', 'keyevent', '4']

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse(callback, parser)

def periodic_send(ws):
    #TODO(scottgwald): catch dead websocket
    # ws.send('blob', 'theMessage34234', 'fromOneToTheOther')
    ws.send('android:glass:f88fca2619bd', 'To: the charcoal glass. Love, ' + client_name);
    ws.send('android:glass:f88fca25588b', 'To: the sky glass. Love, ' + client_name);
    ws.send('android:glass:f88fca26183f', 'To: the cotton glass. Love, ' + client_name);
    ws.send('android:glass:f88fca26273d', 'To: the shale glass. Love, ' + client_name);
    ws.send('android:glass:f88fca2627c1', 'To: shale2. Love, ' + client_name);
    gevent.spawn_later(5, periodic_send, ws)

def callback(ws, **kw):
    global client_name

    def get_ping(chan, resultChan, timestamp):
        print "Got ping %5f" % timestamp
        ws.send(resultChan, time.time());
        # ws.publish(resultChan, timestamp, time.time(), ws.group_device)

    def registered(chan, name):
        global client_name
        print "I'm registered as: " + name
        client_name = name

    def get_blob(chan, title, body):
        print "Got blob %s %s" % (title,body)

    def tinder_cb(chan, arg):
        global last_fire_time
        print "Got tinder gesture " + arg
        current_time = datetime.datetime.today()
        if current_time - last_fire_time > refire_threshold:
            print "Firing " + arg
            last_fire_time = datetime.datetime.today()
            if arg == 'yes':
                subprocess.Popen(yes_list)
            elif arg == 'no':
                subprocess.Popen(no_list)
            elif arg == 'back':
                subprocess.Popen(back_button_list)
        else: 
            print "Not firing because previous event was too recent, time"

    client_name = "%.6f" % time.time()
    print "Client ws callback, trying to register as " + client_name
    # ws.subscribe('ping', get_ping)
    ws.subscribe('registered', registered)
    ws.subscribe('blob', get_blob)
    ws.subscribe('tinderGestures', tinder_cb)
    ws.subscribe('tinderYes', tinder_cb)
    ws.send('register', 'registered', client_name)
    gevent.spawn_later(5, periodic_send, ws)
    ws.handler_loop()

if __name__ == '__main__':
    serverThread = gevent.spawn(ws_parse, argparse.ArgumentParser())
    print "And I made it past"
    gevent.joinall([serverThread])

# wearscript.parse(callback, argparse.ArgumentParser())
