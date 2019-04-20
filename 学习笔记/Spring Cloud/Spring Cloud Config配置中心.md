# Spring Cloud Config配置中心

## 概述

### 为什么需要配置中心

​	在微服务的环境下，当我们的微服务配置越来越多的时候，配置文件的管理问题就凸现出来了。这时，就需要这样一个统一的配置文件管理中心。

### Spring Cloud Config 

​	Spring Cloud的一个配置中心的组件，提供统一的配置文件管理、实时更新等功能。

​	在本教程中将使用git作为 Spring Cloud Config 配置中心的配置存储工具。当然其也支持内存、本地存储系统。

## 开始搭建服务

这里主要演示基本的config-server。消息总线的动态配置刷新，会在后续中添加

#### 1. 创建config-server

​	这里简述一下 spring cloud config 中微服务配置文件获取的流程(和注册中心协作)。

​	首先在微服务启动的时候，应用会根据我们在 bootstrap.yml 文件中配置的文件路径获取根据一些命名规则定义的配置文件，如果使用了注册中心，应用将到注册中心查找对应的config server。然后，应用会下载这些配置文件到本地系统并在应用启动的时候加载这些配置。

#### 2. 创建spring boot 应用  并添加依赖

这里将继续以子项目的形式创建新项目，我使用的是IDEA的spring init.. 方式创建的，创建完成后修改<parent>依赖，完整的pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.tifangedu</groupId>
        <artifactId>tifang-project</artifactId>
        <version>1.0.0</version>
    </parent>
    <groupId>com.tifangedu.base</groupId>
    <artifactId>tifang-base-config</artifactId>
    <version>${tifang.service.version}</version>
    <packaging>jar</packaging>

    <name>tifang-base-config</name>
    <description>配置中心</description>

    <dependencies>
        <!--添加依赖-->
       <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.1</version>
                <configuration>
                    <!-- 一般而言，target与source是保持一致的，但是，有时候为了让程序能在其他版本的jdk中运行(对于低版本目标jdk，源代码中不能使用低版本jdk中不支持的语法)，会存在target不同于source的情况 -->
                    <source>1.8</source> <!-- 源代码使用的JDK版本 -->
                    <target>1.8</target> <!-- 需要生成的目标class文件的编译版本 -->
                    <encoding>UTF-8</encoding><!-- 字符集编码 -->
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <goals>
                            <goal>build-info</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>

```

```
提示
	如果不使用子项目的方式，直接使用spring boot 的<parent> 也是可以的。
	否则请检查父pom文件中的
	<modules>
        <module>模块名</module>
    </modules>
    中是否有
    <module>创建module指定的名称</module>
    没有的话手动添加
```

#### 3. 编写配置文件

```yml
server:
  port: 8861 #指定端口

spring:
  application:
    name: config-server  #指定服务名称

# config server 配置，这里配置GIT
  cloud: 
    config:
      discovery: #启用springcloud 服务发现能力并指定该服务在注册中心的唯一id
        enabled: true
        service-id: ${spring.application.name}
      server:
        git: #git仓库相关配置
          uri: http://自行自行替换成你自己的仓库.git
          searchPaths: config-repo
          skipSslValidation: true
          username: wangfeng
          password: wangfeng
          default-label: ${GIT_LABLE}
      retry:
        max-attempts: 2
        max-interval: 2000
  profiles:
    active: dev
#  注册中心配置 并指定该服务在注册中心的唯一id，所有请求将使用这个唯一id，也就是${spring.application.name}
eureka:
  instance:
    leaseRenewalIntervalInSeconds: 10
    health-check-url-path: /actuator/health
    prefer-ip-address: false
    hostname: ${spring.application.name}
    instance-id: ${spring.application.name}:${server.port}
  client:
    registryFetchIntervalSeconds: 60
    serviceUrl:
      defaultZone: http://eureka-server-1:8761/eureka/,http://eureka-server-2:8762/eureka/
```

#### 4. 启动

在spring boot 应用的启动类上引入`@EnableConfigServer`注解。依次启动上一篇创建的两个注册中心，再启动config-server。

```
提示：对spring boot不熟悉的同学请自行学习
```

#### 5. 测试

在指定Git仓库中新建一个yml文件，内容随意，我这里有现成的，新建过程就不说了。配置文件的读取规则，在spring cloud config中，有以下几种方式获取配置文件：

```
/{application}/{profile}[/{label}]  	
	-----服务器地址/应用/环境名[/分支名(可选项)]
/{application}-{profile}.yml			
	-----服务器地址/应用/环境名.配置文件后缀
/{label}/{application}-{profile}.yml	
	-----服务器地址/分支名/应用-环境名.配置文件后缀
/{application}-{profile}.properties
	-----服务器地址/应用/环境名.配置文件后缀
/{label}/{application}-{profile}.properties
	-----服务器地址/分支名/应用/环境名.配置文件后缀
```

这里我做一个演示:

```http
http://ip或域名:configserver的端口/配置文件名-环境.yml
```

演示的请求为：

```http
http://localhost:8861/service-message-dev.yml
```

请求结果：

```yml
logging:
  file: logs/message/app.log
  pattern:
    file: '%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(%5p) %clr(${PID}){magenta}
      %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint}
      %m%n%wEx'
spring:
  cloud:
    bus:
      trace:
        enabled: true
  rabbitmq:
    addresses: rabbitmq
    password: admin123
    port: 5672
    username: admin
```



#### 涉及到加密之类的配置请移步官方文档

```http
http://cloud.spring.io/spring-cloud-config/single/spring-cloud-config.html
```

