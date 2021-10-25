# -*- coding:utf-8 -*-
import os


# 定义加密字典
encrypt_original_dict = {0: "皮皮", 1: "皮卡", 2: "皮丘", 3: "卡皮", 4: "卡卡", 5: "丘皮", 6: "丘卡"}
encrypt_extend_dict = {7: "丘丘", 8: "皮皮", 9: "皮卡", 10: "皮丘", 11: "卡皮", 12: "卡卡", 13: "卡丘", 14: "丘皮", 15: "丘卡"}

encrypt_whitelist = list("`1234567890=[]\\;',./?><\":|}{+_*&^%$#@!！@#￥%……&*（）——+：”《》？“，。、；‘【】、=· \n\r")
encryt_whitelist_sentences = ["皮卡丘"] + list(encrypt_extend_dict.values()) + list(encrypt_original_dict.values())

# 定义解密字典
decrypt_original_dict = dict(zip(list(encrypt_original_dict.values()), list(encrypt_original_dict.keys())))
decrypt_extend_dict = dict(zip(list(encrypt_extend_dict.values()), list(encrypt_extend_dict.keys())))


def beautift_text(text):
    """将文本美化 text长度必须为偶数"""
    if len(text) % 2 != 0:
        raise BaseException("text must be even!")  # 必须是偶数

    sub = 0  # 用于标记文本光标位置（即文本处理位置）

    while sub <= len(text) - 1:
        if text[sub:sub + 2] == text[sub + 2:sub + 4]:  # 是否有重复字段
            text = text[:sub + 2] + "~" + text[sub + 4:]  # 替换成 “~”
            sub += 3  # 由于被替换成一个字符则是+3而不是+4
            continue
        elif text[sub + 1:sub + 2] * 2 == text[sub + 2:sub + 4]:  # 是否有单字重复字段
            text = text[:sub + 2] + "-" + text[sub + 4:]  # 替换成 “-”
            sub += 3  # 由于被替换成一个字符则是+3而不是+4
            continue
        else:
            sub += 2  # 什么都没有就+2
    return text


def encode_text(text):
    """把一段普通文本加密成“皮卡丘语”"""
    # 白名单句子
    if text in encryt_whitelist_sentences:
        return text
    # 定义加密前需要的变量
    finally_text = ""
    for sub in range(len(text)):
        # 白名单字符排除
        if text[sub] in encrypt_whitelist:
            finally_text = finally_text + text[sub]
            continue
        # 特别字符排除
        if text[sub] in ("(", ")", "-", "~"):
            finally_text = finally_text + "丘丘" + text[sub] + "丘丘"
            continue
        # 转化十六进制前定义变量
        one_way_encode_text = ""  # 此次循环加密的结果
        quotient = ord(text[sub])  # 取出文本在字符(Unicode)中的编号
        while quotient != 0:  # 用于标记十六进制单个结果 商数不为0 即十六进制尚未完全转化
            remainder = quotient % 16  # 取余 此余数会在 0 <= remainder <= 15 范围内且为整数
            quotient = quotient // 16  # 取整 为下一次转化做准备 取整取余顺序不可以调换！！！
            # one_way_encode_text 是倒着添加，因为最先转化出来的其实是最后的位数
            if remainder <= 6:
                one_way_encode_text = encrypt_original_dict[remainder] + one_way_encode_text
            elif remainder > 6:
                one_way_encode_text = "(" + encrypt_extend_dict[remainder] + ")" + one_way_encode_text
            else:
                # 出现此外清空 即为程序出错
                raise BaseException(
                    "An error occurred! There are extra digits in hexadecimal conversion!")  # 出现错误！转化十六进制时出现额外的进制位数！
        finally_text = finally_text + one_way_encode_text + "卡丘"  # 追加到最终结果

    # 输出美化处理 第一步：去除连续括号
    finally_text = finally_text.replace(")(", "")
    # 输出美化处理 第二、三步：连续字段替换为 “~”与“-”
    sub = 0  # 用于标记文本光标位置（即文本处理位置）
    temp_text = ""  # 临时文本用于存储读入的文本
    return_text = ""  # 用于存储返回文本
    while sub <= len(finally_text) - 1:
        if finally_text[sub] in ("皮", "卡", "丘"):
            temp_text = temp_text + finally_text[sub]  # 添加数据
            sub += 1
            continue
        else:
            return_text = return_text + beautift_text(temp_text) + finally_text[sub]  # 找到额外数据
            temp_text = ""  # 清空
            sub += 1
    return_text = return_text + beautift_text(temp_text)
    return return_text


