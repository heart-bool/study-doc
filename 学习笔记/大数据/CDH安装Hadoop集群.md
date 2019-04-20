# CDH安装Hadoop集群

## 1 环境准备

### 1.1 版本信息

- Java:	jdk1.8.0_181
- CDH:       CM 6.0.1
- OS:          CentOS 7.4

### 1.2 机器准备

```
172.16.135.51 hdp-master
172.16.135.52 hdp-node-1
172.16.135.53 hdp-node-2
```

#### 1.2.1 关闭 SELINUX

```
vim /etc/selinux/config

将
SELINUX=enforcing
改为
SELINUX=disabled
```

#### 1.2.2 关闭防火墙

```shell
systemctl stop firewalld.service #停止firewall
```

#### 1.3 使用chrony进行时间同步

##### 1.3.1 开启chrony服务

```shell
sudo systemctl enable chronyd.service
sudo systemctl start chronyd.service
```

##### 1.3.2 设置时区

```shell
sudo timedatectl set-timezone Asia/Shanghai
```

##### 1.3.3 同步系统时间

```shell
sudo chronyc -a makestep
```

##### 1.3.4 选择一台主服务器作为其他节点服务器的同步服务器，编辑

```shell
sudo vim /etc/chrony.conf

# 注释掉前面四行
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
# server 0.centos.pool.ntp.org iburst
# server 1.centos.pool.ntp.org iburst
# server 2.centos.pool.ntp.org iburst
# server 3.centos.pool.ntp.org iburst
# 加入以下内容
server ntp1.aliyun.com iburst
allow 172.16.135.51/24
local stratum 10
```

##### 1.3.5 重启服务

```shell
sudo systemctl restart chronyd.service
sudo chronyc -a makestep
sudo chronyc sourcestats
sudo chronyc sources -v
```

##### 1.3.6 配置节点服务器

```shell
sudo vim /etc/chrony.conf

# 注释掉前面四行
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
# server 0.centos.pool.ntp.org iburst
# server 1.centos.pool.ntp.org iburst
# server 2.centos.pool.ntp.org iburst
# server 3.centos.pool.ntp.org iburst
# 加入以下内容
server 172.16.135.51

#之后执行
sudo systemctl restart chronyd.service
sudo chronyc -a makestep
sudo chronyc sourcestats
sudo chronyc sources -v
```



#### 1.4 配置集群的免密登录

```
参照笔记根目录下的 CentOS免密登录配置.md
```

#### 1.5 配置专用的用户(可选)

```
adduser xxx
passwd xxx
```

#### 1.6 准备安装包

```
cdh6.1.0 离线包：
CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel
CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel.sha256
manifest.json
下载： https://archive.cloudera.com/cdh6/6.1.0/parcels/ 并保存到 /var/www/html/ 文件夹下，没有就新建

cdh6 的CM 包:
cloudera-manager-agent-6.1.0-769885.el7.x86_64.rpm
cloudera-manager-daemons-6.1.0-769885.el7.x86_64.rpm
cloudera-manager-server-6.1.0-769885.el7.x86_64.rpm
cloudera-manager-server-db-2-6.1.0-769885.el7.x86_64.rpm
oracle-j2sdk1.8-1.8.0+update141-1.x86_64.rpm
allkeys.asc

下载地址：https://archive.cloudera.com/cm6/6.1.0/redhat7/yum/RPMS/x86_64/ 并保存到 /var/www/html/ 文件夹下，没有就新建

jdbc 驱动：
mysql-connector-java-8.0.15-1.el7.noarch.rpm

下载：mysql官网下载
```

#### 1.7 使用httpd搭建本地repo镜像 

##### 1.7.1 安装httpd

```
sudo yum install httpd -y
```

##### 1.7.2 修改http配置文件

```
sudo vim /etc/httpd/conf/httpd.conf

添加: AddType application/x-gzip .gz .tgz .parcel
```

注：在1.6步骤中如果有将对应的文件放置到 `/var/www/html`下则直接启动httpd，否则先拷贝文件再启动httpd

正常情况下可以看到如下

![image-20190409233946344](/Users/bool/Library/Application Support/typora-user-images/image-20190409233946344.png)

##### 1.7.3 创建repo文件

```
sudo vim /etc/yum.repos.d/cm.repo #新建repo

#拷贝如下内容 注意替换httpd的主机ip
------
[cmrepo]
name = cm_repo
baseurl =http://172.16.135.51/cm6.1
enable = true
gpgcheck = false
-----

#生成 yum 缓存
sudo yum makecache 
```

##### 1.7.3 将新建的repo文件拷贝到其他主机

```
scp /etc/yum.repos.d/cm.repo xx@xx:/etc/yum.repos.d/

#生成 yum 缓存
sudo yum makecache
```

![image-20190409234701857](/Users/bool/Library/Application Support/typora-user-images/image-20190409234701857.png)

#### 1.8 配置MySQL-jdbc

```shell
wget https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-8.0.15-1.el7.noarch.rpm

sudo rpm -ivh mysql-connector-java-8.0.15-1.el7.noarch.rpm
cd /usr/share/java/
cp -p mysql-connector-java-8.0.15.jar  mysql-connector-java.jar

wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.46.tar.gz
tar zxvf mysql-connector-java-5.1.46.tar.gz
mkdir -p /usr/share/java/
cd mysql-connector-java-5.1.46
cp mysql-connector-java-5.1.46-bin.jar /usr/share/java/mysql-connector-java.jar
```

## 2 安装

### 2.1 安装java

```http
https://www.cnblogs.com/caosiyang/archive/2013/03/14/2959087.html
```

### 2.2 安装MySQL

#### 2.2.1 参考

```
/Users/bool/Documents/学习笔记/MySql/MySQL5.7.x安装(yum).md
```

#### 2.2.2 在 mysql 当中创建 CM 需要的注册库

```shell
# mysql -uroot -p密码
mysql> create database cmf character set utf8;
mysql> grant all privileges on cmf.* to 'cmf'@'%' identified by '密码' with grant option;
mysql> grant all privileges on cmf.* to 'cmf'@'NN01.yl.com' identified by '密码' with grant option;
mysql> flush privileges;
```

#### 2.2.3 注入CM-server库 与 CM-agent端的server

```shell
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql cmf cmf cmf用户的密码
```

### 2.3 安装cdh

#### 2.3.1 安装`cloudera-manager-server` 

```shell
sudo yum install -y cloudera-manager-server 
```

#### 2.3.2 安装启动CM

```
sudo service cloudera-scm-server start 
cd /var/log/cloudera-scm-server/
tail -f cloudera-scm-server.log
```

`Cloudera Manager` 默认密码:

```
username: admin
password: admin
```

