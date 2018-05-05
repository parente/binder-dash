FROM jupyter/base-notebook:1fbaef522f17

COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
