import asyncio
import json
from abc import ABC, abstractmethod

import websockets  # websockets パッケージをインポート
from model import FXModel  # model.pyからimport
from views import AccountView, BaseView, OrderView, RateView  # views.pyからimport


class FXClientFactory(ABC):
    @abstractmethod
    def create_client(self):
        pass


class WebSocketClientFactory(FXClientFactory):
    def create_client(self):
        return WebSocketClient("ws://example.com")


class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.callback = None

    async def connect(self):
        async with websockets.connect(self.url) as ws:
            while True:
                data = await ws.recv()
                message = json.loads(data)
                if self.callback:
                    self.callback(message)


class FXController:
    def __init__(self, model, client_factory):
        self.model = model
        self.client_factory = client_factory
        self.ws_client = self.client_factory.create_client()
        self.ws_client.callback = self.on_message  # set callback
        self.views = []

    def on_message(self, message):
        self.model.update(message)
        self.update_all_views()

    def add_view(self, view):
        if isinstance(view, BaseView):
            self.views.append(view)

    def update_all_views(self):
        data = self.model.export_to_dict()
        for view in self.views:
            view.update_view(data)

    async def run(self):
        await self.ws_client.connect()
        self.update_all_views()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    fx_model = FXModel()
    controller = FXController(fx_model, WebSocketClientFactory())
    controller.add_view(RateView())
    controller.add_view(AccountView())
    controller.add_view(OrderView())
    loop.run_until_complete(controller.run())
