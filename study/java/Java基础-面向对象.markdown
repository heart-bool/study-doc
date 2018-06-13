面向对象

1. 基本概念
    
    
    面向对象和面向对象的比较:
    
        面向过程:
            分析出解决问题的步骤, 然后用函数将这些步骤一步一步实现, 使用的时候依次执行. 
         
        面向对象:
            是一种编程思想或者思维方式
            
            面向对象的思维方式:
                
                1. 先整体, 再局部
                2. 先抽象, 再具体
                3. 能做什么, 再怎么做
            
            面向对象的设计原则
        
2. 类与对象
    
     
    类:
       
        成员变量:
            
            也就是上边所说的属性. 例如上边 Person 类的name age 都是 Person 类的成员变量
            成员变量在内存中的位置是堆内存
            生命周期随对象的创建而存在, 随对象的销毁而销毁
            每个成员变量在不被初始化的情况下都会有默认的初始化值
                引用类型为 null
                数值类型为 0
                bool类型为 false    
        
        定义:
        
            类是一个抽象的概念. 可以理解为某一个具体的事物的分类.
            类是一组具有相同特性(属性)与行为(方法)的事物集合.
        
        类由属性和方法组成:
            
            属性: 类的单个特性
            方法: 类的具体的行为
        
        举例:
            
            人类有姓名 年龄 等属性 有吃饭 睡觉 等行为
            
    对象:
        
        某一个类的实例. 比如 `张三`属于人类的一个实例
        
        
    类与对象的关系:
        
        多个对象可以属于某一个类, 某一个类可以拥有多个对象
        
        
3. 类和对象的定义格式


    Java 中的类的定义:
                
        class className {
            
            // 属性
            filedName;
            
            // 方法
            returnType methodName() {}
        }
        
        按照上面的人类来举例
        
        class Person {
            
            // 属性
            // 名字
            String name = "张三";
            // 年龄
            int age = 18;
        
            // 方法
            // 吃饭
            void eat() {
            
            }
        }        
     
    对象的创建:
        
        new 关键字: 创建一个对象 
        
        // 创建一个人
        Person zhangsan = new Person();
        
        // 访问这个对象的属性
        zhangsan.name
        zhangsan.age
        
        // 调用实例对象的方法
        zhangsan.eat()   
    
4. 对象内存分析

        
    在java中创建一个引用类型的对象实例的时候, 首先会在栈内存中创建一个引用, 然后在堆内存中分配一块空间用来存放实例对象的信息, 然后再将栈内存中的地址赋值给引用变量.
    
5. 封装


    class Person {
        
        // 属性
        // 名字
        private String name = "张三";
        // 年龄
        private int age = 18;
    
        // 方法
        // 吃饭
        void eat() {
        
        }
        
        public String getName() {
            return this.name;
        }
        
        public String getAge() {
            return this.age;
        }
        
        public void setName(String name) {
            this.name = name;
        }
        
        public void setAge(int age) {
            this.age = age;
        }
    }      

    面向对象特性之一. 封装就是隐藏具体的实现, 只提供对外访问的接口.
    例如上边的人类, 封装了 getName getAge setAge setName 等方法来提供对外访问的接口
    通俗的来说, 就是将对象的成员变量用 private 修饰符等 来限制成员变量的赋值方式.
    
    
6. 构造方法
    
    
    Java 中的构造方法分为无参构造和有参构造. 
        无参构造: 没有参数的构造方法
            
            Person () {
            }
            
        有参构造: 有参数的构造方法
        
            Person (String name, int age) {
                this.name = name;
                this.age = age;
            }
            
            Person (String name, int age) {
                this.name = name;
                this.age = age;
            }
        
            Person (String name) {
                this.name = name;
            }
            
        注意点:
            
            java 中的有参构造可以有一个或者多个, 一个类中如果没有手动实现有参构造方法, jvm会自动生成一个无参构造方法. 如果有, 将不会自动生成.        

7. this


    this 表示当前对象.
        当前对象:
            实例调用类的方法时, 就是当前方法的那个实例.
    
    
8. 值传递与引用传递

    
    值传递:
        public class ValueDemo {
            public void main(String args[]) {
                int x = 0; // 1
                method(x); // 2
                System.out.println(x) // 0
            }        
            
            public void method(int mx) {
                mx = 20; // 3
            }
        }
        
        解析:
            在java内存模型中, 每一个方法都会有自己的临时数据区.
            在上面的例子中, 主线程执行[1]的时候, 创建并赋值给变量x, 压栈, 在执行[2]的时候, 将 x 的值赋值给了方法的mx参数, 在栈中创建了一个新的变量mx并压栈, 这时的mx是相等于x的,  
            所以, 这时候其实创建了两个变量, 即mx跟x并不是同一个变量, 当执行[3]的时候,只是对mx进行的操作, x 依然是0.
            也就是说, 在进行值传递的过程中对参数直接赋值, 是不会对原来的变量有影响的. 因为操作的不是同一个变量, 也可以说操作的不是同一块内存区域.
            
    引用传递:
        public class ValueDemo {
            public void main(String args[]) {
                List<String> list = new ArrayList<>(); // 1
                list.add("1");
                method(list); // 2
                System.out.println(list); // [1, 2]
            }        
            
            public void method(List<String> list) {
                list.add("2"); // 3
            }
        }
        
        解析:
            相比引用传递唯一不同的地方是在[2]. 当程序执行2的时候, 只是将list对象的引用传递了方法的参数, 所以在方法内操作的其实是在main方法中创建的list对象.
            
    注意: String 类型值传递的混淆点. 
    
        public class ValueDemo {
            public void main(String args[]) {
                String str = 0; // 1
                method(str); // 2
                System.out.println(str) 
            }        
            
            public void method(String str) {
                str = 20; // 3
            }
        }
    
        String 类型值进行值传递的时候, 如果在被调用的方法体内直接对参数进行赋值或者字符串连接等其他操作的时候, 也是不会对原字符串有影响的.
        因为String 本身就是一个对象, 对String对象进行操作的时候, 在[3]步的时候其实str的引用已经被改变了, 并在线程栈中独立存在.

9. 对象的一对一关系


    Java 中对象一对一关系的表示方式, 
        
        单向一对一
            例如: 一个人只有一张身份证(不绝对, 仅仅举例)
            
            
            class Person {
                IdCard idCard;
            }
            
            class IdCard {
            }
        
        双向一对一
            例如: 一个人只有一张身份证, 一张身份证可以表某个人(不绝对, 仅仅举例)
            class Person {
                IdCard idCard;
            }
            
            class IdCard {
                Person person;
            }
        
    
10. static关键字


    修饰属性: 全局变量. 随类的加载而存在, 不创建类的对象实例也可以直接使用.
    修饰方法: 随类的加载而存在, 不创建类的对象实例也可以直接调用.
    修饰类: 
    
11. main方法


    s
    
12. 单例设计模式


    s
    
13. 对象数组


    s