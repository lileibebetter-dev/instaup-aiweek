#!/bin/bash

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    云秒搭AI周报 - 文章管理后台"
echo "========================================"
echo -e "${NC}"

echo -e "\n${YELLOW}[1/3] 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到Python3，请先安装Python 3.7+${NC}"
    echo "macOS: brew install python3"
    echo "Ubuntu: sudo apt install python3 python3-pip"
    exit 1
fi
echo -e "${GREEN}✅ Python环境正常${NC}"

echo -e "\n${YELLOW}[2/3] 安装依赖包...${NC}"
pip3 install flask flask-cors requests beautifulsoup4 lxml > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 依赖包检查完成${NC}"
else
    echo -e "${YELLOW}⚠️  依赖包安装可能有问题，但继续尝试启动...${NC}"
fi

echo -e "\n${YELLOW}[3/3] 启动服务器...${NC}"
echo ""
echo -e "${BLUE}🚀 正在启动文章管理后台...${NC}"
echo -e "${BLUE}📝 管理界面: http://localhost:8080${NC}"
echo -e "${BLUE}🔧 按 Ctrl+C 停止服务器${NC}"
echo ""
echo -e "${YELLOW}⏳ 请稍候，正在启动服务器...${NC}"
echo ""

# 启动Flask服务器
python3 server.py

echo ""
echo -e "${GREEN}👋 服务器已停止${NC}"
