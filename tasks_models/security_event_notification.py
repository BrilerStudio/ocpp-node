from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class SecurityEventNotificationTask(BaseTask):
    action: Action = Action.SecurityEventNotification
