# Dockerfile 

## Dockerfile 简介

Docker 可以通过读取 Dockerfile 来自动构建一个image镜像文件. Dockerfile 是一个文本文档, 包含一些可以使用 `docker build` 构建镜像的指令集, 语法结构在后续介绍

## 使用Docker build通过Dockerfile构建镜像

### Docker build 命令简单使用

```
用法: docker build [OPTIONS] PATH | URL | -
options: 
	常用的有 -t 指定镜像的tag 如 name:tag
	其他参考百度
path Dockerfile 文件的路径
URL Dockerfile 的网络地址
```

#### 使用当前路径的Dockerfile进行build

`docker build -t 镜像名称 本地Dockerfile的路径: 官方建议是不使用/根目录作为镜像构建的上下文`

```
示例: 从当前路径下的Dockerfile构建一个hello-wrold的镜像
docker build -t hello-world .
```

#### 使用URL的Dockerfile构建镜像

一般来说在开发中使用` DevOps`进行自动化部署的时候, 通常都是将`Dockerfile`放在Git 仓库中(可以是`GitHub, GitLab` 等等), 但是实际的用法并不推荐使用URL的方式, 而是将具体的github代码clone到本地机器, 然后使用本地Dockerfile 进行镜像的构建.

```
示例: 使用URL github.com/creack/docker-firefox 的 Dockerfile 创建镜像
docker build -t firefox github.com/creack/docker-firefox
```

#### 通过-f命令指定Dockerfile的路径

```
docker build -f /docker/demo/Dockerfile .
```

## Dockerfile 语法及使用

### FROM

表示从哪个 `base image` 进行新的image的构建, 可以在同一个`Dockerfile`中多次出现

```
FROM <image> [AS <name>] 
或者
FROM <image>[:<tag>] [AS <name>]
或者
FROM <image>[@<digest>] [AS <name>]

AS <name>: 将FROM 下载的image重命名。该名称可用于后续FROM和COPY --from=<name|index>指令, 以引用此阶段构建的Image。
```

### RUN 和 CMD 和 ENTRYPOINT

这三个命令在使用上会有一些差异, 根据使用的语法格式不同会有一些需要注意的地方

#### RUN  

​	命令每执行一次命令将创建一个新的Image Layer(镜像的层)

#### CMD 

​	RUN 命令用来设置容器启动后默认执行的命令和参数

​	如果docker run指定了其它命令,  CMD命令将被忽略

​	并且如果指定了多个CMD, 将只有最后一个会被执行

#### ENTRYPOINT

​	ENTRYPOINT 命令用来设置容器启动时运行的命令

​	让容器以应用或者服务的形式来运行

​	不会被忽略, 一定会被执行

#### 此三个命令都有两种格式

##### Shell 格式

`shell` 格式会将命令以shell命令的方式来执行

```
RUN yum install -y vim				
CMD echo xxxx
ENTRYPOINT echo xxxx
```

##### Exec 格式

`Exec` 格式需要使用特定的语法格式来指明运行的命令以及命令的参数

```
RUN ["yum","install","-y","vim"]					
CMD ["echo", "XXX"]
ENTRYPOINT ["echo", "xxx"]
```

##### 两种格式中使用shell变量的区别

shell 格式下会打印出 `hello Docker`

```
FROM centos
ENV name Docker
ENTRYPOINT echo hello ${name}
RUN echo hello ${name}
CMD echo hello ${name}
```

Exec 格式下需要指明运行命令是通过shell来执行的

```
FROM centos
ENV name Docker
ENTRYPOINT ["/bin/bash", "-c", "echo hello ${name}"]
RUN ["/bin/bash", "-c", "echo hello ${name}"]
CMD ["/bin/bash", "-c", "echo hello ${name}"]
```

### LABLE

该`LABEL`指令将元数据添加到Image. 一个 `LABEL`是键值对。要在`LABEL`值中包含空格，请使用引号和反斜杠，就像在命令行解析中一样。

​	

