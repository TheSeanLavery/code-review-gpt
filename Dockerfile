FROM python:3.9

RUN pip install requests configparser openai pytest

CMD ["python"]