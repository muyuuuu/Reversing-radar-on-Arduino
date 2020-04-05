import sys
import time
import random
import queue
from PyQt5.QtCore import Qt, QPointF, QRectF, QVariantAnimation, QAbstractAnimation, QTimer
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QGraphicsRectItem, QGraphicsScene,
                             QGraphicsView, QMainWindow, QGridLayout, QFrame,
                             QSplitter, QWidget, QTextEdit, QVBoxLayout, QPushButton,
                             QGraphicsItem, QHBoxLayout, QLabel, QLineEdit, QGridLayout)
from functools import partial


class RectItem(QGraphicsRectItem):
    def __init__(self, rect=QRectF()):
        super(RectItem, self).__init__(rect)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self._pos_animation = QVariantAnimation()
        self._pos_animation.valueChanged.connect(self.setPos)

    def move_smooth(self, end, duration):
        if self._pos_animation.state() == QAbstractAnimation.Running:
            self._pos_animation.stop()
        self._pos_animation.setDuration(duration)
        self._pos_animation.setStartValue(self.pos())
        self._pos_animation.setEndValue(end)
        self._pos_animation.start()


# 负责绘制车辆的类
class GraphicsView(QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()

        # 创建图形容器
        # 将车库实体化为 宽度450 长度600 大小
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 400, 500)

        # 创建车辆实例
        self.rect = RectItem()

        # 初始化位置为 30 30 车辆宽度 250 长度 400
        self.rect.setRect(0, 0, 260, 400)

        # 创建颜色刷子
        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(QColor(124, 214, 175))

        # 给车身上色
        self.rect.setBrush(brush1)

        # 将车身添加到容器中 即放到车库里
        self.scene.addItem(self.rect)

        # 设置当前场景
        self.setScene(self.scene)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 设置文字的字体
        font = QFont()
        font.setFamily("Microsoft Yahei")
        font.setPointSize(11)

        btn_list = []

        # 整体布局
        pagelayout = QHBoxLayout()

        # 左侧开始布局
        left_layout = QGridLayout()

        btn_start = QPushButton("倒车")
        btn_start.setFixedSize(100, 80)
        left_layout.addWidget(btn_start, 0, 0)
        btn_list.append(btn_start)

        btn_forward = QPushButton("前进")
        btn_forward.setFixedSize(100, 80)
        left_layout.addWidget(btn_forward, 0, 1)
        btn_list.append(btn_forward)

        btn_lift = QPushButton("解除")
        btn_lift.setFixedSize(100, 80)
        left_layout.addWidget(btn_lift, 0, 2)
        btn_list.append(btn_lift)

        btn_left = QPushButton("左转")
        btn_left.setFixedSize(100, 80)
        left_layout.addWidget(btn_left, 1, 0)      
        btn_list.append(btn_left)

        btn_stop = QPushButton("停车")
        btn_stop.setFixedSize(100, 80)
        left_layout.addWidget(btn_stop, 1, 1)      
        btn_list.append(btn_stop)

        btn_right = QPushButton("右转")
        btn_right.setFixedSize(100, 80)
        left_layout.addWidget(btn_right, 1, 2)      
        btn_list.append(btn_right)

        btn_back = QPushButton("后退")
        btn_back.setFixedSize(100, 80)
        left_layout.addWidget(btn_back, 2, 1)      
        btn_list.append(btn_back)

        btn_slow = QPushButton("减速")
        btn_slow.setFixedSize(100, 80)
        left_layout.addWidget(btn_slow, 2, 2)      
        btn_list.append(btn_slow)
                                                   
        pagelayout.addLayout(left_layout)

        for btn in btn_list:
            btn.setFont(font)

        # 右侧开始布局
        right_layout = QVBoxLayout()

        # 右上侧开始布局 ----------------------------------------------
        # 创建左侧的文本编辑器  用于显示距离数字
        left_label = QLabel("左")
        left_label.setFixedSize(28, 30)
        self.left_line = QLineEdit()
        self.left_line.setFixedSize(88, 30)
        back_label = QLabel("后")
        back_label.setFixedSize(28, 30)
        self.back_line = QLineEdit()
        self.back_line.setFixedSize(88, 30)
        right_label = QLabel("右")
        right_label.setFixedSize(28, 30)
        self.right_line = QLineEdit()
        self.right_line.setFixedSize(88, 30)

        top_right_layout = QHBoxLayout()
        top_right_layout.addWidget(left_label)
        top_right_layout.addWidget(self.left_line)
        top_right_layout.addWidget(back_label)
        top_right_layout.addWidget(self.back_line)
        top_right_layout.addWidget(right_label)
        top_right_layout.addWidget(self.right_line)

        # 右侧开始布局 ----------------------------------------------
        #　添加右侧的倒车情景
        g = GraphicsView()
        self.car = g.rect
        self.scene = g.scene
        # print(self.scene.x())
        right_layout.addLayout(top_right_layout)
        right_layout.addWidget(g)
        pagelayout.addLayout(right_layout)

        # 设置最终的窗口布局与控件-------------------------------------
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        btn_start.clicked.connect(self.run)

    def update(self):
        ql = queue.Queue(2)
        left = int(self.item.x())
        qb = queue.Queue(2)
        back = int(self.item.y())
        ql.put(left)
        qb.put(back)
        if ql.qsize() == 1:
            self.left_line.setText(str(left))
        else:
            if left - ql.get() > 1:
                self.left_line.setText(str(left))
        if qb.qsize() == 1:
            self.back_line.setText(str(100 - back))
        else:
            if back - qb.get() > 1:
                self.back_line.setText(str(100 - back))

    def move_pos(self, scene):
        Left = [i for i in range(30, 50, 2)]
        Center = [i for i in range(70, 80, 2)]
        for it in scene.items():
            self.item = it
            for left, center in zip(Left, Center):
                pos = QPointF(left, center)
                if hasattr(it, 'move_smooth'):
                    it.move_smooth(pos, 5000)
                    it._pos_animation.valueChanged.connect(self.update)

    def run(self):
        wrapper = partial(self.move_pos, self.scene)
        timer = QTimer(interval=5000, timeout=wrapper)
        timer.start()
        wrapper()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())
