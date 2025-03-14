# SPCloud Python SDK 使用文档

## 目录
1. [简介](#简介)
2. [环境要求](#环境要求)
3. [入门指南](#入门指南)
4. [核心功能](#核心功能)
5. [错误处理](#错误处理)
6. [示例代码](#示例代码)

## 简介

SPCloud Python SDK 是一个用于云计算和授权验证的开发工具包。它提供了完整的云计算服务接入能力，包括用户管理、卡密管理、在线验证等功能。

## 环境要求

- Python 3.6+
- Windows 操作系统
- SPCloud64_Py.dll 动态库文件

## 入门指南

### 安装

1. 确保 SPCloud64_Py.dll 文件在正确的目录中
2. 将 SDK 代码文件复制到您的项目中

### 基本使用流程

1. 创建云计算对象
2. 设置连接信息
3. 登录验证
4. 使用其他功能
5. 销毁对象

```python
import os
from spcloud import *

# 创建云计算对象
cloud = sp_cloud_create()

# 设置连接信息
sp_cloud_set_conninfo(cloud, 
    software_name="您的软件名称",
    ip="服务器IP",
    port=端口号,
    timeout=超时时间,
    pop_out=False
)

# 登录验证（以卡密登录为例）
result = sp_card_login(cloud, "您的卡密")
if result['ret']:
    print("登录成功")
else:
    print("登录失败:", sp_cloud_get_error_msg(result['code']))

# 使用完毕后销毁对象
sp_cloud_destroy(cloud)
```

## 核心功能

### 1. 卡密管理功能

#### 卡密登录
```python
result = sp_card_login(cloud, "卡密字符串")
```

#### 获取卡密信息
```python
# 获取卡密类型
result = sp_cloud_get_card_type(cloud)

# 获取过期时间
result = sp_cloud_get_expired_time_stamp(cloud)

# 获取卡密点数
result = sp_cloud_get_fyi(cloud)
```

### 2. 用户管理功能

#### 用户注册
```python
result = sp_cloud_user_register(cloud, 
    user="用户名",
    password="密码",
    super_pwd="超级密码",
    recharge_cards="充值卡密"
)
```

#### 用户登录
```python
result = sp_user_login(cloud, "用户名", "密码")
```

### 3. 在线验证功能

#### 心跳验证
```python
result = sp_cloud_beat(cloud)
```

#### 获取在线信息
```python
result = sp_cloud_get_online_count(cloud)
```

### 4. 机器码管理

#### 查询机器码绑定信息
```python
result = sp_cloud_query_pc_sign(cloud, "卡密")
```

#### 解绑机器码
```python
result = sp_cloud_remove_pc_sign(cloud, "卡密", "机器码", unbind_ip=0)
```

## 错误处理

SDK 所有接口都会返回包含以下字段的字典：
- ret: 布尔值，表示操作是否成功
- code: 错误码
- 其他返回值（根据具体接口不同）

获取错误信息：
```python
error_msg = sp_cloud_get_error_msg(error_code)
```

### 常见错误码

- -1: 参数错误
- -2: 内存申请失败
- -3: 网络错误
- -4: 服务器返回数据错误
- -5: 登录失败

## 示例代码

### 完整登录流程示例

```python
from spcloud import *

def login_example():
    # 1. 创建云计算对象
    cloud = sp_cloud_create()
    
    try:
        # 2. 设置连接信息
        sp_cloud_set_conninfo(
            cloud=cloud,
            software_name="测试软件",
            ip="127.0.0.1",
            port=8888,
            timeout=5000,
            pop_out=False
        )
        
        # 3. 登录验证
        result = sp_card_login(cloud, "测试卡密")
        if not result['ret']:
            print("登录失败:", sp_cloud_get_error_msg(result['code']))
            return
            
        print("登录成功")
        
        # 4. 获取卡密信息
        card_info = sp_cloud_get_card_type(cloud)
        expired_info = sp_cloud_get_expired_time_stamp(cloud)
        
        print("卡密类型:", card_info['card_type'])
        print("过期时间:", expired_info['expired_time_stamp'])
        
    finally:
        # 5. 销毁对象
        sp_cloud_destroy(cloud)

if __name__ == '__main__':
    login_example()
```

### 用户注册和充值示例

```python
def user_management_example():
    cloud = sp_cloud_create()
    
    try:
        # 设置连接信息
        sp_cloud_set_conninfo(cloud, "测试软件", "127.0.0.1", 8888, 5000, False)
        
        # 注册新用户
        reg_result = sp_cloud_user_register(
            cloud,
            user="testuser",
            password="testpass",
            super_pwd="superpass",
            recharge_cards="CARD123456"
        )
        
        if not reg_result['ret']:
            print("注册失败:", sp_cloud_get_error_msg(reg_result['code']))
            return
            
        # 用户充值
        recharge_result = sp_cloud_user_recharge(
            cloud,
            user="testuser",
            recharge_cards="RECHARGE123456"
        )
        
        if recharge_result['ret']:
            print("充值成功")
            print("新增点数:", recharge_result['info']['u64NewFYI'])
            
    finally:
        sp_cloud_destroy(cloud)
```

## 注意事项

1. 务必正确调用 sp_cloud_destroy() 释放资源
2. 网络操作可能需要异常处理
3. 建议在单独的线程中执行心跳验证
4. 敏感信息（如密码）建议加密存储
5. 注意处理所有返回值中的错误码

## 技术支持

如果您在使用过程中遇到问题，请检查：

1. DLL文件是否正确放置
2. 网络连接是否正常
3. 参数是否正确
4. 错误码含义

如仍有问题，请联系技术支持。

---
是否需要我为特定功能提供更详细的说明？或者您有其他任何问题吗？