多线程并发库使用及源码解析

    1. 线程池
        1.1 线程池的创建方式:
            只列出常用的4中, 其他参考源码或文档.

            newCachedThreadPool()
                创建一个可根据需要创建新县城的线程池, 但是如果之前创建的线程可用的时候, 将不会创建新的线程. 如果没有, 则新建一个线程并添加到线程池中.
                该线程池中的线程默认的缓存时间为60m. 如果线程池中的线程未被使用的时间超过60m, 线程将被移除.

            newFixedThreadPool(int nThreads)
                创建一个固定数量线程的线程池, 以无界队列的方式来运行这些线程. 当有新的任务被提交, 如果线程池中有空闲线程时, 则直接执行. 如果没有空闲线程时, 添加的多余的任务将在无界队列中等待线程空闲.
                在某个线程没有被显式的关闭时, 线程池中的线程将一直存在.

            newSingleThreadExecutor(int corePoolSize)
                创建单个线程的线程池, 以无界队列运行该线程. 如果线程在执行期间出现失败而终止了这个单线程, 将会新创建一个线程来替换它.
                可以保证无界队列中所有的任务按顺序的执行.

            newScheduledThreadPool()
                创建并返回一个ScheduledExecutorService对象, 并且也可以指定线程池的大小

        1.2 ThreadPoolExecutor 类
            Executors类中提供的所有线程都使用这个类来创建
                构造方法: 用指定参数来创建新的线程池

                public ThreadPoolExecutor(int corePoolSize,
                                          int maximumPoolSize,
                                          long keepAliveTime,
                                          TimeUnit unit,
                                          BlockingQueue<Runnable> workQueue,
                                          ThreadFactory threadFactory,
                                          RejectedExecutionHandler handler)
                corePoolSize:               线程池中保存的线程数量. 包括空闲的线程.
                maximumPoolSize:            构造的线程池允许的最大线程数量.
                keepAliveTime:              线程池中线程存活的时间.
                unit:                       keepAliveTime 参数的时间类型.
                workQueue:                  用来保存任务的队列.
                threadFactory:              执行创建新线程时使用的工厂.
                handler:                    当任务超过线程池中活动的线程时定义的处理程序.

        1.3 CountDownLatch 类
            一个同步辅助类，在完成一组正在其他线程中执行的操作之前，它允许一个或多个线程一直等待。
            在创建CountDownLatch实例对象时, 设置一个等待次数, 然后, 当某一个线程调用该实例的await() 方法时, 在调用countDown()方法操作等待次数达到0之前, 所有的线程都将被阻塞.
            之后, 所有阻塞的线程将被释放.

        1.4 CyclicBarrier 类
            一个同步辅助类，它允许一组线程互相等待，直到到达某个公共屏障点 (common barrier point)。
            当指定等待线程数量中的最后一个线程到达之后（但在释放所有线程之前）, 释放所有线程.

            使用方式:
                1. 创建一个线程类, 该线程类接收一个 CyclicBarrier 参数 并在某一时刻调用CyclicBarrier 参数的await()方法.
                2. 创建 CyclicBarrier 并指定等待线程的数量.
                3. 创建对应等待线程的数量的多个线程实例.
                4. 启动这些线程.
            CountDownLatch 和 CyclicBarrier 的区别.
                前者是某一个线程等待其他所有线程向自己发送通知 针对一个线程. 后者是所有线程一起阻塞 针对多个线程.

        1.5 Callable 和 Future 的使用.

    2. Lock (锁)
        2.1 AQS 框架

            AQS 其实就是 java.util.concurrent.locks.AbstractQueuedSynchronizer 这个类. 这个类是整个java.util.concurrent的核心之一.
            比如 ReentrantLock Semaphore CountDownLatch 等类中都有一个内部类 Sync 继承该类.

            AQS 的核心是通过一个共享状态来同步状态. 变量的状态由其子类去负责维护, 而框架本身做的是:
                线程阻塞队列的维护.
                线程阻塞和唤醒.

