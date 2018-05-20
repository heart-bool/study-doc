多线程

    线程依赖进程而存在.
    进程: 一个进程就是一个运行中的应用. 系统进行资源分配和调度的独立单位. 每一个进程都有它自己的内存空间和系统资源.
    线程: 进程的执行单元. 同一进程中的多条执行路径.
    意义: 为了提高应用程序的执行效率. 提高CPU的使用率.

    并发和并行:
        前者是逻辑上同时发生. 在某一个时间内同时运行多个程序.
        后者是物理上同时发生. 在某一时间点上同时运行多个程序.

    并发和并行:
        前者是逻辑上同时发生. 在某一个时间内同时运行多个程序.
        后者是物理上同时发生. 在某一时间点上同时运行多个程序.

    线程的状态:
        创建 就绪 运行 阻塞 结束

    实现线程的方式:
        1. 继承 Thread 类, 并重写 run() 方法

            public MyThread extends Thread {
                private String name;
                public MyThread(String name) {
                    this.name = name;
                }
                public void run() {
                    System.out.println("当前线程的名字:" + name);
                }
            }

            MyThread thread = new MyThread("线程1")

        2. 实现Runable 接口

            new Thread(new Runnable() {
                @Override
                public void run() {
                    System.out.println("当前线程的名字:" + Thread.currentThread().getName());
                }
            }).start();

        注意:
            创建一个线程之后 必须显示的调用 start() 方法 运行线程, 当start()方法被调用时, 也并非表示立即执行该线程, 而是使线程进入可运行状态.
            至于什么时候执行线程, 由操作系统来决定. 多线程并行执行时, 各个线程执行的顺序是无法保证的.

        区别:
            两种方式并没有太大的区别, 从多态来说 实现Ruannabl 接口可以额外的继承一个类, 而继承Thread 不行.

        线程控制:
            线程休眠: Thread.sleep(long m);
            线程加入: join();
            线程礼让: Thread.yield();
            守护线程: setDeamon(boolean on);
            线程中断:
                        stop(boolean on); // 直接终止线程
                        interrput(); //中断线程, 并在执行线程中抛出异常.

        线程的状态转换
            1、新建状态(New):新创建了一个线程对象.
            2、就绪状态(Runnable):线程对象创建后,其他线程调用了该对象的start()方法.该状态的线程位于可运行线程池中,变得可运行,等待获取CPU的使用权.
            3、运行状态(Running):就绪状态的线程获取了CPU,执行程序代码.
            4、阻塞状态(Blocked):阻塞状态是线程因为某种原因放弃CPU使用权,暂时停止运行.直到线程进入就绪状态,才有机会转到运行状态.阻塞的情况分三种:
            (一)、等待阻塞:运行的线程执行wait()方法,JVM会把该线程放入等待池中.(wait会释放持有的锁)
            (二)、同步阻塞:运行的线程在获取对象的同步锁时,若该同步锁被别的线程占用,则JVM会把该线程放入锁池中.
            (三)、其他阻塞:运行的线程执行sleep()或join()方法,或者发出了I/O请求时,JVM会把该线程置为阻塞状态.
                            当sleep()状态超时、join()等待线程终止或者超时、或者I/O处理完毕时,线程重新转入就绪状态.(注意,sleep是不会释放持有的锁)
            5、死亡状态(Dead):线程执行完了或者因异常退出了run()方法,该线程结束生命周期.
    线程的优先级:
        Java 线程优先级. 线程优先级越高的线程将获得更多的执行机会.
        static int MAX_PRIORITY
                  线程可以具有的最高优先级,取值为10.
        static int MIN_PRIORITY
                  线程可以具有的最低优先级,取值为1.
        static int NORM_PRIORITY
                  分配给线程的默认优先级,取值为5.
        每个线程都有默认的优先级. 主线程的默认优先级为Thread.NORM_PRIORITY.

    线程安全性:
        当多个线程同时操作相同的一份数据, 会出现线程安全性的问题.
        定义:
            当多个线程访问某个类时, 这个类始终保持正确的行为, 那么这个类就是线程安全的.

    线程的特性:
        1 原子性
            当进行多个操作时, 要么都执行,  要么都不执行. 例如:
                有一个变量 count, 在多线程情况下都其进行 count++ 操作时, 实际上这个操作包含了三个独立的步骤: 读取count的值 -> 将其值加1 -> 将计算结果赋值给count
                这是一个操作序列, 并且其结果状态依赖于之前的状态. 所以在多线程情况下, 需要保证 count 的原子性, 也就是这三个独立的操作要么同时执行, 要么都不执行.
            一般我们使用加锁的方式来保证这个操作的原子性.

        2 可见性
            当一个变量在多线程共享时, 任何一个线程对该变量的修改都是对其他线程可见的.
        3 重排序


    volatile 变量
        Volatile 变量具有 synchronized 的可见性特性，但是不具备原子特性. 这就是说线程能够自动发现 volatile 变量的最新值。
        Volatile 变量可用于提供线程安全，但是只能应用于非常有限的一组用例：多个变量之间或者某个变量的当前值与修改后值之间没有约束。
        因此，单独使用 volatile 还不足以实现计数器、互斥锁或任何具有与多个变量相关的不变式（Invariants）的类
        在某些情况下，如果读操作远远大于写操作，volatile 变量还可以提供优于锁的性能优势。

        只能在有限的一些情形下使用 volatile 变量替代锁。要使 volatile 变量提供理想的线程安全，必须同时满足下面两个条件：
            对变量的写操作不依赖于当前值。
            该变量没有包含在具有其他变量的不变式中。
        这些条件表明，可以被写入 volatile 变量的这些有效值独立于任何程序的状态，包括变量的当前状态。

