Nginx

        介绍
            高性能的HTTP和反向代理服务器, 也是一个 IMAP/POP3/SMTP代理服务器
    
        安装:
    
            1. 下载 tar 包
                wget  http://nginx.org/download/nginx-1.10.3.tar.gz
            2. 解压
                tar -zxvf nginx-1.10.3.tar.gz
            3. 配置
                进入解压的目录 执行 ./configure prefix=/usr/local/nginx/
            4. 执行安装
                make && make install
    
                再安装的过程中可能会报错
                    缺少PCRE 正则表达式的包.
                    1. yum install PCRE
                        再configure报错时, 执行
                       yum install pcre-devel
                    缺少 zlib 包
                    1. yum install zlib
                        再configure报错时, 执行
                       yum install zlib-devel
            5. 启动
                conf    配置文件
                html    静态网页文件
                logs    日志文件
                sbin    进程文件
    
                启动命令
                 ./bin/nginx
    
        信号量
    
            ./bin/nginx      启动
            kill sign pid    杀掉nginx进程
                signs:
                    term INT            立即关闭
                    QUIT                优雅关闭
                    HUP                 在修改了nginx的配置文件的时候, 可以不必关闭原nginx的进程, 在使用HUP读取新配置之后再杀掉原主进程
                    USR1                重读日志
                    USR2                平滑的升级
                    WINCH
    
            常规命令
                ./bin/nginx -s reload
                ./bin/nginx -s reopen
                ./bin/nginx -s stop
                ./bin/nginx -t
    
    
        配置文件
    
    
            #user  nobody;
            worker_processes  1;    # 工作的子进程数量  一般设置为CPU数*核数
    
            # nginx的进程与链接的特性
            events {
                # 每个工作进程最多允许的连接数
                worker_connections  1024;
            }
    
            # 配置http服务器
            http {
                include       mime.types;
                default_type  application/octet-stream;
    
                #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                #                  '$status $body_bytes_sent "$http_referer" '
                #                  '"$http_user_agent" "$http_x_forwarded_for"';
    
                #access_log  logs/access.log  main;
    
                sendfile        on;
                #tcp_nopush     on;
    
                #keepalive_timeout  0;
                keepalive_timeout  65;
    
                #gzip  on;
    
                #配置虚拟主机
                server {
                    # 监听的端口
                    listen       80;
                    # 监听的域名
                    server_name  localhost;
    
                    # 映射的资源
                    location / {
                        root   html;
                        index  index.html index.htm;
                    }
                }
            }
    
        日志管理
            nginx 可以针对不同的server访问日志配置
            默认格式:
                log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                  '$status $body_bytes_sent "$http_referer" '
                                  '"$http_user_agent" "$http_x_forwarded_for"';
            配置方式:
                access_log  logs/z.com.access.log  main;
    
    
        rewrite 重写
            语法
                if () {} 设定条件再进行重写. 注意 if 后空格必须写
                    1. = 判断相等
                        if ($remote_addr = 192.168.126.20) {
                            return 403;
                        }
                    2. ~ 正则
                        if ($http_user_agent ~ rv) {
                            rewrite ^.*$ /ie.html;
                            break;
                        }
                    3. -f -e
    
        优化
    
            gzip 压缩
                在 http 请求头中声明 accept-encoding: gzip deflate sdch 服务器在回应的时候会把内容使用相应方式进行压缩再返回给浏览器
    
                常用参数
    
                    gzip on|off                             是否开启gzip
                    gzip_buffer 32 4K | 64 8K               缓冲
                    gzip_comp_level [1-9]                   压缩级别 越高压缩的越小 越浪费cpu
                    gzip_disable                            正则匹配什么样的Uri不进行gzip
                    gzip_min_lenght 300                     压缩的最小长度
                    gzip_http_version 1.0|1.1               压缩的协议版本
                    gzip_proxied                            设置请求者代理服务器, 如何缓存内容
                    gzip_types text/plain application/xml   指定那些类型的文件进行压缩. 具体那些类型可以在 conf/nime_types 文件中查看
                    gzip_vary on|off                        是否传输gizp标志
    
                注意点:
                    图片/视频类二进制文件不进行压缩, 因为压缩率不高, 还浪费cup资源
                    比较小的文件不进行压缩
    
            expires 缓存设置
                在location 或 if 段里使用
                    格式
                        expires 30s|30m|30h|30d
                    注意
                        服务器的日期要准确, 如果服务器的日期落后于实际日期, 缓存将失效
    
                在nginx中的使用方式:
    
        proxy 反向代理
            
            
    
    
        upstream 负载均衡
            
            将多台服务器用up_stream绑定在一起并七个组名, 然后proxy_pass 指向该组. 
            默认的负载均衡很简单, 就是针对组中的服务器逐个请求.
            一致性哈希算法:
                 
        

