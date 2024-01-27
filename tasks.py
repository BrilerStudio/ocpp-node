from __future__ import annotations

from functools import wraps
from typing import Callable, Union

from ocpp.v16.enums import Action
from websockets.legacy.server import WebSocketServer

from core.fields import ConnectionStatus
from router import Router
from tasks_models.authorize import AuthorizeTask
from tasks_models.boot_notification import BootNotificationTask
from tasks_models.heartbeat import HeartbeatTask
from tasks_models.meter_values import MeterValuesTask
from tasks_models.security_event_notification import SecurityEventNotificationTask
from tasks_models.start_transaction import StartTransactionTask
from tasks_models.status_notification import StatusNotificationTask
from tasks_models.stop_transaction import StopTransactionTask
from utils.logging import logger

router = Router()


def prepare_task(func) -> Callable:
    @wraps(func)
    async def wrapper(data, *args, **kwargs):
        task = {
            Action.StatusNotification: StatusNotificationTask,
            Action.BootNotification: BootNotificationTask,
            Action.Heartbeat: HeartbeatTask,
            Action.SecurityEventNotification: SecurityEventNotificationTask,
            Action.Authorize: AuthorizeTask,
            Action.StartTransaction: StartTransactionTask,
            Action.StopTransaction: StopTransactionTask,
            Action.MeterValues: MeterValuesTask,
        }[data['action']](**data)
        return await func(task, *args, **kwargs)

    return wrapper


@prepare_task
async def process_task(
        task: Union[
            StatusNotificationTask,
            BootNotificationTask,
            HeartbeatTask,
            SecurityEventNotificationTask,
            AuthorizeTask,
            StartTransactionTask,
            StopTransactionTask,
            MeterValuesTask,
        ],
        server: WebSocketServer,
) -> None:
    logger.info(f'Got task from manager (task={task})')
    connections = [conn for conn in server.websockets if conn.charge_point_id == task.charge_point_id]
    if not connections:
        return
    connection = connections[0]

    if task.action is ConnectionStatus.DISCONNECT:
        await connection.close()
        return

    await router.handle_out(connection, task)
