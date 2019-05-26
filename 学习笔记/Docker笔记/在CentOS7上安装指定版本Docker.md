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
yum install -y docker-ce-18.06.3.ce-3.el7
   
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

## 5. 设置镜像加速器

```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://cxs1gh2d.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

