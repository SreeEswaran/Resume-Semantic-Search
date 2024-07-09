

FROM python:3.9-slim

COPY .. /app
RUN pip install -r requirements.txt



WORKDIR /app


RUN ./start.sh

CMD ["streamlit", "run", "app.py", "--server.port=8501"]