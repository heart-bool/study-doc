"""
    open()函数:
        操作模式	具体含义
        'r'	读取 （默认）
        'w'	写入（会先截断之前的内容）
        'x'	写入，如果文件已经存在会产生异常
        'a'	追加，将内容写入到已有文件的末尾
        'b'	二进制模式
        't'	文本模式（默认）
        '+'	更新（既可以读又可以写）
"""
import json


def main():
    """读取文本文件示例"""
    complete_read('C:/Users/awafen1/Desktop/武汉.xml', 'r', 'utf-8')
    i = 0
    for block in block_read('C:/Users/awafen1/Desktop/武汉.xml', 'r', 'utf-8', 100):
        i = i + 1
        print('第%d次读取: %s' % (i, block))
    readLines('C:/Users/awafen1/Desktop/武汉.xml', 'r', 'utf-8')
    mydict = {
        'name': '骆昊',
        'age': 38,
        'qq': 957658,
        'friends': ['王大锤', '白元芳'],
        'cars': [
            {'brand': 'BYD', 'max_speed': 180},
            {'brand': 'Audi', 'max_speed': 280},
            {'brand': 'Benz', 'max_speed': 320}
        ]
    }
    writeJSON(mydict, 'data.json', 'w', 'utf-8')
    readJSON('data.json', 'r', 'utf-8')


# 完整文件读取
def complete_read(path, mode, encoding):
    # f = open('C:/Users/awafen1/Desktop/武汉.xml', 'r', encoding='utf-8')
    # print(f.read())
    # f.close()
    """"如上代码如果遇到文件不存在，或者无法打开的情况，将会发生异常。这时可以利用python的异常机制"""

    f = None
    try:
        f = open(path, mode, encoding=encoding)
        print(f.read())
    except FileNotFoundError:
        print("找不到指定的文件")
    except LookupError:
        print('指定的编码不正确')
    except UnicodeDecodeError:
        print('读取文件时解码错误')
    finally:
        if f:
            f.close()


# 分块读取
def block_read(path, mode, encoding, size=4096):
    f = None
    try:
        f = open(path, mode, encoding=encoding)
        while True:
            data = f.read(size)
            if not data:
                break
            yield data

    except FileNotFoundError:
        print("找不到指定的文件")
    except LookupError:
        print('指定的编码不正确')
    except UnicodeDecodeError:
        print('读取文件时解码错误')
    finally:
        if f:
            f.close()


# 使用with open 读取
def readLines(path, mode, encoding):
    try:
        i = 0
        with open(path, mode, encoding=encoding) as f:
            for lien in f:
                i = i + 1
                print('正在读取第%d行, 结果为:\n%s' % (i, lien))

    except FileNotFoundError:
        print("找不到指定的文件")
    except LookupError:
        print('指定的编码不正确')
    except UnicodeDecodeError:
        print('读取文件时解码错误')
    finally:
        if f:
            f.close()


# 操作JSON数据
def writeJSON(source, path, mode, encoding):
    try:
        with open(path, mode, encoding=encoding) as f:
            json.dump(source, f)
    except IOError as e:
        print(e)
    print('保存成功')


def readJSON(path, mode, encoding):
    try:
        with open(path, mode, encoding=encoding) as f:
            load = json.load(f)
            print(load)
    except IOError as e:
        print(e)


if __name__ == '__main__':
    main()
