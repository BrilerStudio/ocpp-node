import asyncio
import http
from traceback import format_exc

import websockets
from ocpp.exceptions import (
    FormatViolationError,
    NotSupportedError,
    PropertyConstraintViolationError,
    ProtocolError,
)
from ocpp.messages import unpack
from websockets import Headers

from core.queue.consumer import start_consume
from core.queue.publisher import publish
from core.settings import OCPP_VERSION, TASKS_EXCHANGE_NAME, WS_SERVER_PORT
from models.on_connection import LostConnectionEvent
from protocols import OCPPWebSocketServerProtocol, api_client
from router import Router
from routers import *  # noqa
from tasks import process_task
from utils.logging import logger

background_tasks = set()
router = Router()


async def watch(connection: OCPPWebSocketServerProtocol):
    while True:
        try:
            raw_msg = await connection.recv()
        except Exception:
            break

        try:
            msg = unpack(raw_msg)
        except (FormatViolationError, ProtocolError, PropertyConstraintViolationError) as exc:
            logger.error('Could not parse message (message=%r, details=%r)' % (raw_msg, format_exc()))
            await connection.send({'code': 'validation_failed', 'details': exc.description})
            continue
        try:
            await router.handle_on(connection, msg)
        except NotSupportedError:
            logger.error('Caught error during call handling (details=%r)' % format_exc())
            continue
        except Exception as error:
            logger.error('Caught error during call handling (details=%r)' % format_exc())
            response = msg.create_call_error(error).to_json()
            await connection.send(response)


async def on_connect(connection, path: str):
    if path == "/healthz":
        await connection.send('ok')
        return await connection.close()

    charge_point_id = path.split('/')[-1].strip('/')
    if not charge_point_id:
        charge_point_id = f'No-id-provided-{id(connection)}'
    connection.charge_point_id = charge_point_id
    logger.info(f'New charge point connected (charge_point_id={charge_point_id}), headers={connection.request_headers}')

    response = await api_client.post(f'manager/ChargePoint/{charge_point_id}/verify_password')
    response_status = http.HTTPStatus(response.status_code)
    if not response_status is http.HTTPStatus.OK:
        connection.write_http_response(response_status, Headers())
        logger.info(f'Could not validate charge point (charge_point_id={charge_point_id})')
        return await connection.close()

    await watch(connection)

    logger.info(f'Closed connection (charge_point_id={charge_point_id})')
    event = LostConnectionEvent(charge_point_id=charge_point_id)
    await publish(event.model_dump_json(), to=event.exchange, priority=event.priority)


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        WS_SERVER_PORT,
        subprotocols=[f'ocpp{OCPP_VERSION}'],
    )
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks_models.
    task = asyncio.create_task(
        start_consume(
            TASKS_EXCHANGE_NAME,
            on_message=lambda data: process_task(data, server),
        ),
    )
    background_tasks.add(task)

    logger.info(f'Server started at ws://0.0.0.0:{WS_SERVER_PORT}')

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
