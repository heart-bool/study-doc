# CentOS 常用命令和配置

## 设置阿里云yum源

1. 备份

   ```
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   ```

2. 下载repo

   ```
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   ```

3. 运行yum makecache生成缓存

4. 安装yum源

   ```
   yum install https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
   ```

## SSH相关

### 清除ssh密钥缓存

在使用ssh连接之前连接过的服务器出现以下信息时：

```shell
➜  ~ ssh root@192.168.1.161
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:SmKlJAuLgD2n6iSMcTd9tTJtsIKKwukSttN8Xd9Dlec.
Please contact your system administrator.
Add correct host key in /Users/bool/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /Users/bool/.ssh/known_hosts:26
ECDSA host key for 192.168.1.161 has changed and you have requested strict checking.
Host key verification failed.
```

解决办法

```
ssh-keygen -R 服务器端的ip地址
```

会提示以下信息

```shell
➜  ~ ssh-keygen -R 192.168.1.161
# Host 192.168.1.161 found: line 26
/Users/bool/.ssh/known_hosts updated.
Original contents retained as /Users/bool/.ssh/known_hosts.old
```

重新登录时

```shell
The authenticity of host '192.168.1.161 (192.168.1.161)' can't be established.
RSA key fingerprint is da:f7:3e:ba:f7:00:e6:44:76:f2:58:6e:48:**.
Are you sure you want to continue connecting (yes/no)?
```

## 网络相关

### 防火墙相关

#### CentOS-7 FRIEWALL

1. ```
   sudo systemctl stop firewalld.service #停止firewall
   sudo systemctl disable firewalld.service #禁止firewall开机启动
   firewall-cmd --version #查看版本
   firewall-cmd --help #查看帮助
   firewall-cmd --state #显示状态
   firewall-cmd --zone=dmz --list-ports #查看所有打开的端口
   firewall-cmd --get-active-zones #查看区域信息
   firewall-cmd --get-zone-of-interface=eth0 #查看指定接口所属区域
   firewall-cmd --panic-on #拒绝所有包
   firewall-cmd --panic-off #取消拒绝状态
   firewall-cmd --query-panic #查看是否拒绝
   firewall-cmd --reload #更新防火墙规则
   firewall-cmd --complete-reload #更新防火墙规则
   systemctl restart firewalld #重启防火墙
   systemctl enable firewalld #开机启动
   sudo firewall-cmd --zone=public --add-port=3000/tcp --permanent 开放端口
   sudo firewall-cmd --reload 重新加载配置文件
   ```

## 系统相关

### hostname

#### 查看主机名

```
hostnamectl --static
hostnamectl --transient
hostnamectl --pretty
```

#### 设置所有主机名

```shell
hostnamectl set-hostname xxx
```

### SELINUX

#### 查看selinux状态

```
/usr/sbin/sestatus -v
```

#### 修改selinux状态

```
vim /etc/selinux/config

将	SELINUX=enforcing	改为	SELINUX=disabled
```

### 时间同步

1. 安装ntp

   ```shell
   sudo yum install ntp -y
   ```

2. 启动ntp

   ```shell
   service ntpd start
   ```

3. 设置开机启动

   ```shell
   chkconfig ntpd on
   ```