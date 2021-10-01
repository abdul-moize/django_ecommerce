# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app/
ADD . /app/

RUN apt-get update && apt-get install -y sudo
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log


RUN python manage.py migrate
RUN echo "from users.models import User; User.objects.create_superuser('admin@admin.com', 'adminpassword', name='Admin')" | python manage.py shell
RUN python manage.py collectstatic
RUN chown www-data:www-data /app/
RUN chown www-data:www-data /app/db.sqlite3
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
EXPOSE 8000

RUN chmod 755 start-script.sh
CMD ["./start-script.sh"]
