from ocpp.v16.call import AuthorizePayload as CallAuthorizePayload
from ocpp.v16.call_result import AuthorizePayload as CallResultAuthorizePayload
from ocpp.v16.enums import Action

from core.queue.publisher import publish
from models.authorize import AuthorizeEvent
from router import Router
from tasks_models.authorize import AuthorizeTask
from utils.logging import logger

router = Router()


@router.on(Action.Authorize)
async def on_boot_notification(
        message_id: str,
        charge_point_id: str,
        **kwargs,
):
    logger.info(
        f'Start accept authorize action '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = AuthorizeEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallAuthorizePayload(**kwargs),
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)


@router.out(Action.Authorize)
async def respond_authorize(task: AuthorizeTask) -> CallResultAuthorizePayload:
    logger.info(f'Start respond authorize task={task}).')
    return CallResultAuthorizePayload(
        id_tag_info=task.id_tag_info,
    )
