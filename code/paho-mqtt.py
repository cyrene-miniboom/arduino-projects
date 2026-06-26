import serial
import time
from paho.mqtt import client as mqtt_client

# ---------- MQTT 回调函数 ----------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("连接成功！")
        client.subscribe("testtopic/py")   # 订阅主题（可选）
    else:
        print(f"连接失败，错误码：{rc}")

# ---------- MQTT 客户端配置 ----------
broker = '0688181a.ala.cn-hangzhou.emqxsl.cn'
port = 8084
keepalive = 60
topic = "testtopic/py"

client = mqtt_client.Client(transport="websockets")
client.tls_set(ca_certs="D:/edgedownload/emqxsl-ca.crt")   # 请确认证书路径
client.username_pw_set(username="xxx", password="xxxxxx")
client.on_connect = on_connect

# 连接到 MQTT 服务器
client.connect(broker, port, keepalive)
client.loop_start()   # 启动网络循环（非阻塞线程）

# ---------- 串口读取与数据发布 ----------
try:
    # 创建串口对象（根据实际设备修改 COM 口和波特率）
    ser = serial.Serial(port='COM6', baudrate=9600, timeout=1)
    print(f"成功连接到 {ser.name}")

    # 等待 Arduino 初始化
    time.sleep(2)
    print("开始接收距离数据...")
    print("按 Ctrl+C 停止")

    while True:
        # 读取一行数据
        line = ser.readline().decode('utf-8').rstrip()
        # 检查数据格式是否有效
        if line.startswith("Distance: ") and " cm" in line:
            # 提取距离数值
            dis_str = line.split(":")[1].split(" cm")[0].strip()
            distance = float(dis_str)
            # 打印并发布
            print(f"当前距离: {distance:.2f} cm")
            msg = f"Distance:{distance:.2f} cm"
            client.publish(topic, msg)
        # 小延时避免 CPU 占用过高
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"串口连接错误: {e}")
except KeyboardInterrupt:
    print("\n程序已停止")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    # 确保关闭串口和 MQTT 连接
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("串口已关闭")
    client.loop_stop()
    client.disconnect()
    print("MQTT 连接已断开")
