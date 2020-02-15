#  这是一个绘制曲线到GUI的脚本。通过在一个主GUI中嵌套一个GUI函数来绘制曲线。

# coding: utf-8
import os, sys
import pandas as pd
import xlrd
import tushare as ts
from tkinter import *
import numpy as np
#  # 创建工具栏需要的库和# 创建画布需要的库
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#  # 创建工具栏需要的库
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
#  # 快捷键需要的库
from matplotlib.backend_bases import key_press_handler
# 导入画图常用的库
from matplotlib.figure import Figure
import time

import matplotlib.pyplot

mygui = Tk(className='股票历史数据查询系统')
# mygui.title('Dat')

mygui.wm_geometry('400x300+50+100')  # 设置窗口的大小，后面两个数字是窗口左上角的坐标值

label_0 = Label(mygui, width=15, text="打开本界面的时间：", anchor='w', justify='left')  # 建立一个标签，justify是文字对齐方式，anchor是文本在格子的方位。
label_0.grid(row=1, column=0, padx=5, pady=2, sticky="wesn")  # 这个命令是定义窗格的行数和列数，下面同理

textlabel0 = Text(mygui,width=30,height=1)  # 对应label_5
textlabel0.grid(row=1, column=1, padx=5, pady=2, sticky="wesn")
textlabel0.insert('insert', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

label_1 = Label(mygui, width=15, height=2, text="股票代码", anchor='w', justify='left')
label_1.grid(row=2, column=0, padx=5, pady=2, sticky="wesn")  # 一旦用了这个定义行的命令，后面每增加一个图标都要配上这个句子

entry_1 = StringVar()
entry_11 = Entry(mygui, width=30, fg='red', textvariable=entry_1)
entry_11.grid(row=2, column=1, padx=5, pady=2, sticky="wesn")
entry_11.insert("insert", '600848')

label_2 = Label(mygui, width=15, height=2, text="开始日期：\n(20XX-XX-XX)", anchor='w', justify='left')
label_2.grid(row=3, column=0, padx=5, pady=2, sticky="wesn")

entry_2 = StringVar()
entry_22 = Entry(mygui, width=30, fg='red')  # entry是输入框
entry_22.grid(row=3, column=1, padx=5, pady=2, sticky="wesn")
entry_22.insert("insert", '2018-01-01')

label_3 = Label(mygui, width=15, height=2, fg='black', background='white', text="结束日期：\n(20XX-XX-XX)", anchor='w', justify='left')
label_3.grid(row=4, column=0, padx=5, pady=2, sticky="wesn")

entry_3 = StringVar()
entry_33 = Entry(mygui, width=30, fg='red')  # entry是输入框
entry_33.grid(row=4, column=1, padx=5, pady=2, sticky="wesn")
entry_33.insert("insert", time.strftime("%Y-%m-%d", time.localtime()))

label_4 = Label(mygui, width=15, height=1, foreground='black', text="股票中文名", anchor='w', justify='left')
label_4.grid(row=5, column=0, padx=5, pady=2, sticky="wesn")


text = Text(mygui, width=30, height=1)  # 对应label_4
text.grid(row=5, column=1, padx=5, pady=2, sticky="wesn")
text.pack  # 另一种布局方式
# 设置 tag
text.tag_config("tag_1", backgroun="yellow", foreground="red")

def stock_search():  # 创建一个专门的画布函数，用来绘制股票曲线
    basedocu = xlrd.open_workbook('stock_code_name_mapping.xlsx', 'r')  # 打开用于存储代码和名字的表格
    sheetnum = basedocu.nsheets  # 获取源文件sheet数目
    bbb = entry_11.get()  # 将输入股票代码赋值给一个变量，用于检索
    stockname = "未命名"
    for m in range(0, sheetnum):
        sheet = basedocu.sheet_by_index(m)  # 读取源excel文件第m个sheet的内容
        nrowsnum = sheet.nrows  # 获取该sheet的行数
        # print(nrowsnum)  # 用于调试
        for i in range(0, nrowsnum):
            data = sheet.row(i)
            for n in range(0, len(data)):
                aaa = str(data[n])  # 把该行第n个单元格转化为字符串，目的是下一步的关键字比对
                if aaa == "number:{}.0".format(bbb.lstrip('0')):  # 进行关键字检索，因为excel的每个内容变成文本之后，开头会有number: 因此要把这个加上去。lstrip是把有些股票的左边的0去掉，因为excel里面的头部的0是没有的。
                    stockname = str(data[2]).strip('text:').strip('\'')
                    # "insert" 索引表示插入光标当前的位置
                    text.delete(1.0, 'end')  # 在标签实时显示
                    text.insert("insert", '{}'.format(str(data[2]).strip('text:').strip('\'')))  # 用strip来去除开头的“text:”文本和首尾的标点\’，显示第3列数据

    df1 = ts.get_k_data(entry_11.get(), start=entry_22.get(), end=entry_33.get())
    str1 = df1['close']  # 提取K线中的收盘价
    startdate = df1['date']  # 取出时间列表
    df2 = ts.get_k_data('sh', start=startdate[0], end=entry_33.get())  # 同期的上证指数
    str2 = df2['close']  # 同期上证指数
    x = range(len(str1))  # 日期
    y = str1  # 收盘价
    x1 = range(len(str2))
    z = str2  # 同期上证收盘价

    root = Tk()  # 创建tkinter的主窗口
    root.title('{}和上证指数对比'.format(stockname))
    root.wm_geometry('480x480+450+50')
    f = Figure(figsize=(5, 4), dpi=100)  # 通过new_figure_manager（新图形管理器）返回一个figure图形实例。定制的figure类将与pylab接口进行关联，同时将相关参数传递给figure的初始化函数
    a = f.add_subplot(211)  # 添加子图:2行1列第1个
    b = f.add_subplot(212)  # 添加子图:2行1列第2个
    f.suptitle('{} VS \'sh\'\n{} to {}'.format(entry_11.get(), startdate[0], entry_33.get()), color='b')
# 在前面得到的子图上绘图
    a.plot(x, y)
    b.plot(x1, z)

# 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(f, master=root)  # master是要显示图形的GUI对象。
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
# 显示画布
    canvas.get_tk_widget().pack(side=TOP,  # 上对齐
                            fill=BOTH,  # 填充方式
                            expand=YES)  # 随窗口大小调整而调整
# matplotlib的导航工具栏显示上来(默认是不会显示它的)，# 创建工具条
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP,  # get_tk_widget()得到的就是_tkcanvas
                        fill=BOTH,
                        expand=YES)
# 调用快捷键
    def on_key_event(event):
        """键盘事件处理"""
        print("你按了%s" % event.key)
        key_press_handler(event, canvas, toolbar)
# 绑定上面定义的键盘事件处理函数
    canvas.mpl_connect('key_press_event', on_key_event)
    def _quit():
        """点击退出按钮时调用这个函数"""
        root.quit()  # 结束主循环
        root.destroy()  # 销毁窗口

    # 创建一个按钮,并把上面那个函数绑定过来
    button = Button(master=root, text="退出", command=_quit)
    # 按钮放在下边
    button.pack(side=BOTTOM)
    # 主循环
    root.mainloop()


btn = Button(mygui, text="获取数据和曲线", command=stock_search)
btn.grid(row=15, column=1, padx=5, pady=2, sticky="wesn")
btn.pack

mygui.mainloop()  # 输入页面的主循环
# end of this script

