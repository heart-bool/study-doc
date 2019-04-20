# Docker Swarm

## Docker Swarm 介绍

Swarm 在 Docker 1.12 版本之前属于一个独立的项目，在 Docker 1.12 版本发布之后，该项目合并到了 Docker 中，成为 Docker 的一个子命令。目前，Swarm 是 Docker 社区提供的唯一一个原生支持 Docker 集群管理的工具。它可以把多个 Docker 主机组成的系统转换为单一的虚拟 Docker 主机，使得容器可以组成跨主机的子网网络。

Docker Swarm 是一个为 IT 运维团队提供集群和调度能力的编排工具。用户可以把集群中所有 Docker Engine 整合进一个「虚拟 Engine」的资源池，通过执行命令与单一的主 Swarm 进行沟通，而不必分别和每个 Docker Engine 沟通。在灵活的调度策略下，IT 团队可以更好地管理可用的主机资源，保证应用容器的高效运行。



## Docker Swarm 集群搭建

### 初始化manager节点

使用 `docker swarm init ` 初始化一个manager节点，并指定IP地址

```
docker swarm init --advertise-addr x.x.x.x
```

初始化完成后将返回如下信息

```
Swarm initialized: current node (uvqduzlmsjtx37wkyr557q94u) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-			1udlh5qgc2n7697gu22sb1nbwusest4eqsrmhbww341apsh4iw-ccovw1qs5fhsce8z5zki8zahd 192.168.1.250:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

### 子节点加入集群

拷贝上面的初始化返回结果中的命令

```
docker swarm join --token SWMTKN-1-			1udlh5qgc2n7697gu22sb1nbwusest4eqsrmhbww341apsh4iw-ccovw1qs5fhsce8z5zki8zahd 192.168.1.250:2377
```

并在需要加入集群的主机上执行

```
This node joined a swarm as a worker.
```

### 检查集群

```
docker node ls
```

这时将会看到有三台集群的swarm集群已经创建好了

![image-20180813092911814](/Users/bool/Documents/Docker笔记/image-20180813092911814.png)

### 可选项

一般来说，我们会将manager节点进行高可用配置。使用

1. ```
   docker node promote <node_id_of_a_worker>
   ```

   这里将第二台虚拟机提升为manager候选

   ```
   docker node promote server02
   ```

   返回如下信息提升节点成功

   ```
   Node server02 promoted to a manager in the swarm.
   ```

   注：命令必须在manager节点执行

   再次执行` docker node ls`可以看到`server02`已经被提升。当主节点server01宕机之后server02将被提升为Leader，类似于ZK的选举机制

   ![image-20180813093634171](/Users/bool/Documents/Docker笔记/image-20180813093634171.png)

### 部署portainer

#### 创建portainer数据卷

```
docker volume create portainer_data
```

#### 以服务的形式运行

```
docker service create \
--name portainer \
--publish 9000:9000 \
--replicas=1 \
--constraint 'node.role == manager' \
--mount type=bind,src=//var/run/docker.sock,dst=/var/run/docker.sock \
--mount type=volume,src=portainer_data,dst=/data \
portainer/portainer \
-H unix:///var/run/docker.sock
```

 



## 部署服务

### Docker stack

docker stack 是将容器提升了一级，称为服务。堆栈是一组相互关联的服务，它们共享依赖关系，并且可以协调和缩放在一起

### docker stack 命令

```
使用语法:	docker stack [选项] 命令

Manage Docker stacks

选项:
      --orchestrator string   Orchestrator to use (swarm|kubernetes|all)

命令:
  deploy      发布一个新的或者更新一个stack
  ls          stack 的列表
  ps          stack 中的任务列表
  rm          删除一个或多个 stacks
  services    stack 中的服务列表

Run 'docker stack COMMAND --help' for more information on a command.
```

#### docker stack deploy 命令

```
使用语法:	docker stack deploy [选项] 名称

选项:
  -c, --compose-file strings   编排文件路径
      --orchestrator string    Orchestrator to use (swarm|kubernetes|all)
```

示例: 发布一个stack。 使用当前路径下的docker-compose.yml文件发布一个名称为stack

```
docker stack deploy -c docker-compose.yml test
```

### stack.yml 文件

类似于单节点的docker主机，docker swarm也支持类似于docker compose的部署方式。

下面这张图片列出了最新的编排文件对应的docker版本:

![image-20180813165110465](/Users/bool/Documents/Docker笔记/image-20180813165110465.png)

