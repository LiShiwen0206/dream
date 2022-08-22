import pyautogui
import pyperclip
import time


def get_msg():
    """想发的消息，每条消息空格分开"""
    contents = "晚上你吃啥 啥，不知道 那听我安排吧 晚上回来先歇会 可以先吃个火龙果，我已经拿出来了 等会会有外卖给你打电话 " \
               "拿到外卖再开始做饭都不晚 什么外卖你别问 这次让我卖个关子可行"
    return contents.split(" ")


def send(msg):
    # 复制需要发送的内容到粘贴板
    pyperclip.copy(msg)
    # 模拟键盘 ctrl + v 粘贴内容
    pyautogui.hotkey('ctrl', 'v')
    # 发送消息
    pyautogui.press('enter')


def send_msg(friend):
    # Ctrl + alt + w 打开微信
    pyautogui.hotkey('ctrl', 'alt', 'w')
    # 搜索好友
    pyautogui.hotkey('ctrl', 'f')
    # 复制好友昵称到粘贴板
    pyperclip.copy(friend)
    # 模拟键盘 ctrl + v 粘贴
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    # 回车进入好友消息界面
    pyautogui.press('enter')
    # 一条一条发送消息
    for msg in get_msg():
        send(msg)
        # 每条消息间隔 2 秒
        time.sleep(2)


if __name__ == '__main__':
    friend_name = "WaiSaa"
    send_msg(friend_name)