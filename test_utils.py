# -*- coding: utf-8 -*-
"""Photoshop Python API 测试工具模块"""

import os
import sys
import codecs

# 设置UTF-8编码解决中文显示问题
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

def safe_print(text):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def get_test_save_dir():
    """获取测试保存目录"""
    save_dir = os.path.join(os.path.dirname(__file__), "tested_cases")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir