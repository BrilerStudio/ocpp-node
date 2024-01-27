from ocpp.v16.call import BootNotificationPayload as CallBootNotificationPayload
from ocpp.v16.call_result import (
    BootNotificationPayload as CallResultBootNotificationPayload,
)
from ocpp.v16.enums import Action

from core.queue.publisher import publish
from models.boot_notification import BootNotificationEvent
from router import Router
from tasks_models.boot_notification import BootNotificationTask
from utils.logging import logger

router = Router()


@router.on(Action.BootNotification)
async def on_boot_notification(
        message_id: str,
        charge_point_id: str,
        **kwargs,
):
    logger.info(
        f'Start accept boot notification '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = BootNotificationEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallBootNotificationPayload(**kwargs),
    )
    await publish(event.model_dump_json(), to=event.exchange, priority=event.priority)


@router.out(Action.BootNotification)
async def respond_boot_notification(task: BootNotificationTask) -> CallResultBootNotificationPayload:
    logger.info(f'Start respond boot notification task={task}).')
    return CallResultBootNotificationPayload(
        current_time=task.current_time,
        interval=task.interval,
        status=task.status,
    )
