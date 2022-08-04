import json
import logging
import sys
from typing import Union, Generator, Any

from merger import HeterogenousTypeException, NotImplementedException
from merger import merge_dict
# from merger import merge_list


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
)


def simulated_event_stream() -> Generator:
    """
    Simulates a stream of events, without knowing the size of the events.
    :return: A generator of dictionaries extracted from a json-per-line file.
    """
    for line in sys.stdin:
        yield json.loads(line)


def new_field_callback(event: dict, path: list, key: Any, value: Any):
    """
    Processes events that received when a new field is added at the current JSON schema.
    :param event: The raw payload of the new event.
    :param path: The path of the field at the JSON file that added.
    :param key: The key of the new field.
    :param value: The value of the new field.
    """

    row_serialised = json.dumps({
        'event': event,
        'path': path,
        'key': key,
        'value': value
    }, indent=2)
    logging.info(f'New field Callback:\n {row_serialised}')


def hetergenous_event_callback(event: dict, message: str, path: list, data: Union[dict, list]):
    """
    Processes events that have hetergenous types at the same field.
    :param event: The raw payload of the erroneous event.
    :param message: The message from the exception that raised.
    :param path: The path of the field (at the JSON file) that face the issue.
    :param data: The values that produce the issue.
    """

    row_serialised = json.dumps({
        'event': event,
        'message': message,
        'path': path,
        'data': data
    }, indent=2)
    logging.error(f'Hetergenous type Callback:\n {row_serialised}')


def schema_callback(doc: dict):
    """
    Processes the "schema" (or merged dictionary) of all events.
    :param doc: The document that represent the schema of all events combined.
    """
    schema_serialised = json.dumps(doc, default=str, indent=2)
    logging.info(f'Schema definition:\n{schema_serialised}')


def main():
    frankenstein = {}
    for event in simulated_event_stream():
        try:
            frankenstein = merge_dict(dict(frankenstein), event, on_new_field=new_field_callback)
        except HeterogenousTypeException as e:
            hetergenous_event_callback(event, e.message, e.path, e.data)
        except NotImplementedException as e:
            logging.error(e)

    schema_callback(frankenstein)


if __name__ == '__main__':
    main()
