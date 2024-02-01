from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class RemoteStopTransactionTask(BaseTask):
    action: Action = Action.RemoteStopTransaction
    transaction_id: int
