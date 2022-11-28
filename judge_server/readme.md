# OJ 微服务Docker构建

## 注意事项
1. 本项目主要分三个部分分别为Base、Mail、Judge
2. Base为整个环境基础
3. Mail为发生邮件服务
4. Judge为外网判题服务

## 使用步骤
### 1. Base的构建
```Docker
docker build . -t hnie:pythonbase -f DockerfileBase
```
### 2. Mail的构建与使用
```Docker
docker build . -t hnie:mail -f DockerfileMail
docker run -d --name mail -p 8000:8000 --restart=always hnie:mail
```
### 3. Judge的构建与使用
```Docker
docker build . -t hnie:judge -f DockerfileJudge
docker run -d --name judge -p 9090:9090 --restart=always hnie:mail
```
