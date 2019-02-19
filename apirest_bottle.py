# -*- coding: utf-8 -*
import argparse
import json
from bottle import run, get, post, request

DB = {}


@get('/<table>')
def get_all_from_table(table):
    return {table: DB[table]}


@get('/<table>/<id>')
def get_from_table_by_id(table, id):
    element = [c for c in DB[table] if c['id'] == int(id)]
    return{table: element[0]}

# TODO: Generalize request.json.*
@post('/<table>')
def add_from_table(table):
    global DB
    new_element = {
        'id': len(DB) + 1,
        'nombre': request.json.get('nombre')}
    DB[table].append(new_element)
    return {'element': new_element}


# TODO: Add method to remove elements


def setup_db(json_file_list):
    global DB
    if json_file_list:
        for json_file in json_file_list:
            with open(json_file) as jf:
                table_name = json_file.split('/')[-1].split('.')[0]
                data = json.loads(jf.read())
                DB[table_name] = []
                for i, d in enumerate(data):
                    d['id'] = i
                    DB[table_name].append(d)
    else:
        DB['cuenta_corriente'] = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        argument_default=None, description='Run APIRest in Bottle.')
    parser.add_argument('-p', '--port', type=str, default='9000',
                        dest='port', help='Port (default 9000)')
    parser.add_argument('-d', '--data', type=str, default=[],
                        nargs="+", dest='json_file_list', required=True,
                        help='Path to JSON file (Space separated list. File name format: table_name.json)')

    args = parser.parse_args()
    setup_db(args.json_file_list)

    run(host='localhost', port=args.port, reloader=True, debug=True)
