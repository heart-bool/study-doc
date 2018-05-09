多线程

    线程:
        统一进程下的多个执行路径.

    目的:
        为了速度

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
            
            




















