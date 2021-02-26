from twisted.internet import protocol, reactor
import names

COLORS = [
    '\033[31m',
    '\033[32m',
    '\033[33m',
    '\033[34m',
    '\033[35m',
    '\033[36m',
    '\033[37m',
    '\033[4m'
]


transports = set()  # variables for saving clients
users = set()  # variables for saving users


class Chat(protocol.Protocol):
    # print user connected
    def connectionMade(self):
        name = names.get_first_name()  # make random name
        color = COLORS[len(users) % len(COLORS)]
        users.add(name)
        transports.add(self.transport)  # if user connected, add client

        # string to bytes encoding
        self.transport.write(f'{color}{name}\033[0m'.encode())

    # print User message
    def dataReceived(self, data):
        for t in transports:  # loop for all clients
            if self.transport is not t:  # if messages not mine, transport messages
                t.write(data)

        print(data.decode('utf-8'))  # for Hanguel


class ChatFactory(protocol.Factory):
    # Define chatting protocol
    def buildProtocol(self, addr):
        return Chat()


print('Server started!')
# TCP 8000 port listen
reactor.listenTCP(8000, ChatFactory())
reactor.run()
