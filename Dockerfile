FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# TA-Lib
#RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
#  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
#  cd ta-lib/ && \
#  ./configure --prefix=/usr && \
#  make && \
#  make install
#
#RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .
# EXPOSE 指令是声明容器运行时提供服务的端口
# 这只是一个声明，在容器运行时并不会因为这个声明应用就会开启这个端口的服务。
# 作用1.帮助镜像使用者理解这个镜像服务的守护端口，以方便配置映射；
# 作用2.则是在运行时使用随机端口映射时，也就是 docker run -P 时，会自动随机映射 EXPOSE 的端口。
EXPOSE 8020
ENTRYPOINT ["python", "./server.py"]
