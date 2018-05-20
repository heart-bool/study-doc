多线程并发库使用及源码解析

    1. Lock (锁)
        1.1 AQS 框架

            AQS 其实就是 java.util.concurrent.locks.AbstractQueuedSynchronizer 这个类. 这个类是整个java.util.concurrent的核心之一.
            比如 ReentrantLock Semaphore CountDownLatch 等类中都有一个内部类 Sync 继承该类.

            AQS 的核心是通过一个共享状态来同步状态. 变量的状态由其子类去负责维护, 而框架本身做的是:
                线程阻塞队列的维护.
                线程阻塞和唤醒.
