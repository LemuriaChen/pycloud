
## automated cloud disk management tools

### features

* 百度云盘
    * 用户登陆和用户和文件管理
    * 百度云链接自动保存
* 坚果云 (TODO)
    
### install

```shell script
pip install pycloud
```

### dependence

记住 chrome driver 的版本要与 chrome 相对应。

* [google chrome](https://www.google.cn/intl/zh-CN/chrome/)
* [google chrome driver](https://npm.taobao.org/mirrors/chromedriver/)

### usage

假设你有很多百度云盘链接，现在想通过一些脚本自动保存到自己的云盘上，可以通过下面的步骤进行操作。

* 手动登陆并保存 cookie 到特定到目录

打开 ipython，运行以下代码。 

```python
from pycloud.netdisk import NetDisk

nd = NetDisk()
nd.manual_login()   # 运行到这一步会跳出一个浏览器界面，然后我们输入用户名和密码进行手动登陆

nd.save_cookie()    # 然后调用 save_cookie 函数保存 cookie, cookie 默认保存在 /home/user/.cookie 文件夹下
```

* 使用 cookie 登陆个人云盘，并遍历分享链接，进行批量保存（或者使用多进程加快保存速度）

```python

from pycloud.netdisk import NetDisk

nd = NetDisk()
nd.login_with_cookie()

items = [
    ('https://pan.baidu.com/s/1NxtrD9QbONy0xRxqXut5Bw', '8irj'),
    ('https://pan.baidu.com/s/1YJw9auKFnKMSeJaYb1PJTg', 'mqxz'),
    ('https://pan.baidu.com/s/17YYdXFyHjVAvbka0J2BFug', 'f8aa'),
    ('https://pan.baidu.com/s/1010Vnz9YZq6ygcsawKqiPw', 'fw38'),
    ('https://pan.baidu.com/s/1T4Chc6h14NOWLPSQI7VVQw', '7tuk'),
    ('https://pan.baidu.com/s/1tvDg7beobRmmFgtLP0zgXQ', 'a9z2'),
    ('https://pan.baidu.com/s/11-cMUa52HGoP_B13yDKhCw', 'p7da'),
]

for url, pwd in items:
    nd.save(url=url, pwd=pwd, save_path='share', verbose=True)

# 注意： 
# 1. 如果不是别人分享的百度云盘链接，调用 save 函数到时候，pwd 参数留空即可 
# 2. cookie 有效期暂时还没测试过，不过应该至少超过 24 个小时
# 3. save_path 参数的格式为 'dir1/dir2/dir3'，save 函数会自动为不存在的路径创建文件夹
```

