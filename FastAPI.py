from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from models_FastAPI import Users, Session, Products

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def glavn_html(request: Request):
    return templates.TemplateResponse('glavn.html', {'request': request})

@app.get('/register')
async def registrat_html(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@app.post('/register')
async def registration(request: Request):
    session = Session()
    form = await request.form()
    login = form.get('login')
    password_1 = form.get('password_1')
    password_2 = form.get('password_2')
    if password_1 != password_2:
        error = 'Пароли должны совпадать!'
        return templates.TemplateResponse('register.html', {'request': request, 'error': error})  # Создаем сессию
    try:
        existing_user = session.query(Users).filter_by(login=login).first()
        if existing_user:
            error = 'Логин не должен совпадать с логином другого пользователя!'
            return templates.TemplateResponse('register.html', {'request': request, 'error': error})
        new_user = Users(login=login, password=password_2)
        session.add(new_user)
        session.commit()
        message = 'Регистрация прошла успешно!'
        return templates.TemplateResponse('register.html', {'request': request, 'message': message})
    finally:
        session.close()

@app.get('/products')
async def products_list(request: Request):
    session = Session
    products = session.query(Products).all()
    session.close()
    return templates.TemplateResponse('products.html', {'request': request, 'product': products})

@app.post('/products')
async def products(request: Request):
    message = 'Вы успешно приобрели продукт!'
    return templates.TemplateResponse('products.html', {'request': request, 'message': message})

@app.get('/add_product')
async def add_product_html(request: Request):
    return templates.TemplateResponse('add_product.html', {'request': request})

@app.post('/add_product')
async def add_product(request: Request):
    session = Session
    form = await request.form()
    name = form.get('name')
    price = form.get('price')
    new_product = Products(name=name, price=price)
    session.add(new_product)
    session.commit()
    session.close()
    message = 'Продукт успешно добавлен!'
    return templates.TemplateResponse('add_product.html', {'request': request, 'message': message})

@app.get('/login')
async def login_html(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.post('/login')
async def login(request: Request):
    session = Session()
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    try:
        user = session.query(Users).filter_by(login=login, password=password).first()
        if not user:
            error = 'Неправильный логин или пароль!'
            return templates.TemplateResponse('login.html', {'request': request, 'error': error})
        message = 'Вы вошли успешно!'
        return templates.TemplateResponse('products.html', {'request': request, 'message': message})
    finally:
        session.close()

@app.get('/logout')
async def logout_html(request: Request):
    return templates.TemplateResponse('logout.html', {'request': request})

@app.post('/logout')
async def logout(request: Request):
    session = Session()
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    try:
        user = session.query(Users).filter_by(login=login, password=password).first()
        if user:
            session.delete(user)
            session.commit()
            message = 'Вы успешно вышли!'
            return templates.TemplateResponse('logout.html', {'request': request, 'message': message})
        else:
            error = 'Пользователь не найден!'
            return templates.TemplateResponse('logout.html', {'request': request, 'error': error})
    finally:
        session.close()