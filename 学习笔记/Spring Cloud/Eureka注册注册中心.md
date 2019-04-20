# Eureka

教程记录公司APP后端项目。整体微服务的开发都将使用Spring Cloud作为微服务来开发，采用Docker Swarm进行部署，后期可能会采用kubernetes进行部署。目前考虑集成Jenkins或者使用gitlab的CICD进行自动化部署测试等DevOps的解决方案，后面逐步的也会加入到教程中。

想写这个教程也是想记录在使用Spring Cloud的时候遇到的一些问题，以及解决的方式



## 项目部分介绍

为了以后打包部署（这里的打包部署主要是针对于各种开发环境，例如测试 开发 预发布 生产等，环境的区分是使用Git在不同的分支上进行开发，利用Spring boot 提供的profiles一次性将所有环境配置写好，再根据不同的环境变量编写对应Docker compose文件，这样可以避免在Git上进行分支合并时的配置文件切换的麻烦），项目主要分为两个部分，一个是基础服务部分，涉及到以下服务：

- 注册中心： 这里使用Eureka
- 配置中心： Spring Cloud Config
- 监控中心： Spring Boot Admin
- 路由网关： Gateway

目前暂定的是这些，至于以后要加的组件，会根据实际情况进行集成

## 注意事项

- 整个项目中的服务地址除了需要对外开放的IP，内部服务的访问方式将采用服务名称来访问。具体的配置会在配置文件中体现。
- 教程中Spring cloud 的版本将使用最新版本 Finchley.RELEASE

## 搭建Spring Cloud Eureka服务注册发现中心

快速的搭建Spring Cloud项目最简单的方式是使用官方提供的Spring Initializr。目前Idea 已经集成了这个功能，作为入门的方式会更容易上手。这里由于是实际的项目，所有才有手动的方式来构建

### 1. 创建Maven父项目

创建一个Maven的项目并将其pom文件设置为：

```java
<packaging>pom</packaging>
```

添加依赖

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.tifangedu</groupId>
    <artifactId>tifang-project</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>
    <name>tifang-project</name>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.3.RELEASE</version>
    </parent>

    <modules>
        <module>tifang-base-eureka</module>
    </modules>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring.cloud.version>Finchley.RELEASE</spring.cloud.version>
        <java.version>1.8</java.version>
        <project.version>1.0.0</project.version>
        <lombok.version>1.16.20</lombok.version>
        <spring.boot.admin.version>2.0.1</spring.boot.admin.version>
    </properties>

	<!-- 在父pom文件中引入公共的依赖，避免在子项目中重复的拷贝 -->
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
    </dependencies>
    
     <!-- 
        增加依赖管理，目的是在子项目中可以引入需要的依赖。例如有的项目需要Spring WebMvc的依赖
    	而有的不需要，还有一个好处是以后版本升级会比较方便，只需要改父pom文件中相关的版本号就可以了
    -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>de.codecentric</groupId>
                <artifactId>spring-boot-admin-starter-client</artifactId>
                <version>${spring.boot.admin.version}</version>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring.cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>de.codecentric</groupId>
                <artifactId>spring-boot-admin-starter-server</artifactId>
                <version>${spring.boot.admin.version}</version>
                <type>jar</type>
            </dependency>
            <dependency>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>${lombok.version}</version>
                <type>jar</type>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.projectlombok</groupId>
                    <artifactId>lombok-maven-plugin</artifactId>
                    <version>1.16.6.1</version>
                </plugin>
            </plugins>
        </pluginManagement>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.1</version>
                <configuration>
                    <source>1.8</source> <!-- 源代码使用的JDK版本 -->
                    <target>1.8</target> <!-- 需要生成的目标class文件的编译版本 -->
                    <encoding>UTF-8</encoding><!-- 字符集编码 -->
                </configuration>
            </plugin>
        </plugins>
        <defaultGoal>[clean,package]</defaultGoal>
    </build>
