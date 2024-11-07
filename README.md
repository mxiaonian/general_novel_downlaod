# general_novel_downlaod
可配置规则的通用小说下载器
基于自动化浏览器操作，可绕过绝大部分反爬措施，可自定义规则，通过xpath,class,id,tag等定位需要获取的部分。
单属性匹配符 @
单个@在只以一个属性作为匹配条件时使用，以'@'开头，后面跟属性名称。
如：
~~~
@class=class_name
~~~
多属性与匹配符 @@
当需要多个条件同时确定一个元素时，每个属性用'@@'开头。
~~~
@@class=class_name@@tag=a
~~~
则匹配的是网页中元素class名为class_name且标签为a的元素

xpath匹配
如：
~~~
xpath:/html/body/div[3]/div[1]/div/div/div[2]/div[1]/h1
~~~

如果网站有字体加密，则可以通过另一个小脚本，通过配置字体映射的和编码获取的方式来进行解密。
