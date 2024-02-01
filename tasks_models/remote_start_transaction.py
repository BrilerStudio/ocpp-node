from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class RemoteStartTransactionTask(BaseTask):
    action: Action = Action.RemoteStartTransaction
    id_tag: str
    connector_id: int
    charging_profile: dict | None = None
