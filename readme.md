
```shell
# 普通镜像构建
docker build -t http-server .

# 高级镜像构建，比如指定CPU平台为arm64
docker buildx build \
-t http-server:2.0-arm64 \
--platform=linux/arm64 \
-o type=docker . 

# 将镜像导出为tar包
docker save http-server:2.0-arm64 -o ./http-server-arm64.tar 

# 在其他服务器将tar包内的镜像加载到本地
docker load -i ./http-server-arm64.tar 
```

```shell
# 不带密码的
docker run -d \
-p 7799:8080 \
-v /Users/pengdu/Library/app:/files \
http-server

# 带密码的
docker run -d \
-e HTTP_USER="admin" \
-e HTTP_PASSWORD="admin123" \
-p 7799:8080 \
-v /Users/pengdu/Library/app:/files \
http-server
```