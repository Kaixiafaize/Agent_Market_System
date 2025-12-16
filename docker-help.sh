# 启动容器（后台运行，首次启动会下载镜像）
docker-compose up -d

# 查看容器状态（确认 STATUS 为 Up，健康检查为 healthy）
docker-compose ps

# 查看日志（调试用）
docker-compose logs dev-postgres  # 查看PostgreSQL日志
docker-compose logs dev-redis     # 查看Redis日志

# 停止容器（数据卷保留，不丢失数据）
docker-compose down

# 彻底清理（谨慎！删除容器+数据卷，所有数据丢失）
docker-compose down -v