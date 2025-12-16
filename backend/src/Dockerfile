# 基础镜像
FROM python:3.12.1-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（wkhtmltopdf + 中文字体，解决PDF中文乱码）
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    fonts-wqy-zenhei \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖清单
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码
COPY src/ /app/src/
COPY .env /app/

# 暴露端口
EXPOSE 8000

# 启动命令（默认启动FastAPI，Celery单独启动）
CMD ["python", "src/main.py"]