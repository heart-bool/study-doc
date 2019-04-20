# CentOS 免密登录配置(单主机免密登录其他主机)

## 1 准备主机

### 1.1 这里准备了三台主机

```
hdp-master
hdp-node-1
hdp-node-2
```

### 1.2 配置hosts映射文件

```
x.x.x.x hdp-master
x.x.x.x hdp-node-1
x.x.x.x hdp-node-2

#x.x.x.x 替换成IP地址
```

## 2 生成秘钥文件

### 2.1 在每台主机上生成秘钥文件

```shell
ssh-keygen -t rsa
```

注: 直接一路回车就行

### 2.2 分别在每台主机上制作`authorized_keys`文件

```shell
ssh-copy-id -i x.x.x.x
```

注: x.x.x.x 为当前主机的ip或者hosts中配置的主机名

### 2.3 选择需要免密访问其他主机的目标机器

例如这里是`hdp-master`需要免密访问另外两台主机，就将`hdp-master`制作的`authorized_keys`文件发送给另外的两台主机

```
scp -r ~/.ssh/authorized_keys x.x.x.x:~/.ssh
```

注: x.x.x.x 为当前主机的ip或者hosts中配置的主机名

## 3 测试

在`hdp-master`中

```
ssh hdp-node-1
ssh hdp-node-2
```

