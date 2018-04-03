# THU-Auth
由于2018.4.2发现有线网需要使用全新的`auth4.tsinghua.edu.cn`进行认证，故新写了认证脚本。

## 配置
- `cp config/account.example.yaml config/account.yaml`
- 修改`config/account.yaml`里面的账号配置。

## 运行
- 版本`Python 3`
- 依赖`sudo -H pip3 install -r requirements.txt`
- 请在当前目录下运行，或者修改`load_config()`的`path`参数。

## `auth.py`
- 完整的认证代码，只支持上线操作，会通过获取页面自动判断是否在线，鲁棒性较好。
- 定义在`auth.py`最前面的`login_url`会全部被尝试，目前`IPv6`并不需要登陆，故注释掉了。
- 执行：`./auth.py`

## `auth_cmd.py`
- 精简的认证代码，针对当前版本进行精简，只进行IPv4登陆，并且不判断当前网络状况。
- 由参数控制登入登出
- 执行：`./auth_cmd.py login`或`./auth_cmd.py logout`

## 版本
- 长期维护中(~2020)
- 2018.4.3