</project>
```

这样父pom就创建好了下面就来创建一个子项目

### 2.创建eureka-server子项目

具体的创建过程就不细说了 直接上pom

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
    <artifactId>tifang-base-eureka</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>tifang-base-eureka</name>
    <description>注册中心</description>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
        <dependency>
            <groupId>de.codecentric</groupId>
            <artifactId>spring-boot-admin-starter-client</artifactId>
        </dependency>
    </dependencies>
    
    <!-- 子项目单独再配置是因为以后可能会存在不使用父pom打包 而是单独的项目打包 -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.1</version>
                <configuration>
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

注： 在Spring boot 2.x版本中，启动类上不再一定需要使用特定注解来启动Spring Cloud组件。例如eureka：

```java
@SpringBootApplication
@EnableEurekaServer  // 在2.x以后，如果类路径下有eureka的jar包，不使用该注解也是可以的
public class TifangBaseEurekaApplication {

	public static void main(String[] args) {
		SpringApplication.run(TifangBaseEurekaApplication.class, args);
	}
}
```

### 3.添加配置 application.yml

#### 高可用Eureka

对于Eureka的基础知识这里不会详细说明。具体来说，Eureka的高可用有两种方式，第一种是利用多容器的副本数量来启动Eureka服务，这种方式在Eureka的web页面不会看到eureka的注册信息。第二种是指定启动多个eureka容器，然后每个eureka向其他所有eureka注册，需要注意的是所有的eureka将定义相同的应用名，通过

`spring.application.name`设置。本文将使用两个eureka服务

#### 编写通用配置

```yml
spring:
  profiles:
    active: 1 # 激活环境为 1的配置文件。自行了解 spring boot profiles
#配置管理暴露的接口，这暴露所有的管理接口
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: ALWAYS
#日志配置
logging:
  file: "logs/eureka/app.log"
  pattern:
    file: "%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(%5p) %clr(${PID}){magenta} %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m%n%wEx"
```

#### 编写第一个eureka配置文件

由于上面我们指定了spring.profiles.active=1 所以这里的配置文件将命名为 application-1.yml。也就是说，当指定spring.profiles.active=string 相应的就需要命名一个 application-string.yml。多个使用不同的 string 就可以了

```yml
server:
  port: 8761
eureka:
  server:
    enable-self-preservation: false
  instance:
    instance-id: ${eureka.instance.hostname}:${server.port}
    prefer-ip-address: false
    hostname: eureka-server-1
  client:
    serviceUrl:
      defaultZone: http://eureka-server-2:8762/eureka/
spring:
  application:
    name: eureka-server
```

#### 编写第二个eureka配置文件

```yml
server:
  port: 8762
eureka:
  server:
    enable-self-preservation: false
  instance:
    instance-id: ${eureka.instance.hostname}:${server.port}
    prefer-ip-address: false
    hostname: eureka-server-2
  client:
    serviceUrl:
      defaultZone: http://eureka-server-1:8761/eureka/
spring:
  application:
    name: eureka-server
```

#### 启动方式

上面说过，将采用服务名称来进行服务通信，所以在配置服务向eureka注册时的 instance-id 就需要指定一下，因为在默认的方式下，eureka会为每一个服务生产不同的instance-id，在其他服务访问某个服务时，将使用这个默认的instance-id进行访问，这种方式在docker中将会无法通信（docker的网络中是找不到这个实例id的路由的）。更多的时候，内部服务的访问方式都是通过eureka的服务列表进行匹配，例如后面将集成的`spring boot admin` 会获取eureka中注册的所有服务的列表，并使用这些服务的instance-id访问这些服务。所以有必要指定eureka的服务实例名称（当然，也可以使用配置ip的方式，但是并不推荐，因为docker在容器重新启动的时候都会重新的生成容器的IP）。如上的：

```yml
instance:
	#指定主机名+ip的方式来生成该服务的实例id
    instance-id: ${eureka.instance.hostname}:${server.port}
    prefer-ip-address: false
    hostname: eureka-server-2
```

启动这两个eureka

```java
java -Dspring.profiles.active=1 eureka-server-1的启动类全路径
java -Dspring.profiles.active=2 eureka-server-2的启动类全路径
```

