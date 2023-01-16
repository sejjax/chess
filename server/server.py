import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while :
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")

ROUTES = {
    'waiting_room': {
        'enter',
        'exit',
        'list_waiting_peers',
        'invite_to_game'
    },
    'game': {
        'start',
        'surrander',
        'do_step',
        'get_state'
    }
}

class Request:
    method: str
    body: str


class Server:
    def __init__(self):
        pass

    def run(self):
        pass


class WaitingRoom:
    def __init__(self):
        self.peers = []

    def add_peer(self, peer):
        self.peers.append(peer)

class InvitesBus:
    pass


class ServerController:
    def enter_waiting_room(self):
        pass

    def exit_waiting_room(self):
        pass

    def list_waiting_peers(self):

    def invite_to_game(self):
        pass

    def start_game(self):
        pass

    def do_step(self):
        pass

    def get_game_state(self):
        pass

    def surrunder(self):
        pass