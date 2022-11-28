### OJ 微服务

### 为hnieoj提供发邮件，将代码提交到其他oj判题的服务

#### 注意事项
1. 该服务运行在 `10.0.38.113` 服务器上的docker容器中。
2. 运行的环境中需先装好 `docker`
3. oj 不能直接向 `10.0.38.113` 发送请求，得使用 `nginx` 做代理转发。
4. sendEmail 服务运行在 `8000` 端口，judge_server 运行在 `9090` 端口上。

#### 项目架构 
1. sendEmail 为使用 django 搭建的后端服务，接收从 oj 发来的各种请求。
2. judge_server 为使用 thrfit 搭建，提供判题服务，现可向 acwing csg codeforces 提交判题。

#### 使用步骤
1. 登录上 `10.0.38.113` 服务器
2. 输入命令 `tmux a` 可进入上次未关闭的tmux中
3. 在 `/home/judge/judge_server` 路径下输入命令 `python3 manage.py runserver 0.0.0.0:8000`启动 Django 服务。
4. 在 `/home/judge/judge_server/match_system/src` 路径下输入命令 `python3 main.py` 启动 thrfit搭建的judge判题服务。

#### [Docker版本的构建](judge_server/)