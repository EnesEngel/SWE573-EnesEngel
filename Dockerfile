FROM python:3.12

WORKDIR /BoSProject

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD cd BoSProject && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
