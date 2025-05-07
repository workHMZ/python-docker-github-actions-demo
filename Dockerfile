# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录内容复制到容器中的 /app 目录
COPY . /app

# 指定容器启动时运行的命令
CMD ["python", "app.py"]