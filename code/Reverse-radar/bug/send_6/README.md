### BUG 描述

- 首先电路层面连接蓝牙
- 而后启动py文件即可

即使什么都不做，`flag`自己也会变成1。输出如下：

```py
b'0\r\n'
b'0\r\n'
b'0\r\n'
b'0\r\n'
b'0\r\n'
b'0\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
b'1\r\n'
```

尽管后期发送了 6，`flag` 的值仍然为1。问题在`py`代码中，而非`Arduino`或串口的问题。

### BUG修复

线程启动后，会自动连接`run`函数，因此导致发送的 6 无效。

`run`函数被两个信号连接，第一个是鼠标点击信号，第二个是多线程绘制的信号。因此需要将鼠标点击关联两个信号，当确定鼠标点击时才出发`run`函数中的`self.com.begin()`信息。