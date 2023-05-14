from .comms import *
from .Playersinfo import *
import time
from pprint import pprint


class Simple_Comms():


    def __init__(self):

        self.commsSender, self.commsListener, self.player = self._initialize_messanger(game='game-04')

        self.listen()

        self.message = {}


    #
    #  Description:
    #
    #        Starts the listener for the server
    #
    def listen(self):
        self.commsListener.bindKeysToQueue([f"#.{self.player}.#", "#.broadcast.#"])
        self.commsListener.threadedListen(self.callback)


    #
    #  Description:
    #
    #        Starts the listener for the server
    #
    def send(self, message):
        self.commsSender.send('broadcast', json.dumps({"data": message}), False)


    def callback(self, ch, method, properties, body):
        """This method gets run when a message is received. You can alter it to
        do whatever is necessary.
        """
        self.commsListener._messageQueue[self.commsListener.user].append(f"{method.routing_key} : {body}")

        # change the message from a string back into json object
        json_body = json.loads(body)

        # print('printing player')
        # print(json_body)

        # only save the message if it's not from the player that sent it
        if self.player != json_body['from']:
            self.message[json_body['from']] = json_body['data']




    def _initialize_messanger(self, **kwargs):

        player = kwargs.get("player", None)
        game = kwargs.get("game", 'game-08')                    # GOES TO GAME 8


        queues = []
        for i in range(1, 10):
            i += 1
            if i < 10:
                q = "0" + str(i)
            queues.append("game-" + q)
        users = []
        for i in range(1, 25):
            if i < 10:
                p = "0" + str(i)
            users.append("player-" + p)

        # no player arg was given
        if not player:
            # shuffle the users list
            random.shuffle(users)

            # seeing which players in the server are used 
            used_players = get_used_players()
            player = random.choice(users)
            while player in used_players:
                player = random.choice(users)
            

        creds = {
            "exchange": game,
            "port": "5672",
            "host": "terrywgriffin.com",
            "user": player,
            "password": player + "2023!!!!!",  # user.capitalize() * 3,
        }

        commsSender = CommsSender(**creds)
        commsListener = CommsListener(**creds)

        return commsSender, commsListener, player

