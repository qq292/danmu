chcp 65001
@echo off
echo ------------------------------------------------------------------------------------------------------------------    
echo 支持的平台:
echo "# 虎牙直播：https://www.huya.com/11352915"
echo "# 斗鱼直播：https://www.douyu.com/85894"
echo "# B站直播：https://live.bilibili.com/70155"
echo "# 快手直播：https://live.kuaishou.com/u/jjworld126"
echo "# 火猫直播："
echo "# 企鹅电竞：https://egame.qq.com/383204988"
echo "# 花椒直播：https://www.huajiao.com/l/303344861?qd=hu"
echo "# 映客直播：https://www.inke.cn/liveroom/index.html?uid=87493223&id=1593906372018299"
echo "# CC直播：https://cc.163.com/363936598/"
echo "# 酷狗直播：https://fanxing.kugou.com/1676290"
echo "# 战旗直播："
echo "# 龙珠直播：http://star.longzhu.com/wsde135864219"

echo "# PPS奇秀直播：https://x.pps.tv/room/208337"
echo "# 搜狐千帆直播：https://qf.56.com/520208a"
echo "# 来疯直播：https://v.laifeng.com/656428"
echo "# LOOK直播：https://look.163.com/live?id=196257915"
echo "# AcFun直播：https://live.acfun.cn/live/23682490"
echo "# 艺气山直播：http://www.173.com/96"
echo ------------------------------------------------------------------------------------------------------------------   
set /p url=输入直播间url:
set py=%cd%\venv\Scripts\python
%py% %cd%\BulletScreen\Dome\Test.py  %url%

pause