from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3

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

app = FastAPI()


@app.get('/')
async def glavn_html(request: Request):
    return templates.TemplateResponse('glavn.html', {'request': request})


@app.get('/registr')
async def registrat_html(request: Request):
    return templates.TemplateResponse('registr.html', {'request': request})


@app.get('/login')
async def login_html(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.get('/logout')
async def logout_html(request: Request):
    return templates.TemplateResponse('logout.html', {'request': request})


@app.post('/register')
async def registration(request: Request):
    login = request.get('login')
    password_1 = request.get('password_1')
    password_2 = request.get('password_2')
    if password_1 != password_2:
        error = 'Пароли должны совпадать!'
        return templates.TemplateResponse('registr.html', {
            'request': request,
            'error': error
        })
    cursor.execute('SELECT * FROM Users WHERE login = ?', (login,))
    if login == cursor.fetchone():
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


@app.post('/login')
async def login(request: Request):
    login = request.get('login')
    password = request.get('password')
    cursor.execute('SELECT * FROM Users WHERE login = ?',
                   (login,))
    if login != cursor.fetchone():
        error = 'Неправильный логин или пароль'
        return templates.TemplateResponse('login.html', {
            'request': request, 'error': error
        })
    cursor.execute('SELECT * FROM Users WHERE password = ?',
                   (password,))
    if password != cursor.fetchone():
        error = 'Неправильный логин или пароль'
        return templates.TemplateResponse('login.html', {
            'request': request, 'error': error
        })
    message = 'Вы вошли успешно!'
    return templates.TemplateResponse('login.html', {
        'request': Request, 'message': message
    })


@app.delete('/logout')
async def logout(request: Request):
    login = request.get('login')
    password = request.get('password')
    cursor.execute('SELECT * FROM Users WHERE login = ?',
                   (login,))
    if login != cursor.fetchone():
        error = 'Неправильный логин или пароль'
        return templates.TemplateResponse('login.html', {
            'request': request, 'error': error
        })
    cursor.execute('SELECT * FROM Users WHERE password = ?',
                   (password,))
    if password != cursor.fetchone():
        error = 'Неправильный логин или пароль'
        return templates.TemplateResponse('login.html', {
            'request': request, 'error': error
        })
    message = 'Вы успешно вышли!'
    return templates.TemplateResponse('login.html', {
        'request': request,
        'message': message
    })