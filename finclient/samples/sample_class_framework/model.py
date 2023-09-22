import json
from abc import ABC, abstractmethod


class FinClientModel(ABC):
    @abstractmethod
    def validate_update_data(self, data):
        pass

    def update(self, data):
        if self.validate_update_data(data):
            vars(self).update(data)

    def export_to_dict(self):
        return vars(self)

    def import_from_dict(self, data):
        if self.validate_update_data(data):
            vars(self).update(data)


class FXRate(FinClientModel):
    def validate_update_data(self, data):
        return "rate" in data


class FXOrder(FinClientModel):
    def validate_update_data(self, data):
        return "order_id" in data


class FXAccount(FinClientModel):
    def validate_update_data(self, data):
        return "balance" in data


class FXModel:
    def __init__(self):
        self.sub_models = {
            "rates": FXRate(),
            "orders": FXOrder(),
            "account": FXAccount(),
        }

    def update(self, message_type, data):
        if message_type in self.sub_models:
            self.sub_models[message_type].update(data)

    def export_to_dict(self):
        return {
            key: sub_model.export_to_dict()
            for key, sub_model in self.sub_models.items()
        }

    def import_from_dict(self, import_data):
        for key, data in import_data.items():
            if key in self.sub_models:
                self.sub_models[key].import_from_dict(data)
