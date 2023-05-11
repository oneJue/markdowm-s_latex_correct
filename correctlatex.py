import time
import sys
import os
import re
import keyboard



def transform(s: str):
    s = s.replace(" ", "")  # 删除空格
    s = s.replace("\u200b", "")
    # 替换双斜杠
    obj = re.compile("\\\\\\\\")
    obj1 = re.compile("\\\\")
    obj2 = re.compile("###")

    tmp1 = re.sub(obj, "###", s)
    tmp2 = re.sub(obj1, "", tmp1)
    s_new = re.sub(obj2, "\\\\", tmp2)

    length = len(s_new)
    start = 0
    end = length
    for chr in s_new:
        if '\u4e00' <= chr <= '\u9fff':
            start += 1
        else:
            break

    for chr in reversed(list(s_new)):
        if '\u4e00' <= chr <= '\u9fff':
            end -= 1
        else:
            break

    maxlen = 0
    for samelen in range(1, end - start):
        front = s_new[start:start + samelen]
        tail = s_new[end - samelen:end]
        if (end - start) - 2 * samelen < samelen:
            break
        if front == tail:
            maxlen = samelen

    result = []
    result.append(s_new[:start])
    result.append("$")
    result.append(s_new[start + maxlen:end - maxlen])
    result.append("$")
    result.append(s_new[end:])

    return "".join(result)

sys.path.append(os.path.abspath("SO_site-packages"))
import pyperclip  # 引入模块


recent_value = ""  # 初始化（应该也可以没有这一行，感觉意义不大。但是对recent_value的初始化是必须的）
def correct(recent_value):
    changed = out = re.sub(r"\s{2,}", " ", recent_value)+"111"  # 将文本的换行符去掉，变成一个空格
    pyperclip.copy(changed)  # 将修改后的文本写入系统剪切板中
    print("\n Value changed: %s" % str(changed))  # 输出已经去除换行符的文本
    return changed

while True:

    try:
        keyboard.wait("ctrl + shift + z")

        keyboard.press_and_release("ctrl+c")
        time.sleep(0.200)
        recent_value = pyperclip.paste()  # 读取剪切板复制的内容
        time.sleep(0.200)
        if recent_value == "esc":
            break

        print(recent_value)
        recent_value = transform(recent_value)
        pyperclip.copy(recent_value)
        time.sleep(0.200)
        keyboard.press_and_release("ctrl+v")

    except KeyboardInterrupt:  #
        break

