FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLAG="DOOM{ssrf_thr0ugh_th3_mult1v3rs3_t0_th3_c0r3}"
ENV INTERNAL_PORT="9000"
# Only the scanner is published. Port 9000 (Sacred Timeline Core) stays internal.
EXPOSE 5003
CMD ["python","app.py"]
