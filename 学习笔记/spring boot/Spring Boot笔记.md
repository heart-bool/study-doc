# Spring Boot 笔记

## Spring Boot 简介

Spring boot 是一个基于Spring创建的项目。用官方的话说，可以轻松的创建和运行一个独立的、生产级别的、基于Spring的应用程序。

### 特征

- 创建独立的Spring应用程序
- 嵌入式的tomcat、jetty、uodertow。无需部署war文件
- 提供   'starter' 依赖简化应用程序的配置
- 尽可能的自动化配置Spring和第三方类库
- 绝对没有xml配置和生成代码

## 安装Spring Boot

一般来说采用 maven 或者 gradle的方式可以轻松的创建一个Spring boot应用。

### Maven

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>

	<groupId>com.example</groupId>
	<artifactId>myproject</artifactId>
	<version>0.0.1-SNAPSHOT</version>

	<!-- 从默认的Spring boot中继承 -->
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.1.3.RELEASE</version>
	</parent>

	<!-- 添加一个web应用的依赖 -->
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
	</dependencies>

	<!-- 打包成一个可执行的jar -->
	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>
</project>
```

## 使用@SpringBootApplication 注解

该注解在启动一个Spring Boot应用的时候会使应用具备如下功能:

- `@EnableAutoConfiguration`: 启用spring boot 自动配置功能
- `@ComponentScan`: 在应用程序所在的包上启用扫描(一般就是以`@SpringBootApplication`标注的类所在的包)
- `@Configuration`：允许在上下文中注册额外的bean或导入其他配置类

