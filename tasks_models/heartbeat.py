from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class HeartbeatTask(BaseTask):
    current_time: str
    action: Action = Action.Heartbeat
