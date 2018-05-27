Redis

    redis 简介
        Redis是一个开源的(BSD许可的) 基于内存的key-value的存储系统. 它可以用作缓存, 消息中间件和数据库.
        key-value 存储形式的特点:
            可扩展性:
                可以支持极大的数据的存储. 只要有更多的机器就能够保证存储跟多的数据.
                支持数量很多的并发的查询.
            分布式: 多节点同时存储数据和状态, 节点之间通过消息来保持数据一致.
            数据一致: 所有节点的数据都是同步更新的, 不用担心得到不一致的结果.
            冗余: 所有节点保存相同的数据, 整个系统的存储能力取决于单台机器的能力.
            容错: 如果集群中少数节点出错, 不影响整个系统的运行.
            可靠性: 容错 冗余保证了系统的可靠性.

        redis 的数据类型

            String          二进制安全的字符串
            Lists           按插入元素的顺序排序的集合. 基本上就是链表
            Sets            不重复且无序的集合.
            Sorted Sets     有序的Set集合
            Hashes          hash表结构

            redis 中所有的操作都是原子性的.

        持久化
            AOF 快照:
                将内存中的数据使用快照的方式不断的写入磁盘.




        bin目录下的脚本:
            redis-benchmark         Redis 性能测试工具
            redis-check-aof         检查 AOF 日志
            redis-check-rdb         检查 RBD 日志
            redis-cli               客户端
            redis-sentinel
            redis-server            服务端

    redis 命令
        通用命令:
            keys * ? []         获取所有的key. * 为通配符.  ? 通配单个字符. [] 通配中括号中某一个字符.
            type key            获取key的类型.
            exists key          是否存在某个key
            del key             删除某个key
            rename key newKey   重命名某个key    注意: 如果 newKey 存在 则值会被覆盖
            renamenx key newKey 重命名某个key 当 newKey 存在 则不修改
            select dbindex      选择一个存储库 redis 默认有16个存储库 下标从0 - 15
            move key dbindex    将某个key移动到另一个存储库

            ttl key             查询某一个key的有效期 redis中默认的有效期都是永久有效 单位为秒
            expire key          设置key的过期时间 单位为秒

            pttl key            查询某一个key的有效期 单位为毫秒
            pexpire key         设置key的过期时间 单位为毫秒
            persist key         将key设置为永久有效

        string
            set key value 1 [ex 秒数] 2[px 毫秒数] 3[nx key不存在时执行操作 / xx key存在时执行操作]
            示例:
                set name zhangsan ex 10             设置一个key name 有效期为10秒
                set name zhangsan px 10             设置一个key name 有效期为10毫秒
                set name zhangsan ex 10 nx          设置一个key name 当name 不存在时才设置 有效期为10秒
                set name zhangsan px 10 xx          设置一个key name 当name 存在时才设置 有效期为10毫秒

            mset key1 value1 key2 value2 ... 一次设置多个key
            mget key1 key2 ... 一次获取多个key

            setrange key offset value  替换某个 key 从 offset 位置开始之后的 value 注意 offset 如果大于value的长度会自动加上十六进制值
            getrange key start end  获取某个key 从start 开始到end
            getset key newvalue     获取旧值设置新值
            incr key                自增1
            decr key                自减1
            incrby key value        自增value值
            decrby key value        自减value值
            incrbyfloat key value        自减value值
            decrbyfloat key value        自减value值

        list
            lpush key [value ...] 将值插入到list的头部
            rpush key [value ...] 将值插入到list的尾部
            lrange key start end  获取list
            lpop key 删除并返回头部元素
            rpop key 删除并返回尾部元素
            lrem key count value 删除指定元素  count 表示删除元素的个数 正数从头部删除 负数从尾部
            ltrim key start stop 截取list
            llen key 获取list长度
            lindex key index 获取index位置的元素
            linsert key before|after povit value 在某个值前面或后面插入元素 如果有多个povit值相同 则只在第一个povit之前或之后插入
            rpoplpush key1 key2 将key1的尾部元素放到key2的头部
            brpop key timeout
            blpop key
        set
            sadd key [value...] 设置一个set
            smembers key 获取 set 的元素
            srem key value 删除 set 中的元素
            spop key 返回并删除 set 中的随机元素
            srandmember key 返回 set 中的随机元素
            sismember key member 判断 set 中是否存在 member
            scard key 返回set的长度
            smove source target member 将 source 中的元素移动到 target 中
            sinter [key...] 求交集
            sunion [key...] 求并集
            sdiff [key...] 求差集
            sinterstore target [key...] 将求出的结果存储到 target

        sorted set
            zadd key value  添加
            zrange key start end 获取
            zrangebyscore key min max [withscore] [limit offset count] 根据score获取
            zrank key member
            zrevrank key member
            zremrangebyscore key min max
            zremrangebyrank key min max
            zrem key value
            zcard key 长度
            zinterstore members key [key ...] [weights weight [weight ...] [sum|min|max]

        hash
            hset key field value    设置一个hash
            hmset key field value [field value ...] 设置多个hash
            hgetall key 获取key的所有field
            hstrlen key field 获取某个hash下的某个field
            hvals key 获取hash的所有值
            hkeys key 获取hash的所有field
            hdel key field [field ...] 删除某个hash的某个field
            hexists key filed 某个hash中是否有某个filed
            hincrby key feild incr 将hash中的某个field加指定的值
            hscan key cursor [match pattern] [count count] 迭代某个hash


    redis 事务
        原理:
            redis在执行简单事务操作的时候, 会在开启一个事务时, 将后续的命令添加到一个任务执行队列, 当调用 exec 命令时按顺序执行队列中的所有任务

        事务操作:
            set lisi 200
            set wangwu 800
            multi                           开启一个事务
            incrby lisi 200
            decrby wangwu 200
            exec                            执行队列中的命令

            当事务执行过程中出错的时候(exec 之前), 如果命令入队返回QUEUED 那么入队成功, 否则失败.
            在2.6.5 之前redis只执行那些入队成功的命令, 忽略入队失败的命令.
            在2.6.5之后 服务器会在命令入队失败的情况进行记录, 并在执行exec命令时, 拒绝执行并自动放弃这个事务.

            discard 取消事务.

        锁
            悲观锁
                直接对key进行加锁, 只有当前客户端能操作

            乐观锁
                检查key有没有被更改

            watch key 在执行事务时, 监视某个key是否被改变
            unwatch 取消监视

    持久化
        redis 的两种持久化方式:
            RDB:
                能够在指定的时间间隔内对数据进行快照存储
                每隔N分钟或N次写操作后 从内存dump文件保存到rdb文件
                优点:
                    与AOF相比, RDB方式在恢复大数据时, 会更快一点
                    由子进程去执行RBD操作
                    单一文件
                    可以最大化redis的性能
                    导出时是内存映像, 恢复速度很快
                缺点:
                    如果redis出现故障, 可能会丢失更多的数据
                    在数据集非常大的时候, 可能会影响redis的性能

                工作原理:
                    在需要保存RDB文件时, 父进程会创建一个子进程(fork/join) 去执行所有的IO操作, 当子进程完成导出, 会用新的文件替换掉旧的文件.

                配置文件:
                    save 900 1
                    save 300 10
                    save 60 10000
                    从下往上看:
                        60 秒修改次数达到 10000 执行持久化 没有达到的时候 300 秒后再检查 更新有没有达到 10 次 如果没有 900 秒后 如果有一次更新, 便持久化

                    stop-writes-on-bgsave-error yes     如果导出RDB过程中出错了 主进程是否停止写入
                    rdbcompression yes                  是否对导出的RDB文件进行压缩
                    dbfilename dump.rdb                 导出的rdb文件名
                    rdbchecksum yes                     导出或存储rdb文件时是否校验
                    dir ./                              导出的rdb文件的路径

                不使用RDB持久化:
                    屏蔽 save 配置

            AOF:
                工作原理:
                    Redis 执行 fork(),现在同时拥有父进程和子进程
                    子进程开始将新 AOF 文件的内容写入到临时文件
                    对于所有新执行的写入命令,父进程一边将它们累积到一个内存缓存中,一边将这些改动追加到现有 AOF 文件的末尾,这样样即使在重写的中途发生停机,现有的 AOF 文件也还是安全的
                    当子进程完成重写工作时,它给父进程发送一个信号,父进程在接收到信号之后,将内存缓存中的所有数据追加到新 AOF 文件的末尾
                    Redis 原子地用新文件替换旧文件,之后所有命令都会直接追加到新 AOF 文件的末尾

                配置方式:
                    appendonly yes
                    appenfsync:
                        aways  每一个命令立即就执行一次 fsync : 非常慢,也非常安全
                        no     写入工作交给操作系统 由系统检测缓冲区大小统一写入到aop: 同步频率低, 速度快
                        eveysec 每秒执行一次 最多丢失1秒的数据
                    no-appendfsync-on-rewrite no    是否在导出RDB时停止AOF同步. 如果是yes, 在导出RDB文件时, 所有的同步AOF会被缓存在内存中的队列中, 不会丢失
                    appendfilename  path            aop日志文件的路径

                    日志重写:
                        直接把内存中的key/value 逆化成命令, 减小aof文件大小
                        auto-aof-rewrite-percentage 100 AOF文件大小是上次重写的文件大小2倍重写
                        auto-aof-rewrite-min-size 64mb  AOF文件大于64M时才重写
            redis恢复数据的时候, 如果 rdb和aof都存在时, 会使用aof恢复





