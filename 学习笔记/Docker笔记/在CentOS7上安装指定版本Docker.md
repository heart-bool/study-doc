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

```
apiVersion: kubeadm.k8s.io/v1beta2
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
---
apiServer:
  timeoutForControlPlane: 4m0s
  certSANs:
  - 192.168.1.221
  - 192.168.1.222
  - 192.168.1.223
  - 192.168.1.224
  - "cluster221"
  - "cluster222"
  - "cluster223"
apiVersion: kubeadm.k8s.io/v1beta2
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes

controllerManager: {}
dns:
  type: CoreDNS
etcd:
  external:
    endpoints:
    - https://192.168.1.221:2379
    - https://192.168.1.222:2379
    - https://192.168.1.223:2379
    caFile: /etc/etcd/ssl/ca.pem
    certFile: /etc/etcd/ssl/etcd.pem
    keyFile: /etc/etcd/ssl/etcd-key.pem
imageRepository: registry.cn-hangzhou.aliyuncs.com/bool-k8s
kind: ClusterConfiguration
kubernetesVersion: v1.16.2
controlPlaneEndpoint: "192.168.1.224:6443"
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.92.0.0/16
  podSubnet: 10.2.0.0/16
scheduler: {}
```

```
cat <<EOF | sudo tee /etc/systemd/system/etcd.service
[Unit]
Description=etcd
Documentation=https://github.com/coreos

[Service]
Type=notify
ExecStart=/usr/bin/etcd \\
  --name ${ETCD_NAME} \\
  --cert-file=/etc/etcd/ssl/etcd.pem \\
  --key-file=/etc/etcd/ssl/etcd-key.pem \\
  --peer-cert-file=/etc/etcd/ssl/etcd.pem \\
  --peer-key-file=/etc/etcd/ssl/etcd-key.pem \\
  --trusted-ca-file=/etc/etcd/ssl/ca.pem \\
  --peer-trusted-ca-file=/etc/etcd/ssl/ca.pem \\
  --peer-client-cert-auth \\
  --client-cert-auth \\
  --initial-advertise-peer-urls https://${ETCD_HOST_IP}:2380 \\
  --listen-peer-urls https://${ETCD_HOST_IP}:2380 \\
  --listen-client-urls https://${ETCD_HOST_IP}:2379,https://127.0.0.1:2379 \\
  --advertise-client-urls https://${ETCD_HOST_IP}:2379 \\
  --initial-cluster-token etcd-cluster-0 \\
  --initial-cluster cluster221=https://cluster221:2380,cluster222=https://cluster222:2380,cluster223=https://cluster223:2380 \\
  --initial-cluster-state new \\
  --data-dir=/var/lib/etcd
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF


etcdctl --cacert=/etc/etcd/ssl/ca.pem --cert=/etc/etcd/ssl/etcd.pem --key=/etc/etcd/ssl/etcd-key.pem --endpoints="https://192.168.1.221:2379,https://192.168.1.222:2379,https://192.168.1.223:2379" endpoint health

kubeadm reset
etcdctl \
  --endpoints="https://192.168.1.221:2379,https://192.168.1.222:2379,https://192.168.1.223:2379" \
  --cacert=/etc/etcd/ssl/ca.pem \
  --cert=/etc/etcd/ssl/etcd.pem \
  --key=/etc/etcd/ssl/etcd-key.pem \
    del /registry --prefix
```

```
kubeadm join 192.168.1.224:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:4d3e3d23e5e3f364550f2cb2ad19dde9c14bad5ad5c9f03658eabd3e4f105eb0 \
    --control-plane

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.1.224:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:4d3e3d23e5e3f364550f2cb2ad19dde9c14bad5ad5c9f03658eabd3e4f105eb0
```

