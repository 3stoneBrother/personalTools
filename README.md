# personalTools
分享一些安全小工具

## 公众号爬虫小脚本
gongzhonghao.py，会输出公众号的ID，运营的公司名称，公众号简介；
用法：python gongzhonghao.py -d "公司名称"

## sslinfo脚本，输入域名能看到其他域名
用法：python3 sslinfo.py -d "example.com"

## 脚本调用dnsdumper的一键生成图片功能
用法：python3 dnsdumpster.py -d target.com
功能：自动化生成域名的脑图结构，方便查看分析

## apk-getLink.sh 自动化提取apk中的域名和链接
用法：两个参数，第一个是apk的前缀，第二个是linkfinder的目录  
apk-getLink.sh “apk的前缀” $LINKFINDER_ROOT  
依赖：apktool工具，需自行安装；也需要[Linkfinder](https://github.com/GerbenJavado/LinkFinder.git)  

## 添加谷歌，百度，wayback 三个脚本  
为什么别人有了，还要写，因为现在的爬虫机制导致，单纯的python requests请求无法获取到资源，采用动态浏览器的方法，比较容易绕过反爬虫机制  
用法 wayback：
python wayback.py -d target.com  
用法：  
输出域名：   
python headless-spider-google.py -k "site:target.com" -od  
python headless-spider-baidu.py -k "site:target.com" -od  
输出链接:  
python headless-spider-google.py -k "site:target.com"   
python headless-spider-baidu.py -k "site:target.com" 





