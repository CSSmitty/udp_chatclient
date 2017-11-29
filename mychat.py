from Queue import Queue, Empty
from threading import Thread
from time import sleep
import sys, socket, errno

MYPORT = int(sys.argv[1])
THEIRIP = sys.argv[2]
THEIRPORT = int(sys.argv[3])
BUFLEN = 1000

class Receiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print "Cannot open socket"
            sys.exit(1)

        try:
            s.bind(('',MYPORT))
        except:
            print "Cannot bind my socket to port"
            sys.exit(1)

        while True:
            try:
                data, addr = s.recvfrom(BUFLEN)
            except OSError as err:
                print "Cannot receive from socket: {}".format(err.strerror)
            print "Received Message"
            self.queue.put(data)


def main():
    queue = Queue()
    r = Receiver(queue)
    r.daemon = True
    r.start()

    print 'p - prints received messages \ns <msg> - sends message \nq-quits\n'
    cmd = raw_input('& ')
    while cmd[0] is not 'q':
        if cmd[0] is 'p':
            try:
                while True:
                    msg = queue.get(False, None)
                    print(msg)
            except:
                print('---')

        if cmd[0] is 's':
            message = ''
            for char in range(2, len(cmd)):
                message += cmd[char]
            send_message(message)

        cmd = raw_input('& ')

    print('So long partner')


def send_message(message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print "Cannot open socket"
        sys.exit(1)

    try:
        s.sendto(message, (THEIRIP, THEIRPORT))
    except OSError as err:
        print "Cannot send: {}".format(err.strerror)
        sys.exit(1)


main()