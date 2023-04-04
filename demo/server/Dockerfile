# Скаичваем образ ubuntu и python
FROM ubuntu:20.04

# Копируем файль requirements.txt в образ
COPY ./requirements.txt /app/requirements.txt

# Меняем рабочу директорию
WORKDIR /app

# Install required libs
RUN apt-get update \
 && apt-get install -y sudo
RUN apt-get -y install locales
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Устаналиваем локали
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8   

# Устанавливаем зависимости python
RUN pip3 install -r requirements.txt 

# Копируем файлы в образ
COPY . /app

# Как запускать приложение
ENTRYPOINT ["python3"]

CMD ["index.py"]