线程池




单例模式


    /***
     * 传统单例模式: 懒汉式
     * 缺点:
     *      在多线程环境下不能正常工作
     */
    class SingeTest_01 {
        private SingeTest_01() {
        }

        private static SingeTest_01 SINGE_TEST = null;

        public static SingeTest_01 getInstance() {
            if (SINGE_TEST == null) {
                SINGE_TEST = new SingeTest_01();
            }
            return SINGE_TEST;
        }
    }

    /***
     * 线程安全的单例模式:
     *      对方法加锁
     *      缺点: 效率有影响
     */
    class SingeTest_02 {
        private SingeTest_02() {
        }

        private static SingeTest_02 SINGE_TEST = null;

        public synchronized static SingeTest_02 getInstance() {
            if (SINGE_TEST == null) {
                SINGE_TEST = new SingeTest_02();
            }
            return SINGE_TEST;
        }
    }

    /***
     * 线程安全的单例模式:
     *      双重锁验证
     */
    class SingeTest_03 {
        private SingeTest_03() {
        }

        private static SingeTest_03 SINGE_TEST = null;

        public static SingeTest_03 getInstance() {
            if (SINGE_TEST == null) {
                synchronized (SingeTest_03.class) {
                    if (SINGE_TEST == null) {
                        SINGE_TEST = new SingeTest_03();
                    }
                }
            }
            return SINGE_TEST;
        }
    }


    /***
     * 静态内部类的方式
     *
     */
    class SingeTest_04 {

        private SingeTest_04() {
        }

        private static class InnerSingeTest {
            private static SingeTest_04 SINGE_TEST = new SingeTest_04();
        }

        public static SingeTest_04 getInstance() {
            return InnerSingeTest.SINGE_TEST;
        }

    }

    //饿汉式单例类.在类初始化时，已经自行实例化
    class SingeTest_05 {
        private SingeTest_05() {
        }

        private static final SingeTest_05 SINGE_TEST = new SingeTest_05();

        public static SingeTest_05 getInstance() {
            return SINGE_TEST;
        }
    }


















