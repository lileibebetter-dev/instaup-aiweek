#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
云秒搭AI周报 - 网站构建脚本
"""

import os
import sys

# 添加scripts目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# 导入构建函数
from build_simple import build_simple_edgeone_site

if __name__ == "__main__":
    print("🚀 开始构建云秒搭AI周报网站...")
    build_simple_edgeone_site()
    print("✅ 网站构建完成！")
