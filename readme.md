
```shell
docker build -t http-server .

docker buildx build \
-t http-server:2.0-arm64 \
--platform=linux/arm64 \
-o type=docker . 

docker save http-server:2.0-arm64 -o ./http-server-arm64.tar 

docker load -i ./http-server-arm64.tar 
```

```shell
docker run -d \
-p 7799:8080 \
-v /Users/pengdu/Library/app:/files \
http-server

docker run -d \
-e HTTP_USER="admin" \
-e HTTP_PASSWORD="admin123" \
-p 7799:8080 \
-v /Users/pengdu/Library/app:/files \
http-server
```