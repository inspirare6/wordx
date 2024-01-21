import sys
sys.path.append(r'd:\git\inspirare6\wordx\src')

from wordx.report import Report 



report = Report('template.docx', 'components')


report.render({
    'data':[{
    'type': 'paragraph',
    'content': '123'
}]})
report.save('test.docx')