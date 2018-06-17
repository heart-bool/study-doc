
Memcached
    
        Free & open source, high-performance, distributed memory object caching system
        免费 & 开源, 高性能, 分布式 基于内存对象缓存系统.
    
        1. 安装
            
            Memcached 适用于大多数的Linux和BSD系统,  官方没有支持Win平台
            
            Linux_64 下安装过程
                1). 到Memcached官网获取源码包的地址. 然后下载.
                2). 解压下载后的文件. 然后cd 到解压的文件夹下
                    执行 ./configure prefix=/usr/local/memcached
                    
                    在执行配置的时候可能会报错
                        checking for libevent directory... configure: error: libevent is required.  
                        You can get it from http://www.monkey.org/~provos/libevent/
                        
                              If it's already installed, specify its path using --with-libevent=/dir/
                              
                    这里需要配置libevent库, 配置方式为
                        1). 到 http://libevent.org/ 下载 libevent 源码包
                        2). 解压源码包, cd 到解压的文件夹下
                            执行  ./configure prefix=/usr
                            
                    再执行 ./configure prefix=/usr/local/memcached
                    
                3). make & make install
                    
                4). 安装完成后, 检查Memcached是否安装成功
                    /usr/local/bin/memcached -h
                    
                    如果出现
                    ./memcached/bin/memcached: error while loading shared libraries: libevent-2.1.so.6: 
                        cannot open shared object file: No such file or directory
                    
                    1). 查找 libevent-xx.xx.so.x 的安装路径
                        whereis libevent-xx.xx.so.x
                    
                    2). 创建软链
                        ln -s /usr/local/lib/libevent-xx.xx.so.x /usr/lib/libevent-xx.xx.so.x 
                        
                    3). 执行 ldconfig 刷新 /etc/ld.so.conf
                
                推荐:
                    先编译安装 libevent, 然后在./configure Memcached 的时候, 指定参数 --with-libevent=/安装好的libevent路径
                       
                    
        2. 启动命令参数
            
            -p <num>        监听的TCP端口(默认是11211)
            -d              以守护进程方式运行Memcached
            -u <username>   运行Memcached的用户, 非root用户
            -m <num>        最大使用的内存. 单位是 MB 缺省是 64MB
            -c <num>        连接数量, 缺省是 1024
            -v              输出警告和错误信息
            -vv             打印客户端的请求和返回信息
            -h              打印帮助信息
            -i              打印memcached和libevent的版权信息
            -f              增长因子,  默认是1.25
            
                    
        3. 基本命令
            
            3-1). add 命令
                add key flag exp length\r\n
                data\r\n
                    
                    key:        存放数据的 key 也就是名字
                    flag:
                    exp         过期时间
                    length      value的长度 
            
            3-2). get 命令    
                get key\r\n
                    以key取值
                
            3-3). replace 命令    
                replace key flag exp lenght
                data
                    参数和add一致
                
            3-4). delete 命令
                delete key [time]
                    time: time参数是指使key失效, 并在time的时间内不允许使用此key. 多用于缓存同步.
            
            3-5). set 命令
                set key flag expiretime bytes\r\n
                data\r\n
                    和add用法一致
                
            3-6). add set replace 的区别:    
                    add:        对已经存在的key进行add, 例如在缓存中已经有一个key为abc, 再次add abc 是无效的
                    replace:    只能针对已经存在的key进行修改操作
                    set:        
                        如果服务器中有某个key, 则对该key进行修改操作.
                        如果服务器中没有某个key, 则新增一个key  
            
            flag参数解析:
                
                标志的意思, 可以用此参数来标志内容的类型, 以数字表示.
                可以自行定义, 比如, 1 是数组, 2是对象 等等
            
            exp参数解析:
                
                过期时间有三种格式:
                    1). 设置秒数, 从设定开始数, 到第 N秒(设定的秒数)失效
                        示例: set key 0 10 4 回车
                              test
                              
                              从设定开始数, 到第 10 秒失效
                    
                    2). 时间戳, 到指定的时间戳失效.              
                        示例: set key 0 1379209999 4 回车
                              test
                              
                              指定key的失效时间为时间戳 1379209999 对应的时间失效
                              
                    3). 设定为0. 不自动失效
                        示例: set key 0 0 4 回车
                              test
                              注意:
                                
                                这里的不自动失效不是永久有效的意思. 
                                1). 在编译Memcached的时候, 可以指定一个最长常量来设置key的最大失效时间, 默认是30天.
                                    所以即使设置为0, 30天之后也会自动失效.
                                2). 数据被踢 
                                
            3-7). incr 命令
                incr key step
                    示例:
                        incr age 2
                        使 key age 的值增加 2

            3-8). decr 命令
                decr key step
                    示例:
                        decr age 2
                        使 key age 的值减去 2
                    
                    注意: incr decr 是把值理解为32为无符号的进行 + - 操作的, 值在 [0 - 2^32-1] 的范围内.
                    
            3-9). stats 命令
                  
                 此处篇幅较长, 建议参阅 https://github.com/memcached/memcached/wiki/Commands#standard-protocol

            3-10). flush-all
                
                清空服务器.
                
            3-11). key value 的参数限制
                key: 
                    key 是缓存名称, 每个缓存名称都有一个独立的名字和存储空间. 是操作数据的唯一标识
                    Memcached 的key 最大支持250个以内的字节, 并且不能有空格. 
                    key 不能重复
             
                
        4. Memcached 内存分配机制
                        
            内存的碎片化:
                内存在程序进行内存分配的过程中, 某一块连续的空间被多次分配和释放之后可能会形成一些很小的内存片段, 无法再利用的情况.
            
            Slab Allocator分配机制
                
                基本原理是按照预先规定的大小, 将分配好的内存分割成特定长度的块, 以缓解解决内存的碎片化问题.
                将分配的内存分割成各种尺寸的块(chunk), 并把尺寸相投的块分成组(chunk的集合)
                
                Memcached 根据收到的数据的大小选择适合数据大小的slab, 
                Memcached 保存着slab内空闲chunk的列表, 根据该列表选择chunk, 然后将数据缓存到里面.
                
            在启动memcached的时候 指定 -vv或者-vvv 参数可以打印出chunk的大小.
            
            注意:
                例如现在有个大小为100字节的内容要存, 但 122 的chunk满了?
                    Memcached 并不会去寻找更大的chunk来存, 而是在 122 的chunk中踢出旧的数据. 详见 5-2
                    
                    
        5. 数据过期和删除机制
            5-1). Lazy Expiration 惰性过期. 
                Memcached 内部不会监视key是否过期, 而是在get时查看记录的时间戳, 检查key是否过期. 这种奇数被称为 惰性过期.
                如果一个key在存储之后一直没有被get过, 不会自动删除, 如果有新的key过来存储, 该位置会直接被当成空的chunk来占用.
                
                这种过期只是让用户看不到这个数据而已, 并没有在过期的瞬间立即从内存中删除.
                
                好处: 节省了CPU时间和检测的成本.
            
            5-2). LRU 删除机制
                Least Recently Used 最近最少使用.
                    当某个单元被请求时, 维护一个计数器, 用过计数器来判断最近谁最少被使用.
                    
                    当memcached的内存空间不足时(无法从slab class 获取到新的空间时), 就从最近未被使用的记录中搜索, 并将其空
                    间分配给新的记录. 从缓存的实用角度来看, 该模型十分理想.

                            
                            
            
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                    