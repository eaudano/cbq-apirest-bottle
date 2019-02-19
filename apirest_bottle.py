# -*- coding: utf-8 -*
import argparse
import json
from bottle import run, get, post, request

DB = {}


@get('/cuenta_corriente')
def get_all_cuenta_corriente():
    return {'cuentas': DB['cuenta_corriente']}


@get('/cuenta_corriente/<id>')
def get_cuenta_corriente_by_id(id):
    cuenta = [c for c in DB['cuenta_corriente'] if c['id'] == int(id)]
    return{'cuenta_corriente': cuenta[0]}


@post('/cuenta_corriente')
def add_cuenta_corriente():
    global DB
    new_cuenta_corriente = {'id': len(
        DB) + 1, 'nombre': request.json.get('nombre')}
    DB['cuenta_corriente'].append(new_cuenta_corriente)
    return {'cuenta_corriente': new_cuenta_corriente}


def setup_db(json_file=None):
    global DB
    if json_file:
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
    parser.add_argument('-d', '--data', type=str, default=None,
                        dest='data', help='Path to JSON file')

    args = parser.parse_args()
    setup_db(args.data)

    run(host='localhost', port=args.port, reloader=True, debug=True)
