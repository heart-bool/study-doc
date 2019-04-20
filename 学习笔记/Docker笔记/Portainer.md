# Docker swarm Portainer 部署

### 部署 Portainer

#### 在Docker swarm集群中创建overlay网络

```
docker network create --driver overlay --attachable portainer_agent_network
```

#### 在集群中部署一个全局的 Portainer Agent

```
docker service create \
    --name portainer_agent \
    --network portainer_agent_network \
    -e AGENT_CLUSTER_ADDR=tasks.portainer_agent \
    --mode global \
    --constraint 'node.platform.os == linux' \
    --mount type=bind,src=//var/run/docker.sock,dst=/var/run/docker.sock \
    --mount type=bind,src=//var/lib/docker/volumes,dst=/var/lib/docker/volumes \
    portainer/agent
```

#### 以服务的形式部署 Portainer

```
docker service create \
    --name portainer \
    --network portainer_agent_network \
    --publish 19000:9000 \
    --replicas=1 \
    --constraint 'node.role == manager' \
    portainer/portainer -H "tcp://tasks.portainer_agent:9001" --tlsskipverify
```