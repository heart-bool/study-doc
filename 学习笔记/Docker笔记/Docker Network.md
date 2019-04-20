# Docker Network

## 网络驱动（Network Devers）

docker 默认情况下提供以下几个网络驱动程序:

- `bridge`：默认的驱动程序。
- `host`： 独立的网络驱动程序，直接使用宿主机器的网络。注：`host` 仅适用于Docker 17.06及更高版本上的群集服务。
- `overlay`：一般在集群的服务中使用。可以让集群内的所有容器具有相互通信的能力。
- `macvlan`：允许为容器网络分配mac地址，使驱动程序显示为网络中的物理设备
- `none`：对于当前容器禁用所有网络。
- `networking plugins`：通过安装使用第三方的网络插件。可以在`https://store.docker.com/search?category=network&q=&type=plugin` 进行搜索和安装

## Docker Network 命令

### `docker network` 命令

```
使用语法:	docker network COMMAND

命令:
  connect     将一个容器连接到一个网络驱动程序
  create      创建一个网络驱动程序
  disconnect  断开容器与网络驱动程序的连接
  inspect     显示网络驱动程序的详情
  ls          网络驱动列表
  prune       删除所有没有使用的网络驱动
  rm          删除一个或者多个网络驱动
```

### `docker network create` 命令

`docker network create` 命令可以指定子网、IP地址范围、网关和其他选项。使用 `docker network create --help` 命令查看所有的设置选项：

```
使用语法:	docker network create [OPTIONS] NETWORK

选项:
      --attachable           Enable manual container attachment
      --aux-address map      网络驱动使用的辅助IPv4或者IPV6地址。默认为 map[]
      --config-from string   从已有的网络驱动程序中复制配置
      --config-only          创建一个仅配置的网络驱动程序
  -d, --driver string        管理网络的驱动程序 (默认 "bridge")
      --gateway strings      主子网的IPV4或IPV6的网关
      --ingress              创建swarm的网状路由
      --internal             限制对网络的外部访问
      --ip-range strings     从 string 范围内为容器分配IP
      --ipam-driver string   IP地址的驱动管理程序 (默认 "default")
      --ipam-opt map         设置IPAM驱动程序特定选项 (默认 map[])
      --ipv6                 启用IPV6
      --label list           在一个网络上设置元数据
  -o, --opt map              设置驱动程序特定选项 (默认 map[])
      --scope string         控制网络的范围
      --subnet strings       CIDR格式的子网，代表网段
```

## Docker 网络的操作和使用

### bridge

#### 默认的bridge网络

默认情况下，在没有进行创建网络时，使用 `docker network ls` 命令可以看到如下内容：

```
NETWORK ID          NAME                DRIVER              SCOPE
c288dd79b62b        bridge              bridge              local
c704b416a1b3        host                host                local
513ea124d549        none                null                local
```

检查默认bridge 网络查看目前连接到网络的容器：

```
docker network inspect bridge
```

#### 用户自定义bridge

创建一个bridge网络：

```
docker network create user-net
```

再次使用`docker network ls` 命令可以看到在网络列表中多了一个网络`user-net`

```
NETWORK ID          NAME                DRIVER              SCOPE
c288dd79b62b        bridge              bridge              local
c704b416a1b3        host                host                local
513ea124d549        none                null                local
bf74b957b2dd        user-net            bridge              local
```

执行`docker network inspect user-net`检查`user-net`网络

```json
[
    {
        "Name": "user-net",
        "Id": "bf74b957b2dd2f89af65f5b89ec7d084d744e7f14c36f7642fd13b59c418b926",
        "Created": "2018-08-09T02:18:55.848621761+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
```

在启动一个容器时指定 `--network`参数

```
docker run --name eureka1 --network user-net 镜像名称

--name eureka1 指定容器的名字，方便以容器的名称进行访问
--network user-net 指定容器连接到 user-net网络
```

再次检查`user-net` 网络的详情，`docker network inspect user-net`

```json
[
    {
        "Name": "user-net",
        "Id": "bf74b957b2dd2f89af65f5b89ec7d084d744e7f14c36f7642fd13b59c418b926",
        "Created": "2018-08-09T02:18:55.848621761+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "c0b94d70ab0cde0f04d572d1d215a093e058e58b9ffa0ef832d1a8ea344e504c": {
                "Name": "apps_eureka1_1",
                "EndpointID": "d405f3b889ffd146cf9d97843564e95239c3597c...",
                "MacAddress": "02:42:ac:13:00:02",
                "IPv4Address": "172.19.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

可以看到启动的容器连接到该网络中并且自动分配了一个该网络的子网IP。如果多个容器同时连接到该网络，这些容器将可以使用IP进行通信，如果在运行容器时指定了容器的名称，还可以通过该名称进行通信。

