from flask import Flask, jsonify, render_template, request
import requests
import base64
import re
import zipfile
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import json
import os


def readPDF(pdfFile):
    pdfFile = open(pdfFile, "rb")
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    pdfFile.close()
    return content


def getcode(text):
    code = re.findall(r"准考证号：(\d+)", text)
    name = re.findall(r"姓名：(.+)\n", text)
    if code:
        code = code[0]
    else:
        code = None
    if name:
        name = name[0]
    else:
        name = None
    if code is not None:
        return {"code": code, "name": name}
    else:
        return None


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():
        file = (zip_file.extract(names, "./data/"))
    zip_file.close()
    # os.remove(file_name) # 删除文件，本地不进行保存
    return file


def down(sid):
    sid = sid.split('"')[0]
    # print("sid"+ sid)
    r = requests.get("http://cet-bm.neea.edu.cn/Home/DownTestTicket?SID=" + sid)
    data = r.content
    with open("data/" + sid + ".zip", "wb") as f:
        f.write(data)
    return "data/" + sid + ".zip"


def _query(province, code, name, number, cookie):
    jar = requests.cookies.RequestsCookieJar()
    cookie = cookie.split("分")
    jar.set('ASP.NET_SessionId', cookie[0], domain='cet-bm.neea.edu.cn', path='/')
    jar.set('BIGipServercet_pool', cookie[1], domain='cet-bm.neea.edu.cn', path='/')
    param = dict(provinceCode=province, IDTypeCode=1, IDNumber=number, Name=name, verificationCode=code)
    r = requests.post("http://cet-bm.neea.edu.cn/Home/ToQuickPrintTestTicket", param, cookies=jar)
    text = r.text
    data = None
    try:
        jsonld = json.loads(text)
        if jsonld.get("ExceuteResultType") == 1:
            sid = re.findall('SID":"(.+)","SubjectName"', jsonld.get("Message"))
            if sid:
                file = down(sid[0])
                file = un_zip(file)
                text = readPDF(file)
                # os.remove(file) # 删除文件，不进行留存
                code = getcode(text)
                if code.get("code"):
                    data = code
                    ExceuteResultType = 1
                    Message = "查询成功"
                else:
                    Message = "查询失败"
                    ExceuteResultType = -1
        else:
            return jsonld
    except Exception as e:
        print(e)
        ExceuteResultType = -1
        Message = "系统错误"
    return dict(ExceuteResultType=ExceuteResultType, Message=Message, data=data)
def code():
    """
    获取验证码,返回cookie，和 验证码的b64
    :return:
    """
    r = requests.get("http://cet-bm.neea.edu.cn/Home/VerifyCodeImg")
    pic = r.content
    with open('Ver_Img.png', 'wb') as f:
        f.write(pic)
    Ver_code = input("请输入验证码：")
    print((r.cookies))
    cookies = r.cookies['ASP.NET_SessionId'] + "分" + r.cookies['BIGipServercet_pool']
    # content = r.content
    # img = 'data:image/jpeg;base64,' + base64.b64encode(content).decode()
    return cookies, Ver_code
# print(code())

province = "37"
cookie, code = code()
name = "马长金"
number = "37152220001104783x"
print(_query(province, code, name, number, cookie))