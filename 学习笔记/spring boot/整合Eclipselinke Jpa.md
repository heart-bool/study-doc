# Spring Boot 整合Eclipselinke Jpa

Spring Boot 默认的Jpa是hibernate jpa，通过Spring Boot可以方便的使用。这里记录Eclipselinke Jpa和Spring Boot的集成方式

## 1、排除Spring Boot默认的 Jpa组件

这个就不多说了，maven 配置:

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
    <exclusions>
    	<exclusion>
        	<artifactId>hibernate-entitymanager</artifactId>
            <groupId>org.hibernate</groupId>
        </exclusion>
    </exclusions
</dependency>
```

## 2、添加依赖

```java
 <dependency>
     <groupId>org.eclipse.persistence</groupId>
     <artifactId>eclipselink</artifactId>
     <version>${eclipselink.version}</version>
     <exclusions>
         <exclusion>
             <artifactId>commonj.sdo</artifactId>
             <groupId>commonj.sdo</groupId>
         </exclusion>
     </exclusions>
 </dependency>
```

### 3、配置插件

```
<plugin>
	<groupId>de.empulse.eclipselink</groupId>
	<artifactId>staticweave-maven-plugin</artifactId>
	<version>1.0.0</version>
	<executions>
		<execution>
            <phase>process-classes</phase>
            <goals>
                <goal>weave</goal>
            </goals>
            <configuration>
                <logLevel>FINE</logLevel>
            </configuration>
		</execution>
	</executions>
	<dependencies>
		<dependency>
            <groupId>org.eclipse.persistence</groupId>
            <artifactId>org.eclipse.persistence.jpa</artifactId>
            <version>${eclipselink.version}</version>
		</dependency>
	</dependencies>
</plugin>
```

#### 4、创建配置类

```java
package com.prs.service.user.config;

import org.springframework.beans.factory.ObjectProvider;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.orm.jpa.JpaBaseConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.JpaProperties;
import org.springframework.boot.autoconfigure.transaction.TransactionManagerCustomizers;
import org.springframework.context.annotation.Configuration;
import org.springframework.orm.jpa.vendor.AbstractJpaVendorAdapter;
import org.springframework.orm.jpa.vendor.EclipseLinkJpaVendorAdapter;
import org.springframework.transaction.jta.JtaTransactionManager;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

@Configuration
public class EclipseLinkJpaConfiguration extends JpaBaseConfiguration {

	protected EclipseLinkJpaConfiguration(@Qualifier("dataSource") DataSource dataSource, JpaProperties properties, ObjectProvider<JtaTransactionManager> jtaTransactionManager, ObjectProvider<TransactionManagerCustomizers> transactionManagerCustomizers) {
		super(dataSource, properties, jtaTransactionManager, transactionManagerCustomizers);
	}

	@Override
	protected AbstractJpaVendorAdapter createJpaVendorAdapter() {
		return new EclipseLinkJpaVendorAdapter();
	}

	@Override
	protected Map<String, Object> getVendorProperties() {
		return new HashMap<>(0);
	}
}
```

