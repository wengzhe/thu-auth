# THU-Auth
由于2018.4.2发现有线网需要使用全新的`auth4.tsinghua.edu.cn`进行认证，故新写了认证脚本。

## 运行
- 版本`Python 3`
- 依赖`sudo -H pip3 install -r requirements.txt`
- 请在当前目录下运行，或者修改load_config()的path参数。

## 配置
- 定义在最前面的`login_url`会全部被尝试，目前IPv6并不需要登陆，故注释掉了。

## 版本
- 长期维护中(~2020)
- 2018.4.3