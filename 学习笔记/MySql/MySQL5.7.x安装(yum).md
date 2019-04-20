# yum安装MySQL

## 1 准备

### 1.1 下载并安装MySQL5.7.x 的 yum repo

```shell
#下载repo
wget https://repo.mysql.com//mysql57-community-release-el7-11.noarch.rpm
#安装repo
sudo rpm -Uvh mysql57-community-release-el7-11.noarch.rpm
```

### 1.2 检查系统中是否已存在mariadb并卸载

```shell
rpm -qa | grep mariadb
rpm -e --nodeps mariadb-*
```

## 2 安装和配置

### 2.1 安装

```shell
sudo yum install mysql-community-server
```

### 2.2 启动

```shell
sudo systemctl start mysqld.service
```

### 2.3 配置root密码

#### 2.3.1 获取默认密码

```shell
sudo grep 'temporary password' /var/log/mysqld.log
```

#### 2.3.2 修改密码

```shell
mysql -uroot -p
#MySQL默认策略为大小写字母数字特殊字符
set password root@localhost password('newpassword')
```

