from ocpp.v16.call import StartTransactionPayload as CallStartTransactionPayload
from ocpp.v16.call_result import (
    StartTransactionPayload as CallResultStartTransactionPayload,
)
from ocpp.v16.enums import Action

from core.queue.publisher import publish
from models.start_transaction import StartTransactionEvent
from router import Router
from tasks_models.start_transaction import StartTransactionTask
from utils.logging import logger

router = Router()


@router.on(Action.StartTransaction)
async def on_start_transaction(
    message_id: str,
    charge_point_id: str,
    **kwargs,
):
    logger.info(
        f'Start transaction '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = StartTransactionEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallStartTransactionPayload(**kwargs),
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)


@router.out(Action.StartTransaction)
async def respond_start_transaction(task: StartTransactionTask) -> CallResultStartTransactionPayload:
    logger.info(f'Start respond start_transaction task={task}).')
    return CallResultStartTransactionPayload(
        transaction_id=task.transaction_id,
        id_tag_info=task.id_tag_info,
    )
