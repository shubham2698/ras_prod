FROM python:3.10
WORKDIR /app
COPY requirement.txt .
COPY run.py .
RUN pip install -r requirement.txt
COPY ras ras
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 CMD curl -f http://localhost:5000/health || exit 1
ENTRYPOINT ["python","./run.py"]