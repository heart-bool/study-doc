# spring笔记

## spring是啥

spring是一个轻量级的企业开发框架，提供一站式的开发解决方案。Spring 可以轻松的创建Java企业级应用，提供了企业环境中Java语言所需的一切。

## spring核心

- IOC (Inversion of control) 控制反转
- AOP 面向切面编程

### IOC (Inversion of control) 控制反转

用户将对象的创建、生命周期管理、依赖关系等转交由Spring来负责控制。

IOC的另一个概念是DI(依赖注入)，表示应用在运行时，动态的向某个对象提供它所依赖的其他对象。

对应代表IOC的类为 `org.springframework.context.ApplicationContext`

### AOP面向切面编程

- 横切关注点

  对哪些方法进行拦截，拦截后怎么处理

- 切面

  对横向关注点的抽象

- 连接点

  在spring中实际就是指拦截的方法

- 切入点

  对连接点的定义

- 通知

  指拦截到连接点之后要执行的代码。通知包括 前置 后置 异常 最终 环绕五种。

- 目标对象

  代理的对象 

- 织入

- 引入

AOP基于IOC对bean的管理，可以直接使用ioc容器中的bean，这种关系可以由依赖注入来实现。spring创建代理的规则:

1. 使用JDK动态代理来创建AOP代理。
2. 当需要被代理的类不是接口，将采用CGLIB代理
3. 使用 aspectj

## Bean概述

Spring IOC容器管理一个或多个Bean。bean是由用户提供给容器的配置元数据来创建的，比如`xml`文件

### 定义bean

1. 基于xml的方式

   ```xml
   <bean id="exampleBean" class="examples.ExampleBean"/>
   ```

2. 基于Java Config的方式

   ```java
   @Configuration
   public class Test {
   	private static Test test = new Test();
   	
       private Test() {}
       
       @Bean
       public getBean() {
           return test;
       }
   }
   ```
