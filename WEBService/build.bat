@echo on

if not "%1"=="" goto %~1

:venv_i
python -m venv venv
md static
md templates
copy _base.html .\templates
call venv\Scripts\activate
call pip install --upgrade pip
call pip install -r requirements.txt
call deactivate

:npm_i
cd frontend
call npm install -g npm
call npm i -g @vue/cli
call npm i axios
call npm i vue-axios
cd ..

:run
cd frontend
call npm run build
cd ..
call venv\Scripts\activate
cls
start http://127.0.0.1:8000
call python manage.py runserver