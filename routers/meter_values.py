from ocpp.v16.call import MeterValuesPayload as CallMeterValuesPayload
from ocpp.v16.call_result import MeterValuesPayload as CallResultMeterValuesPayload
from ocpp.v16.enums import Action

from core.queue.publisher import publish
from models.meter_values import MeterValuesEvent
from router import Router
from tasks import MeterValuesTask
from utils.logging import logger

router = Router()


@router.on(Action.MeterValues)
async def on_meter_values(
    message_id: str,
    charge_point_id: str,
    **kwargs,
):
    logger.info(
        f'Start handle meter values '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = MeterValuesEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallMeterValuesPayload(**kwargs),
    )
    await publish(event.model_dump_json(), to=event.exchange, priority=event.priority)


@router.out(Action.MeterValues)
async def respond_meter_values(task: MeterValuesTask) -> CallResultMeterValuesPayload:
    logger.info(f'Start respond meter values task={task}).')
    return CallResultMeterValuesPayload()
