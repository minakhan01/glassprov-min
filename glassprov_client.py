import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse
import time

client_name = ""

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

    client_name = "%.6f" % time.time()
    print "Client ws callback, trying to register as " + client_name
    # ws.subscribe('ping', get_ping)
    ws.subscribe('registered', registered)
    ws.subscribe('blob', get_blob)
    ws.send('register', 'registered', client_name)
    gevent.spawn_later(5, periodic_send, ws)
    ws.handler_loop()

if __name__ == '__main__':
    serverThread = gevent.spawn(ws_parse, argparse.ArgumentParser())
    print "And I made it past"
    gevent.joinall([serverThread])

# wearscript.parse(callback, argparse.ArgumentParser())
