from typing import Dict

from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class StopTransactionTask(BaseTask):
    action: Action = Action.StopTransaction
    id_tag_info: Dict
