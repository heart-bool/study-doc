# Kubernetes安装（多主集群、外置ETCD集群模式）

## 1. 安装准备

### 1.1 服务器

| IP地址        | 主机名     | 角色               |
| ------------- | ---------- | ------------------ |
| 192.168.1.221 | cluster221 | master，node，etcd |
| 192.168.1.222 | cluster222 | master，node，etcd |
| 192.168.1.223 | cluster223 | master，node，etcd |
| 192.168.1.224 | VIP        | VIP                |
| 192.168.1.191 | rancher01  |                    |

### 1.2 安装环境准备（所有机器执行）

```shell
# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

# 关闭swap，k8s不执行交换内存
swapoff -a 
sed -i 's/.*swap.*/#&/' /etc/fstab

###禁用Selinux
setenforce  0 
sed -i "s/^SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux 
sed -i "s/^SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config 
sed -i "s/^SELINUX=permissive/SELINUX=disabled/g" /etc/sysconfig/selinux 
sed -i "s/^SELINUX=permissive/SELINUX=disabled/g" /etc/selinux/config  

###报错请参考下面报错处理
modprobe br_netfilter   
cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
vm.swappiness=0
EOF
sysctl -p /etc/sysctl.d/k8s.conf
ls /proc/sys/net/bridge

###K8S源
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

###内核优化
echo "* soft nofile 204800" >> /etc/security/limits.conf
echo "* hard nofile 204800" >> /etc/security/limits.conf
echo "* soft nproc 204800"  >> /etc/security/limits.conf
echo "* hard nproc 204800"  >> /etc/security/limits.conf
echo "* soft  memlock  unlimited"  >> /etc/security/limits.conf
echo "* hard memlock  unlimited"  >> /etc/security/limits.conf

###kube-proxy开启ipvs的前置条件
# 原文：https://github.com/kubernetes/kubernetes/blob/master/pkg/proxy/ipvs/README.md
# 参考：https://www.qikqiak.com/post/how-to-use-ipvs-in-kubernetes/

# 加载模块 <module_name>
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4

# 检查加载的模块
lsmod | grep -e ipvs -e nf_conntrack_ipv4
# 或者
cut -f1 -d " "  /proc/modules | grep -e ip_vs -e nf_conntrack_ipv4

#所有node节点安装ipvsadm
yum install ipvsadm -y
ipvsadm -l -n
```

#### 1.3 安装Docker-CE

#### 1.3.1 配置阿里云docker-ce 的 yum源

```shell
yum install -y yum-utils 
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum makecache fast
```

#### 1.3.2 安装Docker-CE

```shell
yum install -y --setopt=obsoletes=0 docker-ce-18.06.3.ce
systemctl start docker
systemctl enable docker
```

#### 1.3.3 设置加速器

```shell
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://cxs1gh2d.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

#### 1.3.4 安装kubeadm kubectl kubelet

```
yum install kubeadm-1.16.2 kubectl-1.16.2 kubelet-1.16.2 -y
```



## 2 安装ETCD

### 2.1 生成TLS证书和秘钥

#### 2.1.1 安装CFSSL

```shell
yum install wget -y
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
chmod +x cfssl_linux-amd64
mv cfssl_linux-amd64 /usr/local/bin/cfssl
chmod +x cfssljson_linux-amd64
mv cfssljson_linux-amd64 /usr/local/bin/cfssljson
chmod +x cfssl-certinfo_linux-amd64
mv cfssl-certinfo_linux-amd64 /usr/local/bin/cfssl-certinfo
export PATH=/usr/local/bin:$PATH
```

#### 2.1.2 创建CA文件,生成etcd证书

- Cluster221 执行

```shell
mkdir /root/ssl
cd /root/ssl
cat >  ca-config.json <<EOF
{
"signing": {
"default": {
  "expiry": "87600h"
},
"profiles": {
  "kubernetes-Soulmate": {
    "usages": [
        "signing",
        "key encipherment",
        "server auth",
        "client auth"
    ],
    "expiry": "87600h"
  }
}
}
}
EOF

cat >  ca-csr.json <<EOF
{
"CN": "kubernetes-Soulmate",
"key": {
"algo": "rsa",
"size": 2048
},
"names": [
{
  "C": "CN",
  "ST": "shanghai",
  "L": "shanghai",
  "O": "k8s",
  "OU": "System"
}
]
}
EOF

