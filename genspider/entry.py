'''
制作人: 张浩铭
参与者: 张浩铭
时间: 2018.07
版本号: v1.0
内容描述: 爬虫运行脚本以及传参进入爬虫
'''

import os

if __name__ == "__main__":
    print("""使用方法:"['网址1', '网址2'...]",单双引号必须加上并且区分,若只有一个网址也必须写外面的括号和双引号，必须加http://或者https://""")
    print("示例1: "+'"'+"['http://www.cdgas.com/', 'http://www.swtjt.com/', 'http://www.cdsfl.org.cn/index.html']"+'"')
    print("示例2: "+'"'+"['http://www.swtjt.com/']"+'"')
    print("示例3: "+'"'+"['https://www.baidu.com/']"+'"')
    urls = input("请输入网址: ")
    os.system("scrapy crawl genspider -a augment={}".format(urls))