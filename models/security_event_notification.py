from ocpp.v16.enums import Action

from models.base import BaseEvent


class SecurityEventNotificationEvent(BaseEvent):
    action: Action = Action.SecurityEventNotification