cfssl gencert -initca ca-csr.json | cfssljson -bare ca

#hosts项需要加入所有etcd集群节点，建议将所有node也加入，便于扩容etcd集群。
cat > etcd-csr.json <<EOF
{
  "CN": "etcd",
  "hosts": [
    "127.0.0.1",
    "192.168.1.221",
    "192.168.1.222",
    "192.168.1.223",
    "192.168.1.224",
    "cluster221",
    "cluster222",
    "cluster223"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "shanghai",
      "L": "shanghai",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
EOF

cfssl gencert -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=kubernetes-Soulmate etcd-csr.json | cfssljson -bare etcd
```

#### 2.1.3 分发证书到所有节点

本教程中共3台K8S机器都作为ETCD节点，故发送到所有节点

- Cluster221上执行

```shell
mkdir -p /etc/etcd/ssl
cp etcd.pem etcd-key.pem ca.pem /etc/etcd/ssl/
scp -r /etc/etcd/ Cluster222:/etc/
scp -r /etc/etcd/ Cluster223:/etc/
```

#### 2.2 安装etcd

本教程中安装的k8s版本为v1.16.2，官方对应的etcd版本为3.3.15，其他版本etcd未测试

### 2.2.1 下载安装etcd

```shell
# 下载地址
mkdir etcd && cd etcd
wget https://github.com/etcd-io/etcd/releases/download/v3.3.15/etcd-v3.3.15-linux-amd64.tar.gz
# 解压并拷贝文件
tar -zxvf etcd-v3.3.15-linux-amd64.tar.gz
cp etcd-v3.3.15-linux-amd64/etcd /usr/bin/
cp etcd-v3.3.15-linux-amd64/etcdctl /usr/bin/
```

### 2.2.2 etcd配置文件准备

分别在3台机器上执行

- cluster221: 

  ```shell
  ETCD_NAME=cluster221
  ETCD_HOST_IP=192.168.1.221
  
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
  ```

- cluster222

  ```shell
  ETCD_NAME=cluster222
  ETCD_HOST_IP=192.168.1.222
  
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
  ```

- cluster223

  ```shell
  ETCD_NAME=cluster223
  ETCD_HOST_IP=192.168.1.223
  
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
  ```

### 2.2.3 启动etcd

```shell
systemctl daemon-reload
systemctl enable etcd
systemctl start etcd
```

### 2.2.4 验证etcd集群

```shell
echo "export ETCDCTL_API=3" >>/etc/profile  && source /etc/profile
etcdctl --cacert=/etc/etcd/ssl/ca.pem --cert=/etc/etcd/ssl/etcd.pem --key=/etc/etcd/ssl/etcd-key.pem --endpoints="https://192.168.1.221:2379,https://192.168.1.222:2379,https://192.168.1.223:2379" endpoint health

##### 显示如下则成功
https://192.168.1.221:2379 is healthy: successfully committed proposal: took = 28.190865ms
https://192.168.1.223:2379 is healthy: successfully committed proposal: took = 28.585104ms
https://192.168.1.222:2379 is healthy: successfully committed proposal: took = 29.899499ms
```

## 3 安装配置Keppalived

### 3.1 安装Keppalived

```
yum install keepalived -y
```

### 3.2 配置Keppalived

- cluster221

  ```shell
  cat <<EOF >/etc/keepalived/keepalived.conf
  global_defs {
     router_id LVS_k8s
  }
  
  vrrp_script CheckK8sMaster {
      script "curl -k https://192.168.1.224:6443"    #VIP Address
      interval 3
      timeout 9
      fall 2
      rise 2
  }
  
  vrrp_instance VI_1 {
      state MASTER
      interface ens32       #Your Network Interface Name
      virtual_router_id 61
      priority 120          #权重，数字大的为主，数字一样则选择第一台为Master
      advert_int 1
      mcast_src_ip 192.168.1.221  #local IP
      nopreempt
      authentication {
          auth_type PASS
          auth_pass sqP05dQgMSlzrxHj
      }
      virtual_ipaddress {
          192.168.1.224    # VIP
      }
      track_script {
          CheckK8sMaster
      }
  }
  EOF
  ```

- cluster222

  ```shell
  cat <<EOF >/etc/keepalived/keepalived.conf
  global_defs {
     router_id LVS_k8s
  }
  
  vrrp_script CheckK8sMaster {
      script "curl -k https://192.168.1.224:6443"    #VIP Address
      interval 3
      timeout 9
      fall 2
      rise 2
  }
  
  vrrp_instance VI_1 {
      state MASTER
      interface ens32       #Your Network Interface Name
      virtual_router_id 61
      priority 110          #权重，数字大的为主，数字一样则选择第一台为Master
      advert_int 1
      mcast_src_ip 192.168.1.222  #local IP
      nopreempt
      authentication {
          auth_type PASS
          auth_pass sqP05dQgMSlzrxHj
      }
      virtual_ipaddress {
          192.168.1.224    # VIP
      }
      track_script {
          CheckK8sMaster
      }
  }
  EOF
  ```

- cluster223

  ```shell
  cat <<EOF >/etc/keepalived/keepalived.conf
  global_defs {
     router_id LVS_k8s
  }
  
  vrrp_script CheckK8sMaster {
      script "curl -k https://192.168.1.224:6443"    #VIP Address
      interval 3
      timeout 9
      fall 2
      rise 2
  }
  
  vrrp_instance VI_1 {
      state MASTER
      interface ens32       #Your Network Interface Name
      virtual_router_id 61
      priority 100          #权重，数字大的为主，数字一样则选择第一台为Master
      advert_int 1
      mcast_src_ip 192.168.1.223  #local IP
      nopreempt
      authentication {
          auth_type PASS
          auth_pass sqP05dQgMSlzrxHj
      }
      virtual_ipaddress {
          192.168.1.224    # VIP
      }
      track_script {
          CheckK8sMaster
      }
  }
  EOF
  ```

  ### 3.3 启动并验证Keppalived

  ```shell
  systemctl enable keepalived
  systemctl start keepalived
  #在所有节点执行 检查是否有VIP192.168.1.224
  ip a
  ```

  ## 4 安装kubernetes集群

  ### 4.1 准备kubeadm配置文件

  ```shell
  cd ～ && cat <<EOF config.yaml
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
  EOF
  ```

  ### 4.2 初始化cluster221

  ```
  kubeadm init --config config.yaml
  ```

  - 初始化成功后输出信息：

    ```shell
    Your Kubernetes master has initialized successfully!
    
    To start using your cluster, you need to run the following as a regular user:
    
      mkdir -p $HOME/.kube
      sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
      sudo chown $(id -u):$(id -g) $HOME/.kube/config
    
    You should now deploy a pod network to the cluster.
    Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
      https://kubernetes.io/docs/concepts/cluster-administration/addons/
    
    You can now join any number of machines by running the following on each node
    as root:
    
      kubeadm join 172.16.1.49:6443 --token b99a00.a144ef80536d4344 --discovery-token-ca-cert-hash sha256:8c
    ```

  - 执行上面提示的命令

    ```shell
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
    ```

  - 初始化成功将生成的证书拷贝到其他节点，目标机器没有目录则创建

    ```
    scp -r /etc/kubernetes/pki  cluster222:/etc/kubernetes/
    scp -r /etc/kubernetes/pki  cluster223:/etc/kubernetes/
    scp ～/config.yaml  cluster222:~
    scp ～/config.yaml  cluster223:~
    ```

  ### 4.3 初始化cluster222、cluster223

  ```
  kubeadm init --config config.yaml
  ```

  - 初始化失败则执行

    ```shell
    kubeadm reset
    etcdctl \
  --endpoints="https://192.168.1.221:2379,https://192.168.1.222:2379,https://192.168.1.223:2379" \
      --cacert=/etc/etcd/ssl/ca.pem \
      --cert=/etc/etcd/ssl/etcd.pem \
      --key=/etc/etcd/ssl/etcd-key.pem \
        del /registry --prefix
    ```
    
  
  ### 4.4 Flannel组件部署
  
  ```
  wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
  ```
  
  - 修改网段
  
    ```
    net-conf.json: |
    {
    	"Network": "10.2.0.0/16",
    	"Backend": {
    		"Type": "vxlan"
    	}
    }
    ```
  
    