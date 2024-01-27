from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class StatusNotificationTask(BaseTask):
    action: Action = Action.StatusNotification
