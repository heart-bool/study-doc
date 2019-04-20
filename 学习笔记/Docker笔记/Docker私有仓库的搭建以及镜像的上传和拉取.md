# Docker私有仓库的搭建以及镜像的上传和拉取

## 搭建Docker官方的私有库

1. 直接运行官方的私有库镜像

```
docker run -d -p 5000:5000 --restart always --name registry registry:2
注: 版本可修改 具体版本tag 参看文档 https://hub.docker.com/_/registry/
```

2. 如果registry没有在本地需要将registry添加到客户端的配置中

   1. 编辑本地镜像地址json文件

      ```
      vim /etc/docker/daemon.json :没有的话直接创建, 路径可以改变
      
      加入
      { 
        "registry-mirrors": ["https://cxs1gh2d.mirror.aliyuncs.com"]
      }
      
      sudo mkdir -p /etc/docker
      sudo tee /etc/docker/daemon.json <<-'EOF'
      {
        "registry-mirrors": ["https://cxs1gh2d.mirror.aliyuncs.com"]
      }
      EOF
      sudo systemctl daemon-reload
      sudo systemctl restart docker
      ```

   2. 编辑docker服务的配置文件,将第一步的json文件路径添加到该配置文件中

      ```
      vim /lib/systemd/system/docker.service
      
      添加以下文本
      EnvironmentFile=/etc/docker/daemon.json :路径为第一步我们编辑dameon.json的路径
      ```

   3. 重启docker

      ```
      systemctl daemon-reload
      systemctl restart docker
      ```

   ------

## 从私有仓库或其他仓库拉取镜像

docker pull 命令

```
语法:	docker pull [OPTIONS] NAME[:TAG|@DIGEST]

Options:
  -a, --all-tags                下载所有版本的镜像到本地仓库
      --disable-content-trust   跳过镜像的验证 默认为true
不指明tag时 总是pull最新的版本

示例: 从自建的docker仓库 192.168.2.128:5000 中拉取一个image
	docker pull 192.168.2.128:5000/hello-docker-java
```

## 将本地镜像上传至私有仓库或其他仓库

docker push

```
语法:  docker push [OPTIONS] NAME[:TAG]

Options:
      --disable-content-trust   跳过镜像的验证 默认为true
示例: 向自建docker仓库 192.168.2.128:5000 上传一个image
	docker push 192.168.2.128:5000/hello-docker-java
```
```
yum install -y https://mirrors.aliyun.com/docker-ce/linux/centos/7/x86_64/stable/Packages/docker-ce-selinux-17.03.0.ce-1.el7.centos.noarch.rpm
```

 

 

 

 

 