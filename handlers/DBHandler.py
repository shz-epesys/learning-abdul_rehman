from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def insert(table='', feilds=[], values=[], where=''):
    values = list(map(lambda v: f'"{v}"', values))
    print(values)
    query = f'INSERT INTO {table} ({",".join(feilds)}) VALUES ({",".join(values)})'
    if where:
        query += f'WHERE {where}'
    db.session.execute(query)
    db.session.commit()


def delete(table='', where=''):
    query = f'delete from {table} '
    if where:
        query += f'WHERE {where}'
    db.session.execute(query)
    db.session.commit()


def update(table='', feilds=[], values=[], where=''):
    values = list(map(lambda v, f: f'{f}="{v}"', values, feilds))
    query = f'update {table} set {",".join(values)}'
    if where:
        query += f'WHERE {where}'
    db.session.execute(query)
    db.session.commit()


def select(table='', feilds=[], where=''):
    if not feilds:
        feilds = '*'
    else:
        feilds = ','.join(feilds)
    query = f'SELECT {feilds} FROM {table}'
    if where:
        query += f' WHERE {where};'
    result = db.session.execute(query)
    return result
