from ctypes import *
import ctypes
import os


__all__ = ['Sprotect']


class TagPCSignInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ("u64BindTS", c_ulonglong),  # 绑定时间戳
        ("szWinVer", c_char_p),      # 操作系统版本
        ("szRemark", c_char_p),      # 备注
        ("szComputerName", c_char_p),# 计算机名
        ("szPCSign", c_char_p),      # 机器码
        ("u64LastLoginTS", c_ulonglong),  # 最后登录时间
        ("Reserved", c_void_p * 20)  # 保留字段
    ]

class TagPCSignInfoHead(Structure):
    _pack_ = 1
    _fields_ = [
        ("u32Count", c_uint),                      # 信息数量
        ("Info", POINTER(TagPCSignInfo)),         # 指向 TagPCSignInfo 数组的指针
        ("u32BindIP", c_uint),                     # 是否绑定IP
        ("u32RestCount", c_uint),                  # 周期内剩余次数
        ("u64RefreshCountdownSeconds", c_ulonglong),  # 更新倒计时的秒数
        ("u32Limit", c_uint),                      # 限制解绑
        ("Reserved", c_void_p * 19)      # 保留字段
    ]

class TagOnlineInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ("u32CID", c_uint),
        ("szComputerName", c_char_p),
        ("szWinVer", c_char_p),
        ("u64CloudInitTS", c_ulonglong),
        ("Reserved", c_void_p * 20)
    ]

class TagOnlineInfoHead(Structure):
    _pack_ = 1
    _fields_ = [
        ("u32Count", c_uint),
        ("Info", POINTER(TagOnlineInfo)),
        ("Reserved", c_void_p * 20)
    ]

class TagUserRechargedInfo(Structure):
    _pack_ = 1  # 设置为 1 字节对齐
    _fields_ = [
        ("u64OldExpiredTimeStamp", c_ulonglong),  # 旧的过期时间戳
        ("u64NewExpiredTimeStamp", c_ulonglong),  # 新的过期时间戳
        ("u64OldFYI", c_ulonglong),                # 旧的点数
        ("u64NewFYI", c_ulonglong),                # 新的点数
        ("u32RechargeCount", c_uint),              # 本次充值的卡密个数
        ("Reserved", c_void_p * 80)      # 保留字段
    ]

class TagBasicInfo(Structure):
    _fields_ = [
        ("ForbidTrial", c_uint),
        ("ForbidLogin", c_uint),
        ("ForbidRegister", c_uint),
        ("ForbidRecharge", c_uint),
        ("ForbidCloudGetCountinfo", c_uint),
        ("Reserved", c_uint * 15)
    ]


class Sprotect:
    def __init__(self, dll_path: str = 'SPCloud64_Py.dll'):
        try:
            self.sp = ctypes.WinDLL(dll_path)
        except:
            path = os.path.join(os.path.dirname(__file__), dll_path)
            self.sp = ctypes.WinDLL(path)

    def sp_cloud_create(self):
        """
        描述: 云计算, 创建一个云计算对象 , 后续cloud都是这个对象
        :return:
        """
        self.sp.SP_Cloud_Create.restype = c_void_p
        self.CID = self.sp.SP_Cloud_Create()
        return self.CID

    def sp_card_login(self, card: str):
        """
        /* 描述: SP云计算_登录; 不可与SP_CloudInit函数一起使用! */
        :param cloud:
        :param card: 卡密
        :return: bool
        """
        error_code = c_int()
        self.sp.SP_CloudLogin.argtypes = [c_void_p, c_char_p, POINTER(c_int)]
        self.sp.SP_CloudLogin.restype = c_bool
        card = bytes(card, 'gbk')
        ret = self.sp.SP_CloudLogin(self.CID, card, byref(error_code))
        return {'ret': ret, 'code': error_code.value}

    def sp_user_login(self, user: str, password: str):
        """
        /* 描述: SP云计算_登录; 不可与SP_CloudInit函数一起使用! */
        :param cloud:
        :param user: 用户名
        :param password: 密码
        :return: bool
        """
        error_code = c_int()
        self.sp.SP_CloudUserLogin.argtypes = [c_void_p, c_char_p, c_char_p, POINTER(c_int)]
        self.sp.SP_CloudUserLogin.restype = c_bool
        user = bytes(user, 'gbk')
        password = bytes(password, 'gbk')
        ret = self.sp.SP_CloudUserLogin(self.CID, user, password, byref(error_code))
        return {'ret': ret, 'code': error_code.value}

    def sp_cloud_set_conninfo(self, software_name: str, ip: str, port: int, timeout: int,
                              localversion: int, pop_out: c_bool):
        """
        /* 描述: SP云计算_设置连接信息; 不可与SP_CloudInit函数一起使用! */
        :param localversion:
        :param cloud:
        :param software_name: 软件名称
        :param ip: IP地址
        :param port: 端口
        :param timeout: 超时时间
        :param pop_out: 是否弹窗
        :return: bool
        """
        software_name = bytes(software_name, 'gbk')
        self.sp.SP_CloudSetConnInfo.argtypes = [c_void_p, c_char_p, c_char_p, c_int, c_int, c_int, c_bool]
        ip = bytes(ip, 'gbk')
        self.sp.SP_CloudSetConnInfo(self.CID, software_name, ip, port, timeout, localversion, pop_out)
        return None