import asyncio


class Player:
    def __init__(self, name, server):
        self.server = server
        self.name = name

    def do_some(self, data):
        self.server.queue.put_nowait(self.name + ' ' + data)


class Server:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.players: list[Player] = [Player('_', self) for _ in range(2)]

    def start(self):
        asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            data = await self.queue.get()
            print(data)
            self.queue.task_done()

    def send(self, data):
        self.queue.put_nowait(data)

    def get_players(self):
        return self.players


async def main():
    # fire up the both producers and consumers
    server = Server()
    server.start()
    one, two = server.get_players()
    one.do_some('One')
    two.do_some('Two')


asyncio.run(main())
