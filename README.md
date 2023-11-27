# logging2feishu
把python中的打印同步到飞书多维表格中。可实时查看某个脚本的运行log。方便各位AI训练师或AI画师炼丹过程中，实时查看模型或LORA等的训练情况（默认设置90s更新一次到飞书），及时查看是否模型训练得偏了，能立即进行中止或修改重新训练，无需要一直守在电脑前。

## Introduction 主要构成介绍

### 1. feishu

- Introduction of feishu

个人暂时（2023.11）觉得算是最好的在线文档，很多地方与notion很像。

- BaseOpenSDK for feishu(Python)

具体官方文档参见https://bytedance.larkoffice.com/wiki/E95iw3QohiOOolkjmXwcVsC5nae   。但不是很详细，我已在pythonFeishuConnector.py中把主要的方法都封装实现了。

### 2.logging

python最常用的log模块，有兴趣可以到官网查看



## Usage 使用

- 1.使用以下命令安装pip库：pip install logging2feishu -i https://pypi.python.org/pypi
  
- 2.导入logging2feishuShower模板  
  
- 3.获取多维表格的获取自己的飞书app_token,personal_base_token,以及“实时结果”与“历史记录”的table_id。获取方式： PC端--侧边栏--插件市场--开发工具中查看table_id，BASE ID即app_token，另点开发工具的设置可获取个人授权码personal_base_token。具体见附图.
  
- 4.在自己项目中创建config.json，把上述参数填入文件中，通过config_file传入文件名即可或直接初始化logging2feishu的logger时通过参数传入（不通过文件传入）
  
- 5.config.json格式样例如下：
```
 {
        "feishu_app_token" : "xxxxxxxxxxo",
        "feishu_personal_base_token" : "pt-Xnxxxxxxxxx",
        "feishu_table_id" : "tblxxxxxxx",
        "feishu_history_table_id" : "tblaxxxxxxxt"
   }
```
- 6.项目中使用时如python的logging模块使用即可：
```
#载入库
from logging2feishu import Logger
#实例logger
lo= Logger(name='haha', file='test2.log',updateInterval=20,
            config_file='config.json')
#debug、info、warning、error等调用  
lo.debug('1111111info level是qqqqqq12sdf3')
```
