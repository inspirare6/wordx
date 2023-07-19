# WordX
Word自动化渲染库  
```python
from wordx.sheet import Sheet 


sheet = Sheet('template.docx')
sheet.render(data)
sheet.save('output.docx')
```
制作Word模板需配套使用word模板工具
![Word模板工具箱](./img/wordx-tool.png)

Word文件模板示例
![Word模板示例](./img/word-template.png)


