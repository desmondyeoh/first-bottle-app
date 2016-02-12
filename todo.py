__author__ = 'desmond'

import sqlite3
from bottle import run, route, template, request, static_file, error


@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status='1'")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows=result)
    return output

@route('/new', method='GET')
def new_item():

    if request.GET.get('save', '').strip():
        # define
        new = request.GET.get('task', '').strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        # do stuff
        c.execute("INSERT INTO todo(task, status) VALUES(?, ?)", (new, 1))
        new_id = c.lastrowid

         # commit
        conn.commit()
        conn.close()

        return "<p>new task was inserted into database, ID is %s</p>" % new_id
    else:
        return template('new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.get('save', '').strip():
        edit = request.GET.get('task', '').strip()
        status = request.GET.get('status', '').strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id = ?", (edit, status, no))
        conn.commit()
        conn.close()

        return "The item number %s was updated" % no
    else:
        conn = sqlite3.connect("todo.db")
        c = conn.cursor()
        no = str(no)
        c.execute("SELECT task FROM todo WHERE id = ?", (no,))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)


@route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute("SELECT task, status FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchone()
    conn.close()
    if not result:
        return 'This item number does not exist'
    else:
        return 'Task: %s' % str(result)


@route('/help')
def help():
    return static_file(filename='help.html', root='.')

@route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id = ?", (json,))
    result = c.fetchone()
    conn.close()
    if not result:
        return {'task': 'This item number does not exist'}
    else:
        return {'Task': result}


@error(404)
def mistake404(error):
    return 'Sorry, this page does not exist'

@error(403)
def mistake403(error):
    return 'The parameter you passed has the wrong format!'

run(host='localhost', port=8080, reloader=True, debug=True)