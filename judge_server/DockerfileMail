FROM python:3.6.8

#RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#		postgresql-client \
#	&& rm -rf /var/lib/apt/lists/*

WORKDIR /home/judge/judge_server
#COPY ./* ./
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN
#RUN


EXPOSE 8000
EXPOSE 22

ENTRYPOINT ["python3 manage.py runserver 0.0.0.0:8000"]