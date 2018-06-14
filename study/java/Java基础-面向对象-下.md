面向对象

1. 继承
   
    
    基本概念:
        从已有类创建新的类的过程.
        
        被继承的类被成为父类, 继承父类的类称为子类.
        通过继承可以实现代码重用. 子类可以直接使用父类的所有非私有的方法和属性.
        
        关键字 extends
            示例:
                class A {
                    private String name;
                }
            
                class B extends A {
                }
                
                在这个例子中, B 类可以直接使用父类 A 中的所有属性. 
        
        子类的实例化过程:
        
            在创建子类对象实例的时候, 父类的构造方法也会被调用, 而且父类的构造方法是在子类的构造方法前面执行.
            如果在父类中没有默认构造方法, 则在子类的构造方法中必须显示的使用 super() 调用父类的有参构造方法,
            并且 super() 必须出现在子类构造方法的第一行.
            
                示例:
                    class A {
                        private String name;
                        
                        public A(String name) {
                        
                        }
                        
                        public void ead() {
                            System.out.println("父类的方法");
                        }
                    }
                
                    class B extends A {
                        public B(String name) {
                            super(name);
                        }
                        
                        @Override // 也可以不加
                        public void ead() {
                            System.out.println("子类重写父类的方法");
                        }
                    }
        
        继承的限制
            Java 中 class 只能实现单继承. 一个子类只能有一个父类.
        
        方法重写:
            注解: @Override 
            在子类中, 可以重写父类的非私有的方法.
                示例:
                    class A {
                        private String name;
                        
                        public void ead() {
                            System.out.println("父类的方法");
                        }
                    }
                
                    class B extends A {
                        
                        @Override // 也可以不加
                        public void ead() {
                            System.out.println("子类重写父类的方法");
                        }
                        
                    }
2. final 关键字
    
    
    在Java中, final 可以用来修饰类, 属性和方法
    
    修饰类:
        表示该类不能被继承. 而且 final 类中的所有私有方法都会被隐式的转换成final方法
        
            publi final class A {}  
        
            class B extends A {} // 会出现编译时异常. 
    修饰方法:
        将方法锁定, 防止任何子类修改该方法的含义.
    
    修饰变量:
        
        对于修饰引用类型的变量:
            引用不能再指向其他对象. 而对象的内容是可变的.
        
        对于基本类型的变量:
            该变量为常量, 其值不可以被改变.    
    注意：
        final 不能修饰抽象类. 因为抽象类本身就是为了继承而存在. 使用 final 修饰抽象类没有任何意义.
                
3. 多态


    抽象类:
    
        抽象类和抽象方法必须使用 abstract 关键字修饰. 当一个类中包含抽象方法时, 该类一定是抽象类, 相反, 抽象类中可以没有抽象方法.
        
        abstract 关键字:
            不能修饰成员变量和局部变量以及构造方法.
            不能修饰类方法, 即不能和static放在一起。
            abstract修饰的方法必须由子类重写才有意义, 因此abstract不能和private同时修饰.
        
        抽象类:
            使用 abstract 关键字修饰的类, 和普通类在使用上除了不能被实例化, 其他没有任何区别. 它的定义主要是用来给子类继承.
            
        抽象方法:
            使用 abstract 关键字修饰的方法. 当一个类中包含抽象方法时, 该类一定是抽象类.
        
        抽象类的声明:
            abstract class A {
                // 可以有抽象方法
                abstract void method();
                
                // 可以有实例方法
                public void print() {
                
                }
                
                // 可以有静态方法
                public static void println() {
                            
                }
                
                // 可以有成员变量
                private String name;
            }
        
    接口:
    
        interface:
            一个抽象类型, 抽象方法的集合, 接口中只声明方法, 并不包含方法的实现.
            接口中的所有方法会被隐式的转换为 public abstract 的.
            接口中的所有变量都是 public static final 的常量
            
        和抽象类的区别:
            抽象类中可以有实例方法, 接口中不行.
                在jdk 1.8之后, 接口可以有一个default 方法, 和静态方法. 主要的目的是为了支持函数式编程.
            
            抽象类中的所有成员变量和普通类一样, 但接口中是常量
            抽象类中可以有静态方法, 而接口中不能.
            一个类只能继承一个抽象类, 但可以同时实现多个接口.
            
        接口的声明:
            interface A {
                // 只能有常量
                String NAME = "张三";
                
                // 只能有抽象方法, 注意是隐式的
                public void print() {
                }
                
            }    
        接口的多继承方式：
        
            interface A extends interface1, interface2 ...{
            }
        
           
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    