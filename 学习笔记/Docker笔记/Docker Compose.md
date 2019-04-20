# Docker Compose

## 概述

`Docker Compose` 是用来定义和运行多容器Docker应用的工具。 使用单个命令就可以创建、启动和运行所有的应用服务。

## 适用场景

生产 开发 测试 CI 

## 使用Docker Compose的基本步骤

1. 定义应用程序的环境
2. 定义应用程序服务
3. 运行`docker-compose up` 启动应用

## 关于Docker Compose配置文件

https://docs.docker.com/compose/compose-file/

## 生命周期命令

- 启动，停止和重建服务
- 查看正在运行的服务的状态
- 流式传输运行服务的日志输出
- 在服务上运行一次性命令

## Docker Compose安装

### 1. 下载最新的Docker Compose

```
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/ \
docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

上面的命令可能会因为网络的原因下载不了，可以到GitHub下载，地址：

```
https://github.com/docker/compose/releases
```

### 2. 应用docker-compose二进制文件的可执行权限

```
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. 测试安装是否成功

```
docker-compose --version
```

输出类似以下内容即安装成功

```
docker-compose version 1.22.0, build f46880fe
```

### 4. 卸载

```
sudo rm /usr/local/bin/docker-compose
```

## Docker Compose 配置文件

