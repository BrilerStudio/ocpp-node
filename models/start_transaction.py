from ocpp.v16.enums import Action

from models.base import BaseEvent
from ocpp.v16.call import StartTransactionPayload


class StartTransactionEvent(BaseEvent):
    action: Action = Action.StartTransaction
    payload: StartTransactionPayload
    transaction_id: int | None = None
