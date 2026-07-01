import socket
import urllib.request
import urllib.parse
import os
import http.server
import socketserver

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def main():
    ip = get_host_ip()
    port = 8000
    url = f"http://{ip}:{port}/网页演示程序/index.html"
    print(f"==================================================")
    print(f" 局域网服务已就绪！")
    print(f" iPad 访问链接：{url}")
    print(f"==================================================")
    
    # 1. 自动获取二维码图片并保存
    qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(url)}"
    qr_path = "/Users/gzm/Downloads/手机剪辑课程/scripts/ipad_scan_qr.png"
    
    try:
        print("正在为您生成 iPad 扫码极速播放二维码...")
        # 设置超时
        urllib.request.urlretrieve(qr_api, qr_path)
        print(f"二维码图片已保存至：{qr_path}")
        # 在 Mac 上自动弹出展示二维码
        os.system(f'open "{qr_path}"')
        print(" 已在 Mac 屏幕上弹出二维码图片，请直接用 iPad 相机扫码即可打开网页放映！")
    except Exception as e:
        print(f"二维码生成失败 ({e})，若无网络您可以直接在 iPad Safari 中手动输入以下链接访问：")
        print(url)

    # 2. 开启静态网页服务器
    os.chdir("/Users/gzm/Downloads/手机剪辑课程")
    Handler = http.server.SimpleHTTPRequestHandler
    
    # 解决端口占用
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f" 本地静态网页服务器正在运行 (端口 {port})... 按 Ctrl+C 可关闭服务")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n 服务已主动停止。")

if __name__ == '__main__':
    main()
