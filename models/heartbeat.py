from ocpp.v16.enums import Action

from models.base import BaseEvent


class HeartbeatEvent(BaseEvent):
    action: Action = Action.Heartbeat
