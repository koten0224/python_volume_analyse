# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 14:18:27 2019

@author: pipiching
"""
'''
被腰斬的UI
'''
import tkinter as tk
import webbrowser

class GUI:
    def __init__(self):
        window = tk.Tk()
        window.title('文章分類器')
        window.geometry('1000x800')
        
        title = tk.Label(window, text = '自製文章分類器', font=('標楷體', 30), width=50, height=2) #主標題
        title.pack()
        
        frame = tk.Frame(window)
        frame.pack()
        
        frame_l = tk.Frame(frame, width = 450, height =500)
        frame_r = tk.Frame(frame, width = 450, height =500)
        frame_l.pack(side='left')
        frame_r.pack(side='right')        
        
# ================================= 左半部視窗 ============================================
        title_1 = tk.Label(frame_l, text = '文本輸入', font=('標楷體', 20), width=30, height=2) #左邊標題
        scrollbar = tk.Scrollbar(frame_l)        
        article = tk.Text(frame_l, width=60, height=30, yscrollcommand=scrollbar.set) #文本接收
        enter = tk.Button(frame_l, text = '確定', width=50, height=2, command = lambda : self.Get_Input(article))
        title_1.pack()
        scrollbar.pack(side='right', fill='y')        
        article.pack(fill='both')
        scrollbar.config(command=article.yview)
        enter.pack()       
        
# ================================= 右半部視窗 ============================================        
        title_2 = tk.Label(frame_r, text = '類別', font=('標楷體', 20), width=30, height=2) #右邊標題
        plotly = tk.Button(frame_r, text='匯出分析圖表',  width=50, height=10, command = self.Show_Plotly)        
        class_ = ['遊戲','運動','投資','生活','科幻','心情','娛樂','科技','政治','閒聊','學術']
        Rad = []
        var = [] #選擇器開關
        for i in range(len(class_)):
            var.append(tk.IntVar())
            Rad.append(tk.Checkbutton(frame_r, text=class_[i], variable=var[i], onvalue=1, offvalue=0))         

        title_2.place(x = 30, y = 10)        
        for j in range(len(Rad)):
            if j % 2 == 0:
                Rad[j].place(x=110, y=100 + 20 * j)
            else:
                Rad[j].place(x=310, y=100 + 20 * (j-1) )
        plotly.place(x = 60, y = 330)
# =======================================================================================
        window.mainloop()
        
    def Get_Input(self, article):
        content = article.get(1.0, "end-1c") # 得到內文
        output = self.Classification(content)
        clas = output[0]
        urls = output[1:]
        
        window2 = tk.Tk()
        window2.title('結果')
        window2.geometry('500x400')            

        cla_title = tk.Label(window2, text = '分類', font=('標楷體', 10))
        cla = tk.Text(window2, width=40, height=5)
        link_title = tk.Label(window2, text = '文章建議', font=('標楷體', 10))
        link = tk.Text(window2, width=40, height=20)
        link.tag_config('link', foreground='blue', underline=True)
        
        cla.insert('insert', clas)
        
# ==================================  超連結  ==================================================
        def show_hand_cursor(event):
            link.config(cursor='arrow')
        def show_arrow_cursor(event):
            link.config(cursor='xterm')
        def click(event,x):
            webbrowser.open(x)
        def handlerAdaptor(fun,**kwds):
            return lambda event,fun=fun,kwds=kwds:fun(event,**kwds)
        m=0
        for url in urls:
            link.tag_config(m,foreground='blue',underline=True)
            link.tag_bind(m,'<Enter>',show_hand_cursor)
            link.tag_bind(m,'<Leave>',show_arrow_cursor)
            
            link.insert('insert', url+'\n', m)
        
            link.tag_bind(m,'<Button-1>',handlerAdaptor(click,x=urls[m]))
            m+=1        
        
        cla_title.pack()
        cla.pack()
        link_title.pack()
        link.pack()
        
        window2.mainloop()
        
    def Show_Plotly(self):
        webbrowser.open('127.0.0.1:8050')
    
    def Classification(self, content):
        # 文章分類打在這
        return 'novel', 'https://www.google.com/', 'https://www.yahoo.com', 'https://www.yahoo.com', 'https://www.yahoo.com', 'https://www.yahoo.com', 'https://www.yahoo.com'

GUI()

