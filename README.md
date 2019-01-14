# IoTWeb

大四终于接触到直接跟物联网有关的实验啦！所以给这个项目起了 叫 ***IoTWeb***，即基于车联网的远程控制 web 项目。本课程设计用 Arduino 以及相关配件模拟车门开关，用树莓派相机作为远程监控，并且开发了远程操控树莓派拍摄照片，并将照片保存在本地。相应的技术有：python3、Flask Web 服务器、HTML5、Jinja、css美化、FRP 内网穿透、SimpleCV，并利搬瓦工服务器和阿里域名实现了外网访问树莓派。

## 实验准备

| 器材           | 型号                                 |
| -------------- | ------------------------------------ |
| 树莓派         | Raspberry Pi 1                       |
| 树莓派相机     | Raspberry Pi Camera Rev 1.3          |
| Ardunio        | UNO R3                               |
| Ardunio 拓展版 | IO Expansion Shield for Arduino V7.1 |
| 蜂鸣器         | (SKU:DFR0032)数字蜂鸣器模块          |
| 数字大按钮     | (SKU:DFR0029)数字大按钮模块 V2       |
| LED x 2        | 数字LED发光模块 (SKU: DFR0021)       |
| 网线           |                                      |
| SD卡           | 金士顿16G                            |

## 实验部署

所需要安装好python3、Ardunio IDE(可以在自己电脑上安装进行 Ardunio 程序烧写)

## 遇到的问题

- 脚本启动缓慢

  原因：由于课设用到的树莓派为1代，内存等各个方面性能不足，项目 import 的包越多，python 脚本启动越慢。

- xshell 无法远程连接树莓派

  原因：未开启 ssh 服务

  解决方案：进入到树莓派界面点击左上角的树莓派，找到【设置】-【远程设置】，开启 ssh 和 VNC connect

- 每次登陆树莓派，发现树莓派的 IP 地址可能会改变，如何设置静态 IP 呢？

  原因：树莓派网络默认开启 DHCP 模式

  解决方案：树莓派采用的是 Debian 操作系统，需要修改 `/etc/dhcpcd.conf`里添加：

  ```bash
  vim /etc/dhcpcd.conf
  # 树莓派自带的vi很不好用，通过sudo apt-get install vim
  
  # 指定接口
  interface eth0
  # 固定IP，别忘了子网掩码
  static ip_address=192.168.137.238/24
  # 设置网关
  static routers=192.168.137.1
  # 手动自定义DNS服务器
  static domain_name_servers=114.114.114.114
  
  sudo reboot # 修改完重启生效（debian好像没有systemctl restart network命令）
  # 或者采用以下命令
  sudo ifconfig eth0 down
  sudo ifconfig eth0 up
  ```

- `ping www.baidu.com`域名解析暂时失败

  1. 若连接的是手机热点（win 10系统），右键右下角WiFi【网络和Internet设置】 - 【网络连接】，右键WLAN属性 - 共享，将 Internet 连接共享以下的两个打勾，然后再 ping 百度。

     ![1547473056271](C:\Users\59813\AppData\Roaming\Typora\typora-user-images\1547473056271.png)

  2. 修改回 DHCP 模式，reboot 重启获取新的网络 IP

## 参考文档

[Arduino 官网](https://www.dfrobot.com/)

购买相应器材→[DF 创客社区](http://mc.dfrobot.com.cn/portal.php)

[Linux 开源社区|树莓派](https://linux.cn/tech/raspberrypi/)

[Arduino 配件查询](http://wiki.dfrobot.com.cn/index.php?title=首页)    

## 

  