import asyncio
import json

import websockets


# Model: データとビジネスロジックを処理
class FXModel:
    def __init__(self):
        self.data = None

    def update_data(self, new_data):
        self.data = new_data


# View: ユーザーにデータを表示
class FXView:
    def display(self, data):
        print(f"Displaying data: {data}")


# Controller: ModelとViewをつなぐ
class FXController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_view(self):
        self.view.display(self.model.data)


# WebSocketClient: Websocket通信のためのクラス
class WebSocketClient:
    def __init__(self, uri, custom_handler=None):
        self.uri = uri
        self.custom_handler = custom_handler

    async def connect(self):
        async with websockets.connect(self.uri) as ws:
            while True:
                message = await ws.recv()
                self.handle_message(message)

    def handle_message(self, message):
        data = json.loads(message)
        if self.custom_handler:
            self.custom_handler(data)


# カスタムのデータ処理関数
def custom_data_handler(data):
    print(f"Custom handler received: {data}")


# エントリーポイント
if __name__ == "__main__":
    model = FXModel()
    view = FXView()
    controller = FXController(model, view)

    # Websocket URIとカスタムハンドラーを設定
    ws_client = WebSocketClient("wss://example.com/websocket", custom_data_handler)

    # Websocket通信を開始
    asyncio.get_event_loop().run_until_complete(ws_client.connect())
