package com.bool.study.集合;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

/***
 * List 相关集合类的解析
 *
 */
public class ListTest {

	public static void main(String[] args) {

		/*
		 * ArrayList:
		 * 		特点: 基于数组的列表集合, 所以具有数组的相关特性. 随机访问的效率较高, 直接通过下标即可访问到元素. 删除和移动元素的效率低, 需要遍历整个数组.
		 *
		 * 		源码解析:
		 *
		 * 		成员变量解析:
		 *
		 *     	默认初始化长度 10
		 *		private static final int DEFAULT_CAPACITY = 10;
		 *
		 *		当前的 elementData 通过初始化长度的构造方法初始化时将直接初始化 elementData 的长度
		 * 		private static final Object[] EMPTY_ELEMENTDATA = {};
		 *
		 *
		 *      当前的 elementData 是没有指定容量的构造方法初始化时, 将在第一个元素被添加的时候初始化 elementData 的长度为默认的 DEFAULT_CAPACITY
		 *		private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
		 *
		 *		存储元数据的数组对象, 实例被创建之后所有操作都跟这个属性有关.
		 *	 	非私有，以简化嵌套类访问
		 *		transient Object[] elementData;
		 *
		 * 		当前 elementData 的元素个数
		 *      private int size;
		 *
		 *		构造方法:
		 *		默认构造方法, elementData 将在第一个元素被添加时进行初始化
		 *	 	public ArrayList() {
		 *         this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
		 *     }
		 *
		 * 		指定初始化长度
		 * 		public ArrayList(int initialCapacity) {
		 * 			initialCapacity 大于 0 则设置 elementData 的长度进行初始化
		 *         if (initialCapacity > 0) {
		 *             this.elementData = new Object[initialCapacity];
		 *         } else if (initialCapacity == 0) {
		 *             this.elementData = EMPTY_ELEMENTDATA;
		 *         } else {
		 *             throw new IllegalArgumentException("Illegal Capacity: "+
		 *                                                initialCapacity);
		 *         }
		 *     }
		 *
		 *     将一个以 Collection 子类的集合类型的实例作为初始化 elementData 的条件
		 *     public ArrayList(Collection<? extends E> c) {
		 *         elementData = c.toArray();
		 *         if ((size = elementData.length) != 0) {
		 *             // c.toArray might (incorrectly) not return Object[] (see 6260652)
		 *             if (elementData.getClass() != Object[].class)
		 *                 elementData = Arrays.copyOf(elementData, size, Object[].class);
		 *         } else {
		 *             // replace with empty array.
		 *             this.elementData = EMPTY_ELEMENTDATA;
		 *         }
		 *     }
		 *
		 *		扩容:
		 *		ArrayList 在添加元素时, 如果当前 elementData 长度不足(比如默认为10, 在添加第11个元素的时候)会对 elementData 进行扩容.
		 *		每次扩充的长度为:
		 *			int oldCapacity = elementData.length;
		 *			int newCapacity = oldCapacity + (oldCapacity >> 1);
		 *		也就是当前 elementData 长度的一半.
		 *
		 */
		List<Integer> list = new ArrayList<>();
		for (int i = 0; i < 20; i++) {
			list.add(i);
		}
		list.add(null);
		list.add(null);
		System.out.printf("111");


		/*
		 *
		 * LinkedList:
		 *
		 * 	特点: 维护一个双向链表。有序列表，按照元素的添加顺序保存元素顺序. 元素可以为null。添加和删除效率高, 随机访问效率低
		 *
		 *	查找元素的方式:
		 *		以下标的形式访问时, LinkedList 会将当前列表的长度右移两位(除2), 如果指定的index小于结果则从头开始遍历, 拿到指定index的上一个Node的next Node.
		 *		否则从尾部进行遍历, 拿到指定index的下一个元素的prev Node;
		 *
		 */
		List<Integer> linkedList = new LinkedList<>();
		linkedList.add(1);
		linkedList.add(2);
		linkedList.add(3);
		linkedList.add(6);
		linkedList.add(5);
		linkedList.add(7);
		linkedList.add(7);
		linkedList.add(8);
		linkedList.add(9);
		linkedList.add(null);
		linkedList.add(null);
		linkedList.forEach(System.out::println);






		ArrayList<T1> aList = new ArrayList<>();
		aList.add(new T1(0,2));
		aList.add(new T1(1,3));
		aList.add(new T1(2,4));
		aList.add(new T1(3,5));
		aList.add(new T1(4,6));
		aList.add(new T1(5,7));

		int [][] arr = {
				{2},
				{3},
				{3},
				{3},
				{3},
				{3},
		};

		int size = aList.size();
//		for (int i = 0; i < size; i++) {
//			T1 t1 = aList.get(i);
//			System.out.println(i+"");
//			arr[t1.getX()][t1.getY()] = 2;
//		}
		char c = (char) -128;

		int i = (int) c;
		System.out.println(c+ " "+ i);

		for (byte j = -128; j < 128; j++) {
			System.out.println(j++);
		}

		/*
		 * Map
		 *
		 *
		 *
		 *
		 *
		 */
	}

	static class T1{
		private int x;
		private int y;

		public T1(int x, int y) {
			this.x = x;
			this.y = y;
		}

		public int getX() {
			return x;
		}

		public void setX(int x) {
			this.x = x;
		}

		public int getY() {
			return y;
		}

		public void setY(int y) {
			this.y = y;
		}
	}

}
