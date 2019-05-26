# Rancher

## 安装Rancher

注意:

​	需要先安装docker

### 1. 单机模式

```
docker run -d --restart=unless-stopped -p 8080:8080 rancher/server
```

### 2. 集群模式

#### 2.1 创建数据库

```mysql
CREATE DATABASE IF NOT EXISTS cattle COLLATE = 'utf8_general_ci' CHARACTER SET = 'utf8';
GRANT ALL ON cattle.* TO 'cattle'@'%' IDENTIFIED BY '11111111';
GRANT ALL ON cattle.* TO 'cattle'@'localhost' IDENTIFIED BY '11111111';
```

#### 2.2 在不同主机执行相应命令

```shell
# 机器IP = 172.16.135.131
docker run -d \
	--restart=unless-stopped \
	-p 8080:8080 \
	-p 9345:9345 \
	--network=bridge \
	rancher/server:stable \
	--db-host 192.168.0.111 \
	--db-port 3306 \
	--db-user cattle \
	--db-pass 11111111 \
	--db-name cattle \
	--advertise-address 192.168.0.111
# 机器IP = 172.16.135.132
docker run -d \
	--restart=unless-stopped \
	-p 8080:8080 \
	-p 9345:9345 \
	rancher/server \
	--db-host 192.168.0.111 \
	--db-port 3306 \
	--db-user cattle \
	--db-pass cattle \
	--db-name cattle  \
	--advertise-address 192.168.0.112
```

