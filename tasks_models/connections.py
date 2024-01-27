from core.fields import ConnectionStatus
from tasks_models.base import BaseTask


class DisconnectTask(BaseTask):
    charge_point_id: str
    name: ConnectionStatus = ConnectionStatus.DISCONNECT
