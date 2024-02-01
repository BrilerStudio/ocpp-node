from ocpp.v16.call import RemoteStartTransactionPayload as CallRemoteStartTransactionPayload
from ocpp.v16.enums import Action

from router import Router
from tasks_models.remote_start_transaction import RemoteStartTransactionTask
from utils.logging import logger

router = Router()


@router.on(Action.RemoteStartTransaction)
async def on_remote_start_transaction(
        message_id: str,
        charge_point_id: str,
        **kwargs,
):
    logger.info(
        f'Got remote start transaction response '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )


@router.out(Action.RemoteStartTransaction)
async def respond_remote_start_transaction(task: RemoteStartTransactionTask) -> CallRemoteStartTransactionPayload:
    logger.info(f'Start respond remote_start_transaction task={task}).')
    return CallRemoteStartTransactionPayload(
        id_tag=task.id_tag,
        connector_id=task.connector_id,
        charging_profile=task.charging_profile,
    )
