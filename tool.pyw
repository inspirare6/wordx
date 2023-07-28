from zgui import * 
from tkinter.ttk import Notebook
from wordx.word_file import WordFile 
from utility import SuperWordFile
import sys
import time 


app =  App({'title':'WordX模板工具箱','size':(420,330),'loc':(500,300)})

root = app.instance

note1=Notebook(root) 
note1.pack(fill=BOTH,expand=True)
 
fr1=Frame(root,relief='ridge', borderwidth=1) 
fr2=Frame(root,relief='ridge', borderwidth=1)
fr3=Frame(root,relief='ridge', borderwidth=1)

note1.add(fr1,text='编辑') 
note1.add(fr2,text='测试') 

label1 = Label(fr1, text='模板目录')
label1.pack()
label1.place(x=5,y=5)

label2 = Label(fr1, text='模板文件')
label2.pack()
label2.place(x=5,y=30)

label3 = Label(fr1, text='资源文件')
label3.pack()
label3.place(x=5,y=55)

label4 = Label(fr1, text='写入路径')
label4.pack()
label4.place(x=5,y=80)

input1 = app.input(fr1, print, width=48)
input1.pack()
input1.place(x=65,y=5)

input2 = app.input(fr1, print, width=48)
input2.pack()
input2.place(x=65,y=30)

input3 = app.input(fr1, print, width=48)
input3.pack()
input3.place(x=65,y=55)

input4 = app.input(fr1, print, width=48)
input4.pack()
input4.place(x=65,y=80)


def get_edit_input():
    folder = input1.get()
    file = input2.get()
    return folder, file

def on_click_extract_document():
    folder, file = get_edit_input()
    wf = SuperWordFile(folder, file)
    wf.extract('document.xml')

def on_click_extract_header():
    folder, file = get_edit_input()
    wf = SuperWordFile(folder, file)
    wf.extract('header.xml')

def on_click_extract_footer():
    folder, file = get_edit_input()
    wf = SuperWordFile(folder, file)
    wf.extract('footer.xml')

def on_click_generate():
    folder, file = get_edit_input()
    wf = SuperWordFile(folder, file)
    wf.generate()

def on_click_test():
    folder, file = get_edit_input()
    wf = SuperWordFile(folder, file)
    wf.test()

def on_click_write():
    folder = input1.get()
    tpl_file = input2.get()
    res_file = input3.get()
    res_path = input4.get()
    wf = SuperWordFile(folder, tpl_file)
    wf.write(res_file, res_path)

def on_click_render():
    folder, file = get_edit_input()
    wf = SuperWordFile(folder, file)
    wf.render()

def on_click_word2xml_h():
    SuperWordFile.word2xml('h')

def on_click_word2xml_v():
    SuperWordFile.word2xml('v')

def on_click_xml2word_h():
    SuperWordFile.xml2word('h')

def on_click_xml2word_v():
    SuperWordFile.xml2word('v')

button = app.button(fr1, '提取document', on_click_extract_document, width=13)
button.pack()
button.place(x=30,y=110)

button = app.button(fr1, '提取header', on_click_extract_header, width=13)
button.pack()
button.place(x=155,y=110)

button = app.button(fr1, '提取footer', on_click_extract_footer, width=13)
button.pack()
button.place(x=280,y=110)

button = app.button(fr1, '组装', on_click_generate, width=22)
button.pack()
button.place(x=30,y=145)

button = app.button(fr1, '测试', on_click_test, width=22)
button.pack()
button.place(x=220,y=145)

button = app.button(fr1, '渲染', on_click_render, width=49)
button.pack()
button.place(x=30,y=180)

button = app.button(fr1, '写入', on_click_write, width=49)
button.pack()
button.place(x=30,y=215)

button = app.button(fr2, 'word转xml(竖向)', on_click_word2xml_v, width=49)
button.pack()
button.place(x=30,y=30)

button = app.button(fr2, 'word转xml(横向)', on_click_word2xml_h, width=49)
button.pack()
button.place(x=30,y=80)

button = app.button(fr2, 'xml转word(竖向)', on_click_xml2word_v, width=49)
button.pack()
button.place(x=30,y=130)

button = app.button(fr2, 'xml转word(横向)', on_click_xml2word_h, width=49)
button.pack()
button.place(x=30,y=180)

app.run()