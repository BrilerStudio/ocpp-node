from ocpp.v16.call import StatusNotificationPayload as CallStatusNotificationPayload
from ocpp.v16.call_result import (
    StatusNotificationPayload as CallResultStatusNotificationPayload,
)
from ocpp.v16.enums import Action

from core.queue.publisher import publish
from models.status_notification import StatusNotificationEvent
from router import Router
from tasks import StatusNotificationTask
from utils.logging import logger

router = Router()


@router.on(Action.StatusNotification)
async def on_status_notification(
    message_id: str,
    charge_point_id: str,
    **kwargs,
):
    logger.info(
        f'Start accept status notification '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = StatusNotificationEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallStatusNotificationPayload(**kwargs),
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)


@router.out(Action.StatusNotification)
async def respond_status_notification(task: StatusNotificationTask) -> CallResultStatusNotificationPayload:
    logger.info(f'Start respond heartbeat task={task}).')
    return CallResultStatusNotificationPayload()
