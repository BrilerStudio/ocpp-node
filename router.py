import functools
from dataclasses import asdict

from ocpp.charge_point import camel_to_snake_case, remove_nones, snake_to_camel_case
from ocpp.exceptions import NotSupportedError
from ocpp.messages import Call, CallResult, validate_payload
from ocpp.v16.enums import Action

from core import settings
from protocols import OCPPWebSocketServerProtocol
from tasks_models.base import BaseTask
from utils.logging import logger


class Router:
    _route_map = {}

    def __init__(self, version: str = settings.OCPP_VERSION):
        self._ocpp_version = version

    async def handle_on(self, connection: OCPPWebSocketServerProtocol, msg: Call):
        logger.info(f'Start handle on action (charge_point_id={connection.charge_point_id}, message={msg.to_json()})')
        try:
            handlers = self._route_map[msg.action]
        except KeyError:
            raise NotSupportedError(
                details={'cause': f'No handler for {msg.action} registered (msg={msg.to_json()}).'},
            )

        if not handlers.get('_skip_schema_validation', False):
            validate_payload(msg, self._ocpp_version)

        snake_case_payload = camel_to_snake_case(msg.payload)

        try:
            handler = handlers['_on_action']
        except KeyError:
            raise NotSupportedError(
                details={'cause': f'No handler for {msg.action} registered.'},
            )

        await handler(msg.unique_id, connection.charge_point_id, **snake_case_payload)

    async def handle_out(self, connection, task: BaseTask):
        logger.info(f'Start handle out action (charge_point_id={connection.charge_point_id}, task={task.dict()})')
        try:
            handlers = self._route_map[task.action]
        except KeyError:
            raise NotSupportedError(
                details={'cause': f'No handler for {task.action} registered.'},
            )
        try:
            handler = handlers['_out_action']
        except KeyError:
            raise NotSupportedError(
                details={'cause': f'No handler for {task.action} registered.'},
            )

        payload = await handler(task)
        temp_response_payload = asdict(payload)
        response_payload = remove_nones(temp_response_payload)
        camel_case_payload = snake_to_camel_case(response_payload)

        if task.action in [Action.RemoteStartTransaction, Action.RemoteStopTransaction]:
            call_result = Call(task.message_id, task.action, camel_case_payload)
            json_response = call_result.to_json()
        else:
            call_result = CallResult(task.message_id, camel_case_payload)
            call_result.action = task.action
            json_response = call_result.to_json()
        await connection.send(json_response)
        logger.info(f'Send response (charge_point_id={connection.charge_point_id}, response={json_response})')

    def _prepare_route_map(self, func, action, option, skip_schema_validation):
        if action not in self._route_map:
            self._route_map[action] = {}
        self._route_map[action][option] = func
        self._route_map[action]['_skip_schema_validation'] = skip_schema_validation

    def on(self, action, *, option='_on_action', skip_schema_validation=False):
        def decorator(func):
            @functools.wraps(func)
            async def inner(*args, **kwargs):
                return await func(*args, **kwargs)

            self._prepare_route_map(func, action, option, skip_schema_validation)

            return inner

        return decorator

    def out(self, action, *, option='_out_action', skip_schema_validation=False):
        def decorator(func):
            @functools.wraps(func)
            async def inner(*args, **kwargs):
                return await func(*args, **kwargs)

            self._prepare_route_map(func, action, option, skip_schema_validation)

            return inner

        return decorator
