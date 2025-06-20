# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录内容复制到容器中的 /app 目录
# 安装依赖
COPY . /app
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

# 指定容器启动时运行的命令
CMD ["python", "app.py"]