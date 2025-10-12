FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

# Ensure entrypoint is executable (Linux container)
RUN chmod +x /app/pettech/run_gunicorn.sh || true

# Default to users service; override with SERVICE env (users|jobs|bookings)
ENV SERVICE=users

EXPOSE 80

ENTRYPOINT ["/app/pettech/run_gunicorn.sh"]