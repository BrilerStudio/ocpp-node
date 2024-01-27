from ocpp.v16.call import (
    SecurityEventNotificationPayload as CallSecurityEventNotificationPayload,
)
from ocpp.v16.call_result import (
    SecurityEventNotificationPayload as CallResultSecurityEventNotificationPayload,
)
from ocpp.v16.enums import Action

from core.queue.publisher import publish
from models.security_event_notification import (
    SecurityEventNotificationEvent,
)
from router import Router
from tasks import StatusNotificationTask
from utils.logging import logger

router = Router()


@router.on(Action.SecurityEventNotification)
async def on_status_notification(
    message_id: str,
    charge_point_id: str,
    **kwargs,
):
    logger.info(
        f'Start accept security event notification '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = SecurityEventNotificationEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallSecurityEventNotificationPayload(**kwargs),
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)


@router.out(Action.SecurityEventNotification)
async def respond_status_notification(
    task: StatusNotificationTask,
) -> CallResultSecurityEventNotificationPayload:
    logger.info(f'Start respond security event notification task={task}).')
    return CallResultSecurityEventNotificationPayload()
