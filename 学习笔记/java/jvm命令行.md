



# JVM命令行

## jvm 参数类型

### 标准参数

- -help
- -version showversion
- -server -client
- -cp -classpath

### 非标准参数

#### X参数

- -Xint:解释执行
- -Xcomp:第一次使用就编译成本地代码
- -Xmixed:混合模式，由jvm自己来绝对是否编译成本地代码

#### XX参数

- boolean类型


​	格式：-XX:[+-]<name>表示启用或者 禁用name属性

- k-v类型


​	格式：-XX:<name>=<value>

#### -Xmx -Xms

​	-Xmx == -XX:initialHeapSize 初始化堆内存大小

​	-Xmx == -XX:MaxHeapSize	最大堆内存大小

## 查看JVM运行时参数

### PrintFlagsInitial

### PrintFlagsFinal

### jps 

​	查看java进程命令

### jinfo

### jstat

​	jstat 可以查看jvm的统计信息:

​	类加载

​	垃圾收集

​	JIT

#### jmap

### 如何定位jvm内存溢出

#### 1. 导出内存映像文件

- 内存溢出自动导出	

  在应用启动时可以通过设置JVM参数来启用内存溢出自动导出:

- ```
  -XX:+HeapDumpOnOutOfMemoryError ---当发生内存溢出时自动导出内存映像文件
  -XX:heapDumpPath=./				---导出的路径
  ```

- jmap手动导出

  ```
  jmap -dump:<dump-options>
  	live dump only live objects; if not specified, all objects in the heap are dumped.
      format=b     binary format
      file=<file>  dump heap to <file>
  ```

#### 使用MAT工具分析内存映像文件

​	检查内存中占用最多的对象

#### jstack定位CPU飙高和死锁的问题

通过导出jvm运行时的线程信息定位相应的问题



### JVisualVM的可视化监控工具





