def hexadecimal2text(List):
    """转化列表内容为文本"""
    List = List[::-1]  # 列表翻转
    total = 0  # 字符编码结果
    for i in range(len(List)):
        total += 16 ** i * List[i]
    return chr(total)


def decode_text(text):
    # 白名单文本不译
    if text in encryt_whitelist_sentences:
        return text
    stay_text = text  # 保存原字段
    sub = 0  # 用于标记文本光标位置（即文本处理位置）
    return_text = ""  # 最终结果
    temp_list = []  # 临时列表用于存储读入的数据
    extend_mode = False  # 括号拓展模式
    jump_mode = False  # 不译模式
    while sub <= len(text) - 1:
        if text[sub] not in ("皮", "卡", "丘", "(", ")", "-", "~"):
            return_text = return_text + text[sub]
            sub += 1
            continue
        if text[sub] == "~" and jump_mode == False:  # 发现省略符号
            text = text[:sub] + text[sub - 2:sub] + text[sub + 1:]
        elif text[sub] == "-" and jump_mode == False:  # 发现重复符号
            text = text[:sub] + text[sub - 1] * 2 + text[sub + 1:]
        if text[sub] == "(" and jump_mode == False:  # 发现左括号 开启拓展模式 读取拓展加密字典内容
            extend_mode = True
            sub += 1
        elif text[sub] == ")" and jump_mode == False:  # 发现右括号 关闭拓展模式 读取普通加密字典内容
            extend_mode = False
            sub += 1
        else:
            if sub + 2 > len(text):
                print("无法解密此语段：提供了一个错误的长度。位置出现在：第" + str(sub) + "位光标位置")
                print("解密原字段：\n" + stay_text)
                print("转化到出错的字段：\n" + text)
                return ""
            if text[sub:sub + 2] == "丘丘" and extend_mode == False:  # 发现不译符号
                jump_mode = jump_mode == False
                sub += 2
                continue
            if jump_mode:
                return_text = return_text + text[sub]
                sub += 1
                continue
            if text[sub:sub + 2] == "卡丘" and extend_mode == False:  # 终止符
                return_text = return_text + hexadecimal2text(temp_list)
                temp_list = []  # 清空
                sub += 2
                continue
            try:
                if extend_mode:
                    temp_list.append(decrypt_extend_dict[text[sub:sub + 2]])
                    sub += 2
                else:
                    temp_list.append(decrypt_original_dict[text[sub:sub + 2]])
                    sub += 2
            except KeyError:  # 没有字段
                print("无法解密此语段：提供了无法识别的内容。位置出现在：第" + str(sub) + "位光标位置")
                print("解密原字段：\n" + stay_text)
                print("转化到出错的字段：\n" + text)
                return ""

    return return_text


if __name__ == "__main__":
    print("欢迎您的下载与使用 “皮卡丘加密法” 此项目开源\n"
          "作者：我叫以赏 and Pikachu\n"
          "此项目参加青少年科技创新成果竞赛 2021-10-25\n")
    while True:
        try:
            function_id = input("输入数字标号打开对应功能：1.加密字符串  2.解密字符串  3.加密纯文本文件(utf-8)  4.解密纯文本文件(utf-8)  5.退出\n")
            if function_id == "1":
                User = input("输入你要加密的字符串：\n")
                print("加密结果：\n" + encode_text(User))
            elif function_id == "2":
                User = input("输入你要解密的字符串：\n")
                print("解密结果：\n" + decode_text(User))
            elif function_id == "3":
                User = input("输入要加密的文件路径：\n")
                User = User.replace("\"", "")

                with open(User, "r",encoding="utf-8") as f:
                    article = f.read()

                with open(os.path.splitext(User)[0] + "_encode" + os.path.splitext(User)[1], "w",encoding="utf-8") as f:
                    f.write(encode_text(article))

                print("加密文件保存至：" + os.path.splitext(User)[0] + "_encode" + os.path.splitext(User)[1])

            elif function_id == "4":
                User = input("输入要解密的文件路径：\n")
                User = User.replace("\"","")

                with open(User, "r",encoding="utf-8") as f:
                    article = f.read()

                with open(os.path.splitext(User)[0] + "_decode" + os.path.splitext(User)[1], "w",encoding="utf-8") as f:
                    f.write(decode_text(article))

                print("加密文件保存至：" + os.path.splitext(User)[0] + "_decode" + os.path.splitext(User)[1])

            elif function_id == "5":
                break
        except KeyboardInterrupt or EOFError:
            break
        except BaseException as error:
            print("程序在运行中出现错误，错误原因："+str(error))
            continue
