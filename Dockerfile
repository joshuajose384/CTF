FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
ENV FLAG="DOOM{r4c1ng_th3_t1m3str34m_b34ts_d00m}"
# RACE_WINDOW widens the exploit window; lower it to make the challenge harder.
ENV RACE_WINDOW="0.25"
EXPOSE 5001
# --threads MUST be > 1 so concurrent requests can race. Keep workers=1 so all
# threads share one in-memory state (that is the whole point).
CMD ["gunicorn","-b","0.0.0.0:5001","--workers","1","--threads","16","app:app"]
