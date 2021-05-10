import sqlite3
from KSM_functions import *

# conn = sqlite3.connect('KSM_db.db')
# c = conn.cursor()

# c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user, name, server, region)''')
# c.execute('''CREATE TABLE whitelist (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name, server, region)''')
# c.execute('''CREATE TABLE blacklist (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name, server, region)''')
# c.execute('''CREATE TABLE character_dungeons (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, character_id INTEGER, dungeon_id INTEGER, timed INTEGER, highest INTEGER)''')

key = get_api_key()
# dungeons = get_dungeon_list(key)

# c.execute('''CREATE TABLE dungeons (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name)''')

# for dungeon in dungeons:
#     c.execute("INSERT INTO dungeons (name) VALUES(?)", (dungeon,))

# conn.commit()
# conn.close()


def update_character(user, name, server, region):
    name = name.lower()
    server = server.lower()
    server = server.replace(" ", "-").replace("'", "")
    region = region.lower()

    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (user, name, server, region) VALUES (?,?,?,?)", (user, name, server, region))
    conn.commit()
    conn.close()

    msg = f'Main character set to {name.title()}-{server.title()}-{region.upper()}'
    return msg

def get_character(user):
    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user= ?', (user,))
    return c.fetchone()

def update_roster(name, server, region):
    #roster (name, rank INTEGER, class)
    guild = [region, server, name.lower()]
    roster = get_roster(key, guild)

    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS roster')
    c.execute('''CREATE TABLE roster (id INTEGER PRIMARY KEY, name, rank INTEGER, class)''')

    for name in roster:
        rank = roster[name]['rank']
        pclass = roster[name]['class']
        c.execute('INSERT INTO roster (name, rank, class) VALUES(?, ?, ?)', (name, rank, pclass))
    conn.commit()
    conn.close()

def clear_roster():
    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS roster')
    conn.close()

def get_db_roster(ranks = None): 
    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    if ranks == None:
        c.execute('SELECT * FROM roster')
    else:
        seq = ','.join(['?']*len(ranks))
        c.execute(f'SELECT * FROM roster WHERE rank IN ({seq})', (ranks))
    return c.fetchall() # [[id, name, rank, class], ]

def update_roster_ksm(table, ranks = None):
    roster = get_db_roster(ranks)
    server = 'zuljin'
    region = 'us'

    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()

    for i in roster:
        name = i[1]
        c.execute('SELECT id FROM roster WHERE name = ?', (name, ))
        character_id = c.fetchone()[0]

        profile = [region, server, name.lower()]
        top_two = top_two_keys(key, profile)
        
        for j in top_two:
            dungeon = j
            c.execute('SELECT id FROM dungeons WHERE name = ?', (dungeon, ))
            dungeon_id = c.fetchone()[0]

            timed = 0
            highest = 0

            for k in top_two[j]:
                if k[1] == True:
                    timed = k[0]
                    if highest < timed:
                        highest = k[0]
                elif k[1] == False:
                    if k[0] > timed:
                        highest = k[0]

            c.execute('INSERT INTO character_dungeons (character_id, dungeon_id, timed, highest) VALUES (?, ?, ?, ?)', (character_id, dungeon_id, timed, highest))
    
    conn.commit()
    conn.close()



# ******************** NYI ********************
# This does not work.......

# def update_guild(user, name, server, region):
#     name = name.lower()
#     server = server.lower()
#     server = server.replace(" ", "-").replace("'", "")
#     region = region.lower()

#     conn = sqlite3.connect('KSM_db.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO users VALUES (?,?,?,?)", (user, name, server, region))
#     conn.commit()
#     conn.close()

def add_character(name, server, region):
    name = name.lower()
    server = server.lower()
    server = server.replace(" ", "-").replace("'", "")
    region = region.lower()

    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO whitelist (name, server, region) VALUES (?,?,?)", (name, server, region))
    conn.commit()
    conn.close()

def ksm_character(table, name, server = 'zuljin', region = 'us'):
    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()

    c.execute("SELECT id from roster WHERE name = (?)", (name, ))
    character_id = c.fetchone()[0]
    c.execute(f"SELECT dungeon_id FROM character_dungeons WHERE character_id = (?) AND timed < 15", (character_id, ))
    ids = c.fetchall()

    needed = []

    for id in ids:
        c.execute("SELECT name FROM dungeons WHERE id = (?)", (id))
        dungeon = c.fetchone()[0]
        needed.append(dungeon)
    return needed

def ksm_dungeon(table, name, server = 'zuljin', region = 'us'):
    conn = sqlite3.connect('KSM_db.db')
    c = conn.cursor()
    c.execute("SELECT id FROM dungeons WHERE name = (?)", (name, ))
    dungeon_id = c.fetchone()[0]

    c.execute(f"SELECT character_id from character_dungeons WHERE dungeon_id = (?) AND timed < 15", (dungeon_id, ))
    ids = c.fetchall()
    
    needed = []

    for id in ids:
        c.execute("SELECT name FROM roster WHERE id = (?)", (id))
        character = c.fetchone()[0]
        needed.append(character)
    return needed