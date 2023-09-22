from abc import ABC, abstractmethod


class BaseView(ABC):
    @abstractmethod
    def update_view(self, data):
        pass


class RateView(BaseView):
    def update_view(self, data):
        print(f"Latest Rate: {data['rate']}")


class AccountView(BaseView):
    def update_view(self, data):
        print(f"Account Balance: {data['balance']}")


class OrderView(BaseView):
    def update_view(self, data):
        print(f"Order ID: {data['order_id']}")
