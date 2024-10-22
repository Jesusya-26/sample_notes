FROM python:3.11-slim

RUN apt update && \
    apt install -y fonts-liberation2 libpq-dev python3-dev build-essential && \
    pip install psycopg2 && \
    apt purge -y python3-dev build-essential --autoremove

COPY requirements.txt /

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN echo "cd sample_notes/db" > /entrypoint.sh && \
    echo "alembic upgrade head" >> /entrypoint.sh && \
    echo "if [ $? = 0 ]; then echo 'Database schema syncronized'; else echo 'alembic upgrade has failed, database state is not determined'; exit 1; fi" >> /entrypoint.sh && \
    echo "cd /" >> /entrypoint.sh && \
    echo "python3 -m sample_notes" >> /entrypoint.sh

COPY sample_notes/ /sample_notes/

ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint.sh"]
