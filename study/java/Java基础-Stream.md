1. 流与集合  
      流与集合类似，但有本质上的不同。
        
         1. Stream 提供了一个特定元素类型的有序值集合的接口。与集合不同的是，Stream 本身不存储数据，而是按需对其值进行计算。
         2. Stream 是不改变原来的数据。类似于不可表数据，总是返回一个新的数据集。
         3. 可以允许无限流上的计算在有限的时间内完成。
         4. 在 Stream 的生命周期中，它的元素只能被访问一次，如果希望重新访问 Stream 中相同的元素，则需要在返回的新的 Stream
2. 中间操作与终端操作
      
      中间操作指的是在对一个 Steam 进行操作时转换（或者说操作完成的返回值）的新的Stream，在流上执行终端操作时，不能再使用该流。
      终端操作指的是关闭 Stream 的操作，最后一个对 Stream 进行计算的操作(一般是一个方法) 
      例如
         
         List.stream().filter(s -> s.length() > 2).count();
         
         对一个 List 进行 filter() 操作，然后生成新的 Stream。（中间）
         然后将新的 Stream 进行了 count() （终端）
3. Optional 容器类

      一个可以为null的容器对象. 创建Optional 的3中方式:
         Optional.of()
         Optional.ofNullable()
         Optional.enpty()