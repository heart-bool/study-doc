# 在CentOS7上安装指定版本Docker

## 1. 卸载旧版的Docker

```
yum remove -y docker*
```

## 2. 设置阿里云Docker的yum源

安装一些必要的软件

```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

配置阿里云docker-ce 的 yum源

```
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

## 3. 安装Docker

### 安装指定版本的Docker

查看Docker的版本列表

```
yum list docker-ce --showduplicates
```

指定安装的版本

```
yum install -y --setopt=obsoletes=0 \
   docker-ce-17.03.2.ce-1.el7.centos.x86_64 \
   docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch
   
```

安装最新的版本

```
yum install -y docker-ce
```

## 4. 启动Docker

```
systemctl enable docker
systemctl start docker
```

