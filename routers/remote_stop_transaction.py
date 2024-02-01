from ocpp.v16.call import RemoteStopTransactionPayload as CallRemoteStopTransactionPayload
from ocpp.v16.enums import Action

from router import Router
from tasks_models.remote_stop_transaction import RemoteStopTransactionTask
from utils.logging import logger

router = Router()


@router.on(Action.RemoteStopTransaction)
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


@router.out(Action.RemoteStopTransaction)
async def respond_remote_start_transaction(task: RemoteStopTransactionTask) -> CallRemoteStopTransactionPayload:
    logger.info(f'Stop respond remote_start_transaction task={task}).')
    return CallRemoteStopTransactionPayload(
        transaction_id=task.transaction_id,
    )
