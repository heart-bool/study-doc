Docker



Docker Engin

​	Docker server

​	Rest Api Server

​	Cli接口



镜像 Image:

​	文件和meta data的集合，分层的 并且每一层都可以添加改变删除文件 成为一个新的Image 不同的Image 可以共享相同的分层 并且Image本身是只读的

​	创建Image

​		1. 编写Dockerfile	

​		2. 使用 build 命令执行创建Image

容器 

​	容器是运行Image的环境

​	一些命令

​		docker rm $(docker container ls -aq)	删除所有的容器

​		docker rm $(docker container ls -f "status=exited" -q) 		删除所有的容器

​		docker container commit == docker commit

​		docker image build == docker build

​	Dockerfile：

​		FROM  base Image：build 新Image的基础Image

​			FROM centos： 使用centos 作为基础Image build 新的Image

​		LABE 注释

​		RUN :  在Image中安装或运行命令，为了避免无用分层，尽量将多条命令合并成一行

​		WORKDIR：设定当前工作目录，类似cd 切换到目标目录执行操作

​			WORKDIR /test 

​			WORKDIR demo

​			RUN pwd ：输出 /test/demo

​		ADD ：添加文件到指定目录 和 COPY的区别: 可以对压缩文件进行解压缩

​		ENV：设置环境变量

​		VOLUME：

​		EXPOSE：

​		RUM CMD ENTRYPOINT 三个命令的区别

​			RUN 执行命令并创建新的Image layer

​								

​			CMD 设置容器启动后迷人执行的命令个参数

​				容器启动时默认执行的命令，如果docker run 指定了其他命令， CMD命令被忽略，

​				如果定义	了多个CMD 只有最后一个会被执行

​			ENTRYPOINT 设置容器启动时运行的命令

​				让容器以应用程序或者服务的形式运行，不会被忽略，一定会执行

​				比如启动一个数据库的服务，启动一个微服务如springcloud应用等

​			Shell 格式 将命令当成shell命令执行

​				RUN yum install -y vim

​				CMD echo “xxxx”

​				ENTRYPOINT echi "xxxx"

​			Exec 特定的格式指明运行的命令以及命令的参数

​				RUN ["yum","install","-y","vim"]					

​				CMD ["echo", "XXX"]

​				ENTRYPOINT ["echo", "xxx"]

Registry



Namespace

Control groups

Union file systems



