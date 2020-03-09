# personalTools
分享一些安全小工具

## 公众号爬虫小脚本
gongzhonghao.py，会输出公众号的ID，运营的公司名称，公众号简介；
用法：python gongzhonghao.py -d "公司名称"
---
## sslinfo脚本，输入域名能看到其他域名
用法：python3 sslinfo.py -d "example.com"
---
## 脚本调用dnsdumper的一键生成图片功能
用法：python3 dnsdumpster.py -d target.com
功能：自动化生成域名的脑图结构，方便查看分析
---
## apk-getLink.sh 自动化提取apk中的域名和链接
用法：两个参数，第一个是apk的前缀，第二个是linkfinder的目录
apk-getLink.sh “apk的前缀” $LINKFINDER_ROOT
依赖：apktool工具，需自行安装；也需要[Linkfinder](https://github.com/GerbenJavado/LinkFinder.git)
