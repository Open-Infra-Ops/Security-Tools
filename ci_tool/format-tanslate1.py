from win32com import client as wc #导入模块
import os
import sys

# path = u'C:\George\DOCX'
path = u'D:\docs'

# 两个日志
def logerr(text):
    errlog = path + u'\文件转换失败列表.txt'
    with open(errlog, "a+") as f:
        f.write(text)
        f.write('\n')


def logok(text):
    infolog = path + u'\转换成功列表.txt'
    with open(infolog, "a+") as f:
        f.write(text)
        f.write('\n')

def doc_to_docx(path):
    for parent, dirnames, filenames in os.walk(path):
        for fn in filenames:
            filedir = os.path.join(parent, fn)
            if fn.endswith('.doc'):
                try:
                    word = wc.Dispatch("Word.Application")  # 打开word应用程序
                    doc = word.Documents.Open(filedir)  # 打开word文件
                    doc.SaveAs("{}x".format(filedir), 12)  # 另存为后缀为".docx"的文件，其中参数12指docx文件
                    doc.Close()  # 关闭原来word文件
                    word.Quit()
                    os.remove(filedir)
                    logok(filedir + ' 转换完成')
                    print("转换完成:"+filedir)
                except Exception as e:
                    # 写入修改失败日志
                    logerr(filedir)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        for arg in sys.argv:
            print(arg)
        print("参数错误，pyfile path")
        sys.exit(2)

    path = sys.argv[1]
    print("开始转换:"+path)
    doc_to_docx(path)