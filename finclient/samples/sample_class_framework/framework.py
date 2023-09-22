import asyncio
import json
from abc import ABC, abstractmethod

import websockets


# WebSocketObserver Interface
class WebSocketObserver(ABC):
    @abstractmethod
    def on_message(self, message):
        pass


# WebSocket Client
class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    async def connect(self):
        async with websockets.connect(self.uri) as ws:
            while True:
                message = await ws.recv()
                self.notify_all(message)

    def notify_all(self, message):
        for observer in self.observers:
            observer.on_message(message)


# WebSocketClientFactory
class WebSocketClientFactory:
    def create_client(self, uri):
        return WebSocketClient(uri)


# FXModel
class FXModel:
    def __init__(self):
        self.rates = {}
        self.orders = {}
        self.account_status = {}

    def update_rates(self, new_rates):
        self.rates.update(new_rates)

    def update_orders(self, new_orders):
        self.orders.update(new_orders)

    async def update_account_status(self):
        while True:
            # Simulate an API call to get account status
            await asyncio.sleep(5)
            self.account_status = {"balance": 1000}  # Dummy data


# FXView Interface
class FXView(ABC):
    @abstractmethod
    def display(self, data):
        pass


# FXRateView
class FXRateView(FXView):
    def display(self, rates):
        print("FX Rates:", rates)


# FXOrderView
class FXOrderView(FXView):
    def display(self, orders):
        print("FX Orders:", orders)


# FXAccountView
class FXAccountView(FXView):
    def display(self, account_status):
        print("Account Status:", account_status)


# FXController
class FXController(WebSocketObserver):
    def __init__(self, model, ws_uri, client_factory):
        self.model = model
        self.views = []
        self.ws_client = client_factory.create_client(ws_uri)
        self.ws_client.add_observer(self)

    def on_message(self, message):
        data = json.loads(message)
        if data.get("type") == "rate":
            self.model.update_rates(data["content"])
        elif data.get("type") == "order":
            self.model.update_orders(data["content"])
        self.update_view()

    def add_view(self, view):
        self.views.append(view)

    def update_view(self):
        for view in self.views:
            if isinstance(view, FXRateView):
                view.display(self.model.rates)
            elif isinstance(view, FXOrderView):
                view.display(self.model.orders)
            elif isinstance(view, FXAccountView):
                view.display(self.model.account_status)

    async def start(self):
        await asyncio.gather(
            self.ws_client.connect(), self.model.update_account_status()
        )


if __name__ == "__main__":
    model = FXModel()
    client_factory = WebSocketClientFactory()
    controller = FXController(model, "wss://example.com/fx_ticker", client_factory)

    rate_view = FXRateView()
    order_view = FXOrderView()
    account_view = FXAccountView()

    controller.add_view(rate_view)
    controller.add_view(order_view)
    controller.add_view(account_view)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(controller.start())
