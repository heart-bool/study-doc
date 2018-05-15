集合

    Java 集合分为两类
        1. 线性结构的 Collection 集合
            Collection 接口是所有线性集合的根接口.

            实现类
                1. List
                    特点:
                        1). 都是按照元素的插入顺序来保存元素的顺序. 故有序.
                        2). 可以添加重复元素.
                        3). 元素可以为空.
                    ArrayList:
                        维护一个动态扩容的数组. 所以具有数组的一些特点. 在移动 删除 扩容的时候效率较低. 随机访问的效率高.
                        1). 非线程安全的.
                        原理:
                            当创建一个新的ArrayList的时候, 并不会立即为这个数组开辟空间, 而是在添加第一个元素的时候将这个空的ArrayList的长度扩充到默认的长度: 10
                            当向数组添加元素时, 添加之后的数组长度大于当前数组的大小, ArrayList 将会扩容, 扩容的长度是 当前数组的长度 >> 1 也就是当前数组的长度的一半.
                    LinkedList:
                        1). 维护一个双向链表, 增删效率高, 随机访问效率低.
                        2).LinkedList 在添加元素时, 默认是将元素添加到链表的最后一个.
                    Vector:
                        1). 线程同步的集合. 与ArrayList相比, Vector在创建时就会创建一个容量为10的数组.
                2. Set
                    特点:
                        1). 并不保存元素的插入顺序, 无序的列表.
                        2). 有且只能有一个 null
                        3). 不可以有重复的元素. 前提是集合内元素必须实现 hashCode() 和 equals() 方法.
                    HashSet:
                        维护一个HashMap, 准确的说, HashSet 只利用了 HashMap的key, 其所有的element作为HashMap的key 存储在HashMap中, 而这个HashMap的所有 value
                        是在类中定义的一个私有的不可变的Object对象. 这么做的目的其实只是利用了 HashMap Key 不能重复的原理.
        2. Map
            将键映射到值,  Key 可以为空, 但不允许重复.
            实现类
                HashMap
                    特点:
                        HashMap 按照映射的插入顺序保存元素. 故有序的集合.
                        HashMap 在多线程环境下是不安全的.
                        Hash 冲突:
                            HashMap 底层维护一个 Entry 数组, 每一个 Entry 数组使用链表来解决 Hash 冲突. 当在向HashMap中添加元素时, HashMap首先会检查key的hash值是否相同,
                            当hash值相等再检查equals是否相等, 两者都相等时, 就会产生Hash冲突. 这时HashMap会将冲突的key放到对应的Entry数组的元素位置上, 将同一hash值的链表都存储在一个链表里.
                            jdk1.8 之前. 如果hash值相等的元素较多时, 通过key获取值的效率就会有所降低. 在jdk1.8之后, HashMap采用Entry+链表+红黑树实现,
                            当链表长度超过阈值（8）时, 将链表转换为红黑树，这样就减少了查找时间
                        通过上面的处理, 我们会发现, 如果两个key 的hash值和equals都相等 则外部的两个key获取的都是最后添加到 HashMap 中的值.
                        例如:
                            String key1 = "hello";
                            String key2 = "hello";
                            map.put(key1, "world1");
                            map.put(key2, "world2");
                            在通过key获取值的时候, key1 和 key2 都会得到 "world2".

                Hashtable
                    特点:
                        在hash冲突的处理上1.8和1.7及之前大致一样, 区别在于Hashtable是线程安全的.

                LinkedHashMap:
                    特点:
                        在hash冲突的处理上1.8和1.7及之前大致一样, 区别在于它是有序的Map容器.
