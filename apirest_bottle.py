# -*- coding: utf-8 -*
import argparse
import json
import bottle
from bottle import run, get, post, request, put, response, route

DB = {}


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            if bottle.request.method != 'OPTIONS':
                return fn(*args, **kwargs)

        return _enable_cors


@get('/<table>')
def get_all_from_table(table):
    return {table: DB[table]}


@get('/<table>/<id>')
def get_from_table_by_id(table, id):
    element = [c for c in DB[table] if c['id'] == id]
    return {table: element[0]}


@route('/<table>', method=['POST', 'OPTIONS'])
def add_to_table(table):
    global DB
    new_element = request.json
    exist_element = [e for e in DB[table] if e['id'] == new_element['id']]
    if exist_element:
        return {'status': 'Fail, exist item with the same id',
                'element': exist_element[0]}
    else:
        DB[table].append(new_element)
        return {'status': 'OK', 'new_element': new_element}


@route('/<table>', method=['PUT', 'OPTIONS'])
def put_in_table(table):
    global DB
    new_element = request.json
    index = -1
    for i, element in enumerate(DB[table]):
        if new_element['id'] == element['id']:
            index = i
            break
    if index >= 0:
        last_version = DB[table].pop(index)
        DB[table].append(new_element)
        return {"status": "OK",
                "new_version": new_element,
                "last_version": last_version}
    else:
        return {'status': 'Fail, element not exist'}


# TODO: Add method to remove elements


def setup_db(json_file_list):
    global DB
    for json_file in json_file_list:
        with open(json_file) as jf:
            table_name = json_file.split('/')[-1].split('.')[0]
            DB[table_name] = json.loads(jf.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        argument_default=None, description='Run APIRest in Bottle.')
    parser.add_argument('-p', '--port', type=str, default='9000',
                        dest='port', help='Port (default 9000)')
    parser.add_argument('-d', '--data', type=str,
                        nargs="+", dest='json_file_list', required=True,
                        help='Path to JSON file (Space separated list. File name format: table_name.json)')
    parser.add_argument('-a', '--host', type=str, default='localhost',
                        dest='host', required=True,
                        help='Host (Default localhost)')
    parser.add_argument('-c', '--enable_cors', type=bool, default=False,
                        dest='enable_cors', help='Enable Cors (default False)')

    args = parser.parse_args()
    setup_db(args.json_file_list)
    if args.enable_cors:
        bottle.install(EnableCors())
    run(host=args.host, port=args.port, reloader=True, debug=True)
