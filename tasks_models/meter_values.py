
from ocpp.v16.enums import Action

from tasks_models.base import BaseTask


class MeterValuesTask(BaseTask):
    action: Action = Action.MeterValues
