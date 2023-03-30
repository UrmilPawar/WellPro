cd skin
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=production
flask run &
cd ../symptoms
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=production
flask run &
cd ../WellPro
pip install -r requirements.txt
export FLASK_APP=chatbot.py
export FLASK_ENV=production
flask run &
cd ../skin
pip install -r requirements.txt
export FLASK_APP=wikipedia.py
export FLASK_ENV=production
flask run &
cd ../WellPro/mysql
pip install -r requirements.txt
export FLASK_APP=mysql.py
export FLASK_ENV=production
flask run &
wait
