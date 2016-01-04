#format_converter

该项目的用途相当的简单，是用来转换数据格式的。 比如把json转换成yaml,json转换成csv. 现在支持的格式有json、txt、csv、yaml.

##安装:
```
pip install format_converter
```

##使用说明:
```python
from format_converter import converter

data = converter < 'data.json'
```

读取配置
```
data = converter < 'file.json'
data = converter < 'file.txt'
data = converter.json < 'file.json'
data = converter.yml < 'file.yml'
data = converter.csv < 'file.csv'
```

写入配置
```
converter(data) > 'file.json'
converter(data) > 'file.txt'
converter.json(data) > 'file.json'
converter.yml(data) > 'file.yml'

```

