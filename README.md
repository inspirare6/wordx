# WordX
以"高度定制化"Word模板实现Word文档自动生成。


## 安装
```shell
pip install wordx
```

## 基本使用
```python
from wordx.sheet import Sheet 


sheet = Sheet('template.docx')
sheet.render(data)
sheet.save('output.docx')
```

## 模板压制
制作Word模板需配套使用word模板工具   
![Word模板工具箱](https://raw.githubusercontent.com/inspirare6/wordx/master/assets/img/wordx-tool.png)

Word文件模板示例   
![Word模板示例](https://raw.githubusercontent.com/inspirare6/wordx/master/assets/img/word-template.png)


