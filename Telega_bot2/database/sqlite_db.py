import sqlite3 as sq
from datetime import date

def sql_start():
    global base, cur
    base = sq.connect(f"anonce{date.today()}.db")
    cur = base.cursor()
    if base:
        print("Base connected")
    base.execute('CREATE TABLE IF NOT EXISTS anonce(photo TEXT, description TEXT, price TEXT, link TEXT PRIMARY KEY)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO anonce VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()