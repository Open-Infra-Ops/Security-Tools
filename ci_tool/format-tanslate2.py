from win32com.client import Dispatch
from os import walk
import sys

wdFormatPDF = 17

def doc2pdf(input_file):
    word = Dispatch('Word.Application')
    doc = word.Documents.Open(input_file)
    outputfile = input_file.replace(".docx", ".pdf")
    doc.SaveAs(outputfile, FileFormat=wdFormatPDF)
    doc.Close()
    print('PDF生成成功: ' + outputfile)
    word.Quit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        for arg in sys.argv:
            print(arg)
        print("参数错误，pyfile path")
        sys.exit(2)
    path = sys.argv[1]
    print("开始转pdf:" + path)
    for root, dirs, filenames in walk(path):
        for file in filenames:
            if file.endswith(".docx"):
                doc2pdf(str(root + "\\" + file))