# Find_CET_id

用于根据身份证号找回CET考试的准考证号。

## 原理

1.使用request访问http://cet-bm.neea.edu.cn/Home/QuickPrintTestTicket

2.构造session，识别验证码，提交表单

3.下载准考证，解压后读取PDF，正则表达式匹配准考证号

4.通过flask框架提供api，接受用户提交并返回

