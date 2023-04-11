import sys
sys.path.append(r'd:\git\inspirare6\wordx\src')
from wordx.word_file import WordFile


wf1 = WordFile('123.docx')
wf2 = WordFile('456.docx')

wf1.merge(wf2)
exit()