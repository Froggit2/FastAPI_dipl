from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory='templates')

connection = sqlite3.connect('FastAPI.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
login TEXT UNIQUE,
password TEXT
)
''')
connection.commit()

@app.get('/')
async def glavn_html(request: Request):
    return templates.TemplateResponse('glavn.html', {'request': request})

@app.get('/registr')
async def registrat_html(request: Request):
    return templates.TemplateResponse('registr.html', {'request': request})

@app.post('/register')
async def registration(request: Request):
    form = await request.form()
    login = form.get('login')
    password_1 = form.get('password_1')
    password_2 = form.get('password_2')
    if password_1 != password_2:
        error = 'Пароли должны совпадать!'
        return templates.TemplateResponse('registr.html', {
            'request': request,
            'error': error
        })
    cursor.execute('SELECT * FROM Users WHERE login = ?', (login,))
    if cursor.fetchone():
        error = 'Логин не должен совпадать с логином другого пользователя!'
        return templates.TemplateResponse('registr.html', {
            'request': request,
            'error': error
        })
    cursor.execute('INSERT INTO Users (login, password) VALUES (?, ?)',
                   (login, password_2))
    connection.commit()
    return templates.TemplateResponse('registr.html', {
        'request': request,
        'message': 'Регистрация прошла успешно!'
    })

@app.get('/login')
async def login_html(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.post('/login')
async def login(request: Request):
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    cursor.execute('SELECT * FROM Users WHERE login = ? AND password = ?',
                   (login, password))
    if not cursor.fetchone():
        error = 'Неправильный логин или пароль'
        return templates.TemplateResponse('login.html', {
            'request': request, 'error': error
        })
    message = 'Вы вошли успешно!'
    return templates.TemplateResponse('login.html', {
        'request': request, 'message': message
    })

@app.get('/logout')
async def logout_html(request: Request):
    return templates.TemplateResponse('logout.html', {'request': request})

@app.post('/logout')
async def logout(request: Request):
    login = request.form.get('login')
    password = request.form.get('password')
    cursor.execute('DELETE FROM Users WHERE login = ? AND password = ?',
                   (login, password))
    message = 'Вы успешно вышли!'
    return templates.TemplateResponse('logout.html', {
        'request': request, 'message': message
    })