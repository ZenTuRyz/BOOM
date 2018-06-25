# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator
#==============================================================================#
botStart = time.time()

ZenTuRy = LINE()
#ZenTuRy = LINE("TOKEN KAMU")
#ZenTuRy = LINE("Email","Password")
ZenTuRy.log("Auth Token : " + str(ZenTuRy.authToken))
channelToken = ZenTuRy.getChannelResult()
ZenTuRy.log("Channel Token : " + str(channelToken))

ZenTuRyMID = ZenTuRy.profile.mid
ZenTuRyProfile = ZenTuRy.getProfile()
lineSettings = ZenTuRy.getSettings()
oepoll = OEPoll(ZenTuRy)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)


myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

myProfile["displayName"] = ZenTuRyProfile.displayName
myProfile["statusMessage"] = ZenTuRyProfile.statusMessage
myProfile["pictureStatus"] = ZenTuRyProfile.pictureStatus
#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
#    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    ZenTuRy.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        ZenTuRy.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
        
def helpmessage():
    helpMessage = " ⚠คำสั่งช่วยเหลือ⚠" + "\n" + \
                  "⭐help ➠ จะแสดงคำสั่ง" + "\n" + \
                  "⭐help2 ➠ จะแสดงคำสั่งชุดที่ 2" + "\n" + \
                  "⭐!help ➠ จะแสดงคำสั่ง OHM" + "\n" + \
                  "⭐รีบอท ➠ บอทจะเริมทำงานใหม่" + "\n" + \
		  " ⚠คำสั่งสถานะ⚠" + "\n" + \
                  "⭐sp ➠ จะแสดงความเร็วบอท" + "\n" + \
                  "⭐เช็คค่า ➠ จะแสดงคำสั่งตั่งค่า" + "\n" + \
                  "⭐บอท ➠ จะแสดงข้อมูลบอท" + "\n" + \
                  "⭐เทส ➠ เชคว่าบอทหลุดไหม" + "\n" + \
                  "⭐Me ➠ คทเรา" + "\n" + \
                  "⭐มิด ➠ MIdเรา" + "\n" + \
                  "⭐ชื่อ ➠ ชื่อเรา" + "\n" + \
                  "⭐ตัส ➠ ตัสเรา" + "\n" + \
                  "⭐รูป ➠ รูปเรา" + "\n" + \
                  "⭐รูปวิดีโอ ➠ รูปวิดีโอเรา" + "\n" + \
                  "⭐ปก ➠ ปกเรา" + "\n" + \
                  "⭐ออน ➠ เวลาทำงานบอท" + "\n" + \
		  " ⚠คำสั่งสถานะคนอื่น⚠" + "\n" + \
                  "⭐Me @ ➠ ลงคทคนอื่น" + "\n" + \
                  "⭐มิด @ ➠ ลงmidคนอื่น" + "\n" + \
                  "⭐ชื่อ @ ➠ ลงชื่อคนอื่น" + "\n" + \
                  "⭐ตัส @ ➠ ลงตัสคนอื่น" + "\n" + \
                  "⭐ดิส @ ➠ ลงดิสคนอื่น" + "\n" + \
                  "⭐ดิสวีดีโอ @ ➠ ลงดิสวีดีโอคนอื่น" + "\n" + \
                  "⭐cover @ ➠ ก็อปปกคนอื่น" + "\n" +\
                  "⭐clone @ ➠ ก็อปปกคนอื่นมาใส่" + "\n" +\
		  " ⚠คำสั่งใช้ในกลุ่ม⚠" + "\n" + \
                  "⭐Vk ➠ เตะแล้วดึงกลับ" + "\n" + \
                  "⭐Zt ➠ แทคชื่อร่องหน" + "\n" + \
                  "⭐Zc ➠ ดูmidคนใส่ร่องหน" "\n" + \
                  "⭐Zm ➠ ดู คท คนใส่ร่องหน" + "\n" + \
                  "⭐เตะ @ ➠ เตะออกจากลุ่ม" + "\n" + \
                  "⭐ข้อมูล @ ➠ ชื่อ ตัส mid คท ดิส" + "\n" + \
                  "⭐โทร ➠ เชิญโทร" + "\n" + \
                  "⭐Groupcreator ➠ ผู้สร้างกลุ่ม" + "\n" + \
                  "⭐Tagall ➠ แทคได้100คน" + "\n" + \
                  "⭐ชื่อกลุ่ม ➠ แสดงชื่อกลุ่ม" + "\n" + \
                  "⭐ไอดีกลุ่ม ➠ ไอดีห้อง" + "\n" + \
                  "⭐รูปกลุ่ม ➠ ปกกลุ่ม" + "\n" + \
                  "⭐กลุ่มทั้งหมด ➠ ดูรายชื่อกลุ่ม" + "\n" + \
                  "⭐ข้อมูลกลุ่ม ➠ ข้อมูลกลุ่ม" + "\n" + \
                  "⭐สมาชิก ➠ รายในห้อง" + "\n" + \
                  "⭐สมาชิก ➠ รายชื่อในห้อง" + "\n" + \
                  "⭐เปิดอ่าน ➠ ตั้งเวลา" + "\n" + \
                  "⭐ปิดอ่าน ➠ ปิดเวลา" + "\n" + \
                  "⭐อ่าน ➠ ดูคนอ่าน" + "\n" + \
                  "⭐ลบเวลา ➠ ลบเวลาคนอ่าน" + "\n" + \
                  "⭐ยกเลิก ➠ ยกเลิกค้างเชินกลุ่ม" + "\n" + \
                  "⭐ลิ้งกลุ่ม ➠ ขอลิ่งกลุ่ม" + "\n" + \
		  " ⚠คำสั่งอื่นๆ⚠" + "\n" + \
                  "⭐Love on/off ➠ เปิดเลียนแบบ" + "\n" + \
                  "⭐Love1 ➠ เพิ่มเลียนแบบ" + "\n" + \
                  "⭐Love2 ➠ ลบเลียนแบบ" + "\n" + \
                  "⭐พูด(ข้อความ) ➠ สั่งสิริพูด" + "\n" + \
                  "⭐name (ชื่อ) ➠ เปรี่ยนชื่อ" + "\n" + \
                  "Created by : ꧁OHM꧂ "
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   " ⚠คำสั่งชุดที่ 2⚠" + "\n" + \
                         "⭐Tag on/off ➠ ตอบกลับแทค" + "\n" + \
                         "⭐Tag2 on/off ➠ แทคส่งรูป" + "\n" + \
                         "⭐กลุ่ม on/off ➠ เข้ากลุ่มออโต้" + "\n" + \
                         "⭐อ่าน on/off ➠ อ่านออโต้" + "\n" + \
                         "⭐แชท on/off ➠ ออกแชทรวมออโต้" + "\n" + \
                         "⭐block on/off ➠ ออโต้บล็อค" + "\n" + \
                         "⭐สติกเกอร์ on/off ➠ แชร์ลิ้งสติกเกอร์" + "\n" + \
                         "⭐เปิดลิ้ง/ปิดลิ้ง ➠ เปิดปิดลิ่งกลุ่ม" + "\n" + \
                  "Created by : ꧁OHM꧂ "
    return helpTextToSpeech

def helpohm():
    helpOhm =   " ⚠ OHM HELP ⚠" + "\n" + \
                         "⭐!help ➠ แสดงคำสั่ง" + "\n" + \
                         "⭐!ohm ➠ ดูสถานะโอม" + "\n" + \
                         "⭐!groupcreator ➠ ผู้สร้างกลุ่ม" + "\n" + \
                         "⭐!online ➠ เวลาในการทำงาน" + "\n" + \
                         "⭐!sp ➠ ความเร็วบอท" + "\n" + \
                         "⭐!test ➠ เช็คว่าบอทหลุดไหม" + "\n" + \
                         "⭐!tagall ➠ แทคทุกคนในกลุ่ม" + "\n" + \
                  "Created by : ꧁OHM꧂ "
    return helpOhm
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                ZenTuRy.blockContact(op.param1)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = ZenTuRy.getGroup(op.param1)
            if settings["autoJoin"] == True:
                ZenTuRy.acceptGroupInvitation(op.param1)
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                ZenTuRy.leaveRoom(op.param1)
        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != ZenTuRy.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    ZenTuRy.sendMessage(to, str(helpMessage))
                    ZenTuRy.sendContact(to, "")
                    ZenTuRy.sendMessage(to, "")
                elif text.lower() == 'help2':
                    helpTextToSpeech = helptexttospeech()
                    ZenTuRy.sendMessage(to, str(helpTextToSpeech))
                elif text.lower() == 'help3':
                    helpOhm = helpohm()
                    ZenTuRy.sendMessage(to, str(helpOhm))
#==============================================================================#
                elif "ผส" == msg.text.lower():
                    ZenTuRy.sendMessage(to,"ผู้สร้างบอท\n ꧁OHM꧂  ")
                elif "เทส" == msg.text.lower():
                    ZenTuRy.sendMessage(to,"LOADING:▒...0%")
                    ZenTuRy.sendMessage(to,"█▒... 10.0%")
                    ZenTuRy.sendMessage(to,"██▒... 20.0%")
                    ZenTuRy.sendMessage(to,"███▒... 30.0%")
                    ZenTuRy.sendMessage(to,"████▒... 40.0%")
                    ZenTuRy.sendMessage(to,"█████▒... 50.0%")
                    ZenTuRy.sendMessage(to,"██████▒... 60.0%")
                    ZenTuRy.sendMessage(to,"███████▒... 70.0%")
                    ZenTuRy.sendMessage(to,"████████▒... 80.0%")
                    ZenTuRy.sendMessage(to,"█████████▒... 90.0%")
                    ZenTuRy.sendMessage(to,"███████████..100.0%")
                    ZenTuRy.sendMessage(to,"บอทยังอยู่ดีไม่หลุด 😂")
                elif "name " in msg.text.lower():
                    spl = re.split("name ",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                       prof = ZenTuRy.getProfile()
                       prof.displayName = spl[1]
                       ZenTuRy.updateProfile(prof)
                       ZenTuRy.sendMessage(to, "เปลี่ยนชื่อสำเร็จแล้ว(｀・ω・´)")
                elif "Vk:" in text:
                    midd = msg.text.replace("Vk:","")
                    ZenTuRy. kickoutFromGroup(msg.to,[midd])
                    ZenTuRy. findAndAddContactsByMid(midd)
                    ZenTuRy.inviteIntoGroup(msg.to,[midd])
                    ZenTuRy.cancelGroupInvitation(msg.to,[midd])
                elif "Vk " in msg.text:
                        vkick0 = msg.text.replace("Vk ","")
                        vkick1 = vkick0.rstrip()
                        vkick2 = vkick1.replace("@","")
                        vkick3 = vkick2.rstrip()
                        _name = vkick3
                        gs = ZenTuRy.getGroup(msg.to)
                        targets = []
                        for s in gs.members:
                            if _name in s.displayName:
                                targets.append(s.mid)
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    ZenTuRy.kickoutFromGroup(msg.to,[target])
                                    ZenTuRy.findAndAddContactsByMid(target)
                                    ZenTuRy. inviteIntoGroup(msg.to,[target])
                                except:
                                    pass
                elif "โทร" == msg.text.lower():
                    ZenTuRy.inviteIntoGroupCall(msg.to,[uid.mid for uid in ZenTuRy.getGroup(msg.to).members if uid.mid != ZenTuRy.getProfile().mid])
                    ZenTuRy.sendMessage(msg.to,"เชิญเข้าร่วมการโทรสำเร็จ(｀・ω・´)")	
                elif "ยกเลิก" == msg.text.lower():
                    if msg.toType == 2:
                        group = ZenTuRy.getGroup(msg.to)
                        gMembMids = [contact.mid for contact in group.invitee]
                        for _mid in gMembMids:
                            ZenTuRy.cancelGroupInvitation(msg.to,[_mid])
                        ZenTuRy.sendMessage(to,"ยกเลิกค้างเชิญเสร็จสิ้น(｀・ω・´)")
                elif "ลบรัน" == msg.text.lower():
                    gid = ZenTuRy.getGroupIdsInvited()
                    for i in gid:
                        ZenTuRy.rejectGroupInvitation(i)
                    if wait["lang"] == "JP":
                        ZenTuRy.sendText(msg.to,"ลบรันเสร็ดแล้ว(｀・ω・´)")
                    else:
                        ZenTuRy.sendText(msg.to,"拒绝了全部的邀请。")
                elif text.lower() == 'sp':
                    start = time.time()
                    ZenTuRy.sendMessage(to, "⚡ความเร็วบอทอยู่ที่⚡")
                    elapsed_time = time.time() - start
                    ZenTuRy.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'รีบอท':
                    ZenTuRy.sendMessage(to, "กำลังรีบอทกรุณารอสักครู่.....")
                    time.sleep(5)
                    ZenTuRy.sendMessage(to, "รีบอทเสร็จสิ้น..(｀・ω・´)")
                    ZenTuRy.sendMessage(to, "กรุณาให้บอทล็อกอินใหม่อีกครั้ง  (｀・ω・´)")
                    restartBot()
                elif text.lower() == 'ออน':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    ZenTuRy.sendMessage(to, "ระยะเวลาการทำงานของบอท\n{}".format(str(runtime)))
                elif text.lower() == 'บอท':
                    try:
                        arr = []
                        owner = "ude3230559bf63a55b9c28aa20ea194e3"
                        creator = ZenTuRy.getContact(owner)
                        contact = ZenTuRy.getContact(ZenTuRyMID)
                        grouplist = ZenTuRy.getGroupIdsJoined()
                        contactlist = ZenTuRy.getAllContactIds()
                        blockedlist = ZenTuRy.getBlockedContactIds()
                        ret_ = "╔══[ ข้อมูลไอดีคุณ ]"
                        ret_ += "\n╠ ชื่อ : {}".format(contact.displayName)
                        ret_ += "\n╠ กลุ่ม : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ เพื่อน : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ บล็อค : {}".format(str(len(blockedlist)))
                        ret_ += "\n╚══[ ข้อมูลไอดีคุณ ]"
                        ZenTuRy.sendMessage(to, str(ret_))
                    except Exception as e:
                        ZenTuRy.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'เช็คค่า':
                    try:
                        ret_ = "[ ข้อมูลการตั้งค่า ]"
                        if settings["autoAdd"] == True: ret_ += "\nบล็อคแอดออโต้✔"
                        else: ret_ += "\nบล็อคแอดออโต้✘"
                        if settings["autoJoin"] == True: ret_ += "\nเข้ากลุ่มออโต้ ✔"
                        else: ret_ += "\nเข้ากลุ่มออโต้ ✘"
                        if settings["autoLeave"] == True: ret_ += "\nออกแชทรวม ✔"
                        else: ret_ += "\nออกแชทรวม ✘"
                        if settings["autoRead"] == True: ret_ += "\nอ่านออโต้ ✔"
                        else: ret_ += "\nอ่านออโต้ ✘"
                        if settings["สติกเกอร์"] == True: ret_ += "\nเช็คสติกเกอร์ ✔ "
                        else: ret_ += "\nเช็คสติกเกอร์ ✘ "
                        if settings["detectMention"] == True: ret_ += "\nเปิดตอบกลับคนแทค ✔"
                        else: ret_ += "\nเปิดตอบกลับคนแทค ✘"
                        if settings["Tag2"] == True: ret_ += "\nเปิดแทคส่งรูป✔ "
                        else: ret_ += "\nเปิดแทคส่งรูป ✘ "
                        ZenTuRy.sendMessage(to, str(ret_))
                    except Exception as e:
                        ZenTuRy.sendMessage(msg.to, str(e))
                elif text.lower() == 'block on':
                    settings["autoAdd"] = True
                    ZenTuRy.sendMessage(to, "เปิดระบบออโต้บล็อคแล้ว(｀・ω・´)")
                elif text.lower() == 'block off':
                    settings["autoAdd"] = True
                    ZenTuRy.sendMessage(to, "ปิดระบบออโต้บล็อคแล้ว(｀・ω・´)")
                elif text.lower() == 'กลุ่ม on':
                    settings["AutoJoin"] = True
                    ZenTuRy.sendMessage(to, "เปิดระบบออโต้เข้ากลุ่มแล้ว(｀・ω・´)")
                elif text.lower() == 'กลุ่ม off':
                    settings["AutoJoin"] = True
                    ZenTuRy.sendMessage(to, "ปิดระบบเข้ากลุ่มออโต้แล้ว(｀・ω・´)")
                elif text.lower() == 'แชท on':
                    settings["autoLeave"] = True
                    ZenTuRy.sendMessage(to, "เปิดระบบออกแชทรวมแล้ว(｀・ω・´)")
                elif text.lower() == 'แชท off':
                    settings["autoLeave"] = True
                    ZenTuRy.sendMessage(to, "ปิดระบบออกแชทรวมแล้ว(｀・ω・´)")
                elif text.lower() == 'อ่าน on':
                    settings["AutoRead"] = True
                    ZenTuRy.sendMessage(to, "เปิดระบบอ่านออโต้แล้ว(｀・ω・´)")
                elif text.lower() == 'อ่าน off':
                    settings["AutoRead"] = True
                    ZenTuRy.sendMessage(to, "ปิดระบบอ่านออโต้แล้ว(｀・ω・´)")
                elif text.lower() == 'สติกเกอร์ on':
                    settings["สติกเกอร์"] = True
                    ZenTuRy.sendMessage(to, "เปิดระบบแชร์ลิ้งสต๊กเกอร์แล้ว(｀・ω・´)")
                elif text.lower() == 'สติกเกอร์ off':
                    settings["สติกเกอร์"] = True
                    ZenTuRy.sendMessage(to, "ปิดระบบแชร์ลิ้งสติกเกอร์แล้ว(｀・ω・´)")
                elif msg.text in ["Autotag on","Tag on","My respon on","Respon:on"]:
                    settings["detectMention"] = True
                    ZenTuRy.sendMessage(to, "เปิดแทคเรียบร้อย(｀・ω・´)")
                elif msg.text in ["Autotag off","Tag off","My respon off","Respon:off"]:
                    settings["detectMention"] = True
                    ZenTuRy.sendMessage(to, "ปิดแทคเรียบร้อยแล่ว(｀・ω・´)")
                elif text.lower() == 'tag2 on':
                    settings['Tag2'] = True
                    ZenTuRy.sendMessage(msg.to,"เปิดแทครูปภาพแล้ว(｀・ω・´)")
                elif text.lower() == 'tag2 off':
                    settings['Tag2'] = True
                    ZenTuRy.sendMessage(msg.to,"ปิดแทครูปภาพแล้ว(｀・ω・´)")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    ZenTuRy.sendMessage(to, "Kirim Contact Yang Mau Di Copy")
#==============================================================================#
                elif text.lower() == 'zt':
                    gs = ZenTuRy.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        ZenTuRy.sendMessage(to, "🤔แน๊ะไม่มีคนใส่ร่องหนในกลุ่มนี้😂")
                    else:
                        mc = ""
                        for target in targets:
                            mc += sendMessageWithMention(to,target) + "\n"
                        ZenTuRy.sendMessage(to, mc)
                elif text.lower() == 'zm':
                    gs = ZenTuRy.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        ZenTuRy.sendMessage(to, "🤗ไม่มีmidคนใส่ร่องหน🤗")
                    else:
                        mc = ""
                        for mi_d in lists:
                            mc += "->" + mi_d + "\n"
                        ZenTuRy.sendMessage(to,mc)
                elif text.lower() == 'zc':
                    gs = ZenTuRy.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        ZenTuRy.sendMessage(to, "🤔แน๊ะไม่มีคนใส่ร่องหนในกลุ่มนี้😂")
                    else:
                        for ls in lists:
                            contact = ZenTuRy.getContact(ls)
                            mi_d = contact.mid
                            ZenTuRy.sendContact(to, mi_d)
                elif "Mc " in msg.text:
                    mmid = msg.text.replace("Mc ","")
                    ZenTuRy.sendContact(to, mmid)
                elif text.lower() == 'me':
                    ZenTuRy.sendContact(to, ZenTuRyMID)
                    sendMessageWithMention(to, ZenTuRyMID)
                elif text.lower() == 'มิด':
                    ZenTuRy.sendMessage(msg.to,">" +  ZenTuRyMID)
                    sendMessageWithMention(to, ZenTuRyMID)
                elif text.lower() == 'ชื่อ':
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    ZenTuRy.sendMessage(msg.to,">" + me.displayName)
                    sendMessageWithMention(to, ZenTuRyMID)
                elif text.lower() == 'ตัส':
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    ZenTuRy.sendMessage(msg.to,">" + me.statusMessage)
                    sendMessageWithMention(to, ZenTuRyMID)
                elif text.lower() == 'รูป':
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    ZenTuRy.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                    sendMessageWithMention(to, ZenTuRyMID)
                elif text.lower() == 'วิดีโอ':
                    me = line.getContact(ZenTuRyMID)
                    ZenTuRy.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'ปก':
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    cover = nadya.getProfileCoverURL(ZenTuRyMID)    
                    ZenTuRy.sendImageWithURL(msg.to, cover)
                    sendMessageWithMention(to, ZenTuRyMID)
                elif msg.text.lower().startswith("me "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = ZenTuRy.getContact(ls)
                            mi_d = contact.mid
                            ZenTuRy.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("มิด "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ mid ]"
                        for ls in lists:
                            ret_ += "\n>" + ls
                        ZenTuRy.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("ชื่อ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = ZenTuRy.getContact(ls)
                            ZenTuRy.sendMessage(msg.to, "ชื่อ:" + contact.displayName)
                elif msg.text.lower().startswith("ตัส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = ZenTuRy.getContact(ls)
                            ZenTuRy.sendMessage(msg.to, "\n" + contact.statusMessage)
                elif msg.text.lower().startswith("ดิส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + ZenTuRy.getContact(ls).pictureStatus
                            ZenTuRy.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("ดิสวีดีโอ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + ZenTuRy.getContact(ls).pictureStatus + "/vp"
                            ZenTuRy.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("ข้อมูล "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = ZenTuRy.getContact(ls)
                            ZenTuRy.sendMessage(msg.to, contact.displayName)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                            contact = ZenTuRy.getContact(ls)
                            ZenTuRy.sendMessage(msg.to, contact.statusMessage)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ">"
                        for ls in lists:
                            ret_ += ls
                        ZenTuRy.sendMessage(msg.to, str(ret_))
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + ZenTuRy.getContact(ls).pictureStatus
                            ZenTuRy.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cover "):
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = ZenTuRy.getProfileCoverURL(ls)
                                ZenTuRy.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("clone "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            ZenTuRy.cloneContactProfile(contact)
                            ZenTuRy.sendMessage(msg.to, "...")
                        except:
                            ZenTuRy.sendMessage(msg.to, "ก็อบปกเสร็จสิ้น")
                            
                elif text.lower() == 'restore':
                    try:
                        ZenTuRyProfile.displayName = str(myProfile["displayName"])
                        ZenTuRyProfile.statusMessage = str(myProfile["statusMessage"])
                        ZenTuRyProfile.pictureStatus = str(myProfile["pictureStatus"])
                        ZenTuRy.updateProfileAttribute(8, ZenTuRyProfile.pictureStatus)
                        ZenTuRy.updateProfile(ZenTuRyProfile)
                        ZenTuRy.sendMessage(msg.to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                    except:
                        ZenTuRy.sendMessage(msg.to, "คืนค่าเสร็จสิ้น")
#==============================================================================#
                elif msg.text.lower().startswith("เตะ "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ZenTuRy.kickoutFromGroup(msg.to,[target])
                        except:
                            ZenTuRy.sendText(msg.to,"Error")
                elif msg.text.lower().startswith("love1 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            ZenTuRy.sendMessage(msg.to,"เพิ่มการเลียนแบบแล้ว(｀・ω・´)")
                            break
                        except:
                            ZenTuRy.sendMessage(msg.to,"Added Target Fail !")
                            break
                elif msg.text.lower().startswith("love2 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            ZenTuRy.sendMessage(msg.to,"ลบการเลียนแบบแล้ว(｀・ω・´)")
                            break
                        except:
                            ZenTuRy.sendMessage(msg.to,"Deleted Target Fail !")
                            break
                elif text.lower() == 'mimiclist':
                    if settings["mimic"]["target"] == {}:
                        ZenTuRy.sendMessage(msg.to,"Tidak Ada Target")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+ZenTuRy.getContact(mi_d).displayName
                        ZenTuRy.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                    
                elif "love" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            ZenTuRy.sendMessage(msg.to,"Reply Message on")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            ZenTuRy.sendMessage(msg.to,"Reply Message off")
#==============================================================================#
                elif text.lower() == 'groupcreator':
                    group = ZenTuRy.getGroup(to)
                    GS = group.creator.mid
                    ZenTuRy.sendContact(to, GS)
                    ZenTuRy.sendMessage(to, "นี่ไงคนสร้างกลุ่ม")
                elif text.lower() == 'ไอดีกลุ่ม':
                    gid = ZenTuRy.getGroup(to)
                    ZenTuRy.sendMessage(to, "\n" + gid.id)
                elif text.lower() == 'รูปกลุ่ม':
                    group = ZenTuRy.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ZenTuRy.sendImageWithURL(to, path)
                elif text.lower() == 'ชื่อกลุ่ม':
                    gid = ZenTuRy.getGroup(to)
                    ZenTuRy.sendMessage(to, "\n" + gid.name)
                elif text.lower() == 'ลิ้งกลุ่ม':
                    if msg.toType == 2:
                        group = ZenTuRy.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = ZenTuRy.reissueGroupTicket(to)
                            ZenTuRy.sendMessage(to, "https://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            ZenTuRy.sendMessage(to, "Grup qr tidak terbuka silahkan buka terlebih dahulu dengan perintah {}openqr".format(str(settings["keyCommand"])))
                elif text.lower() == 'เปิดลิ้ง':
                    if msg.toType == 2:
                        group = ZenTuRy.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ZenTuRy.sendMessage(to, "เปิดลิ้งสำเร็จ(｀・ω・´)")
                        else:
                            group.preventedJoinByTicket = False
                            ZenTuRy.updateGroup(group)
                            ZenTuRy.sendMessage(to, "ลิ้งเปิดอยู่ครับ(｀・ω・´)")
                elif text.lower() == 'ปิดลิ้ง':
                    if msg.toType == 2:
                        group = ZenTuRy.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            ZenTuRy.sendMessage(to, "ปิดอยู่(｀・ω・´)")
                        else:
                            group.preventedJoinByTicket = True
                            ZenTuRy.updateGroup(group)
                            ZenTuRy.sendMessage(to, "ปิดลิ้งสำเร็จ(｀・ω・´)")
                elif text.lower() == 'ข้อมูลกลุ่ม':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "ไม่พบผู้สร้างกลุ่ม"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "ปิด"
                        gTicket = "ปิด"
                    else:
                        gQr = "เปิด"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(ZenTuRy.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "ข้อมูลกลุ่ม"
                    ret_ += "\nชื่อที่แสดง : {}".format(str(group.name))
                    ret_ += "\nรหัสกลุ่ม : {}".format(group.id)
                    ret_ += "\nผู้สร้างกลุ่ม : {}".format(str(gCreator))
                    ret_ += "\nจำนวนสมาชิก : {}".format(str(len(group.members)))
                    ret_ += "\nจำนวนคำเชิญ : {}".format(gPending)
                    ret_ += "\nURL ของกลุ่ม : {}".format(gQr)
                    ret_ += "\nURL ของกลุ่ม : {}".format(gTicket)
                    ret_ += "\n[ 完 ]"
                    ZenTuRy.sendMessage(to, str(ret_))
                    ZenTuRy.sendImageWithURL(to, path)
                elif text.lower() == 'สมาชิก':
                    if msg.toType == 2:
                        group = ZenTuRy.getGroup(to)
                        ret_ = "╔══[ จำนวนสมาชิกทั้งหมด Members List ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ จำนวน {} ]".format(str(len(group.members)))
                        ZenTuRy.sendMessage(to, str(ret_))
                elif text.lower() == 'กลุ่มทั้งหมด':
                        groups = ZenTuRy.groups
                        ret_ = "╔══[ รายชื่อกลุ่มทั้งหมด Groups List ]"
                        no = 0 + 1
                        for gid in groups:
                            group = ZenTuRy.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ มีกลุ่มทั้งหมด {} กลุ่ม ]".format(str(len(groups)))
                        ZenTuRy.sendMessage(to, str(ret_))
#==============================================================================#          
                elif text.lower() == 'tagall':
                    group = ZenTuRy.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        ZenTuRy.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        ZenTuRy.sendMessage(to, "จำนวนสมาชิก {} คน".format(str(len(nama))))          
                elif text.lower() == 'เปิดอ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                ZenTuRy.sendMessage(msg.to,"Selfbot: เปิดอ่านอยู่")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            ZenTuRy.sendMessage(msg.to, "Set reading point:\n" + readTime)
                            
                elif text.lower() == 'ปิดอ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        ZenTuRy.sendMessage(msg.to,"Selfbot: ปิดอ่านอยู่")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        ZenTuRy.sendMessage(msg.to, "Delete reading point:\n" + readTime)
    
                elif text.lower() == 'ลบเวลา':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        ZenTuRy.sendMessage(msg.to, "\n" + readTime)
                    else:
                        ZenTuRy.sendMessage(msg.to, "Lurking belum diaktifkan ngapain di reset?")
                        
                elif text.lower() == 'อ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            ZenTuRy.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = ZenTuRy.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = 'ผู้ที่แอบอ่าน\n\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\nอ่านแล้วไม่ตอบหรอเดะโบกเลย\n" + readTime
                        try:
                            ZenTuRy.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        ZenTuRy.sendMessage(receiver,"Selfbot: ยังไม่ได้เปิดอ่าน")
#==============================================================================#
                elif text.lower() == 'calender':
                    tz = pytz.timezone("Asia/Makassar")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    ZenTuRy.sendMessage(msg.to, readTime)                 
                elif "screenshotwebsite" in msg.text.lower():
                    sep = text.split(" ")
                    query = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        r = web.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                        data = r.text
                        data = json.loads(data)
                        ZenTuRy.sendImageWithURL(to, data["result"])
                elif "checkdate" in msg.text.lower():
                    sep = msg.text.split(" ")
                    tanggal = msg.text.replace(sep[0] + " ","")
                    r=requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                    data=r.text
                    data=json.loads(data)
                    ret_ = "╔══[ D A T E ]"
                    ret_ += "\n╠ Date Of Birth : {}".format(str(data["data"]["lahir"]))
                    ret_ += "\n╠ Age : {}".format(str(data["data"]["usia"]))
                    ret_ += "\n╠ Birthday : {}".format(str(data["data"]["ultah"]))
                    ret_ += "\n╠ Zodiak : {}".format(str(data["data"]["zodiak"]))
                    ret_ += "\n╚══[ Success ]"
                    ZenTuRy.sendMessage(to, str(ret_))
                elif "searchimage" in msg.text.lower():
                    separate = msg.text.split(" ")
                    search = msg.text.replace(separate[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(urllib.parse.quote(search)))
                        data = r.text
                        data = json.loads(data)
                        if data["result"] != []:
                            items = data["result"]
                            path = random.choice(items)
                            a = items.index(path)
                            b = len(items)
                            ZenTuRy.sendImageWithURL(to, str(path))
                elif "searchyoutube" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {"search_query": search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.youtube.com/results", params = params)
                        soup = BeautifulSoup(r.content, "html5lib")
                        ret_ = "╔══[ Youtube Result ]"
                        datas = []
                        for data in soup.select(".yt-lockup-title > a[title]"):
                            if "&lists" not in data["href"]:
                                datas.append(data)
                        for data in datas:
                            ret_ += "\n╠══[ {} ]".format(str(data["title"]))
                            ret_ += "\n╠ https://www.youtube.com{}".format(str(data["href"]))
                        ret_ += "\n╚══[ Total {} ]".format(len(datas))
                        ZenTuRy.sendMessage(to, str(ret_))
                elif "searchmusic" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {'songname': search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://ide.fdlrcn.com/workspace/yumi-apis/joox?" + urllib.parse.urlencode(params))
                        try:
                            data = json.loads(r.text)
                            for song in data:
                                ret_ = "╔══[ Music ]"
                                ret_ += "\n╠ Nama lagu : {}".format(str(song[0]))
                                ret_ += "\n╠ Durasi : {}".format(str(song[1]))
                                ret_ += "\n╠ Link : {}".format(str(song[4]))
                                ret_ += "\n╚══[ reading Audio ]"
                                ZenTuRy.sendMessage(to, str(ret_))
                                ZenTuRy.sendAudioWithURL(to, song[3])
                        except:
                            ZenTuRy.sendMessage(to, "Musik tidak ditemukan")
                elif "searchlyric" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {'songname': search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://ide.fdlrcn.com/workspace/yumi-apis/joox?" + urllib.parse.urlencode(params))
                        try:
                            data = json.loads(r.text)
                            for song in data:
                                songs = song[5]
                                lyric = songs.replace('ti:','Title - ')
                                lyric = lyric.replace('ar:','Artist - ')
                                lyric = lyric.replace('al:','Album - ')
                                removeString = "[1234567890.:]"
                                for char in removeString:
                                    lyric = lyric.replace(char,'')
                                ret_ = "╔══[ Lyric ]"
                                ret_ += "\n╠ Nama lagu : {}".format(str(song[0]))
                                ret_ += "\n╠ Durasi : {}".format(str(song[1]))
                                ret_ += "\n╠ Link : {}".format(str(song[4]))
                                ret_ += "\n╚══[ Finish ]\n{}".format(str(lyric))
                                ZenTuRy.sendMessage(to, str(ret_))
                        except:
                            ZenTuRy.sendMessage(to, "Lirik tidak ditemukan")
            elif msg.contentType == 7:
                if settings["สติกเกอร์"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "╔══( ข้อมูลสติกเกอร์ )"
                    ret_ += "\n╠ สติกเกอร์ id : {}".format(stk_id)
                    ret_ += "\n╠ แพคเกจสติกเกอร์ : {}".format(pkg_id)
                    ret_ += "\n╠ เวอร์ชั่นสติกเกอร: {}".format(stk_ver)
                    ret_ += "\n╠ ลิ้งสติกเกอร์ : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n╚══( ข้อมูลสติกเกอร์ )"
                    ZenTuRy.sendMessage(to, str(ret_))
                    
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = ZenTuRy.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break                             
                        else:
                            targets.append(copy)
                    if targets == []:
                        ZenTuRy.sendText(msg.to, "Not Found...")
                        pass
                    else:
                        for target in targets:
                            try:
                                ZenTuRy.cloneContactProfile(target)
                                ZenTuRy.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                                settings['copy'] = False
                                break
                            except:
                                     msg.contentMetadata = {'mid': target}
                                     settings["copy"] = False
                                     break                     
                    
                    
#==============================================================================#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != ZenTuRy.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    ZenTuRy.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        ZenTuRy.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in ZenTuRyMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys())!= None:
                        if settings['Tag2'] == True:
                             contact = ZenTuRy.getContact(msg._from)
                             cName = contact.pictureStatus
                             balas = ["http://dl.profile.line-cdn.net/" + cName]
                             ret_ = random.choice(balas)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention["MENTIONEES"]
                             for mention in mentionees:
                                   if mention["M"] in ZenTuRyMID:
                                          ZenTuRy.sendImageWithURL(to,ret_)
                                          break
                if msg.contentType == 0 and sender not in ZenTuRyMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys()) != None:
                         if settings['detectMention'] == True:
                             contact = ZenTuRy.getContact(msg._from)
                             cName = contact.displayName
                             balas = ["Selfbot Auto Replied: แทคทำไมเดะโบกเลย ☠"]
                             ret_ = "" + random.choice(balas)
                             name = re.findall(r'@(\w+)', msg.text)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention['MENTIONEES']
                             for mention in mentionees:
                                   if mention['M'] in ZenTuRyMID:
                                          ZenTuRy.sendMessage(to,ret_)
                                          sendMessageWithMention(to, contact.mid)
                                          break
            if msg.text in ["Speed","speed","Sp","sp",".Sp",".sp",".Speed",".speed","!sp","!Sp","!Speed","!speed"]:
            	ZenTuRy.sendMessage(to, "แรงแล้วพี่แรงแล้ว 😜")
            if msg.text in ["เทส","test"]:
            	ZenTuRy.sendMessage(to, "เช็คจังเลยกลัวบอทหลุดหรอ 😜")
            if msg.text in ["แตก","แตก1","แตก 1","แตก!","แตก !","แตก 1!"]:
            	ZenTuRy.sendMessage(to, "สวยพี่สวย 😜")
            if msg.text in ["โอม","โอมมี่","ohm"]:
            	ZenTuRy.sendMessage(to, "Selfbot Auto Replied: โอมไม่อยู่ 😜")
            if msg.text in ["บอท","bot"]:
            	ZenTuRy.sendMessage(to, "บอทยังออนไลน์อยู่ 😜")
#==============================================================================#
            if msg.text in ["!groupcreator","!Groupcreator"]:
            	group = ZenTuRy.getGroup(to)
            	GS = group.creator.mid
            	ZenTuRy.sendContact(to, GS)
            	ZenTuRy.sendMessage(to, "นี่ไงคนสร้างกลุ่ม")
            if msg.text in ["!online","!Online"]:
            	timeNow = time.time()
            	runtime = timeNow - botStart
            	runtime = format_timespan(runtime)
            	ZenTuRy.sendMessage(to, "ระยะเวลาการทำงานของบอท\n{}".format(str(runtime)))
            if msg.text in ["!test","!Test"]:
                    ZenTuRy.sendMessage(to,"LOADING:▒...0%")
                    ZenTuRy.sendMessage(to,"█▒... 10.0%")
                    ZenTuRy.sendMessage(to,"██▒... 20.0%")
                    ZenTuRy.sendMessage(to,"███▒... 30.0%")
                    ZenTuRy.sendMessage(to,"████▒... 40.0%")
                    ZenTuRy.sendMessage(to,"█████▒... 50.0%")
                    ZenTuRy.sendMessage(to,"██████▒... 60.0%")
                    ZenTuRy.sendMessage(to,"███████▒... 70.0%")
                    ZenTuRy.sendMessage(to,"████████▒... 80.0%")
                    ZenTuRy.sendMessage(to,"█████████▒... 90.0%")
                    ZenTuRy.sendMessage(to,"███████████..100.0%")
                    ZenTuRy.sendMessage(to,"บอทยังอยู่ดีไม่หลุด 😂")
            if msg.text in ["!sp","!Sp"]:
                    start = time.time()
                    ZenTuRy.sendMessage(to, "⚡ความเร็วบอทอยู่ที่⚡")
                    elapsed_time = time.time() - start
                    ZenTuRy.sendMessage(to,format(str(elapsed_time)))
            if msg.text in ["!tagall","!Tagall"]:
                    group = ZenTuRy.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        ZenTuRy.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        ZenTuRy.sendMessage(to, "จำนวนคนในการแทค {} คน".format(str(len(nama))))      
            if msg.text in ["!help","!Help"]:
                    helpOhm = helpohm()
                    ZenTuRy.sendMessage(to, str(helpOhm))
            if msg.text in ["!ohm","!Ohm"]:
                    ZenTuRy.sendMessage(to, "ME")
                    ZenTuRy.sendContact(to, ZenTuRyMID)
                    ZenTuRy.sendMessage(to, "STATUS")
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    ZenTuRy.sendMessage(msg.to,">" + me.statusMessage)
                    ZenTuRy.sendMessage(to, "PICTURE PROFILE")
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    ZenTuRy.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                    ZenTuRy.sendMessage(to, "COVER PROFILE")
                    me = ZenTuRy.getContact(ZenTuRyMID)
                    cover = ZenTuRy.getProfileCoverURL(ZenTuRyMID)    
                    ZenTuRy.sendImageWithURL(msg.to, cover)
#==============================================================================#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != line.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    ZenTuRy.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        ZenTuRy.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in ZenTuRyMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if ZenTuRyMID in mention["M"]:
                              if settings["detectMention"] == True:
                                 sendMention(receiver, sender, "", "????")

        if op.type == 17:
           print ("MEMBER JOIN TO GROUP")
           if settings["Sambutan"] == True:
             if op.param2 in ZenTuRyMID:
                 return
             ginfo = ZenTuRy.getGroup(op.param1)
             contact = ZenTuRy.getContact(op.param2)
             image = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
             ZenTuRy.sendMessage(op.param1,"Hi " + ZenTuRy.getContact(op.param2).displayName + "\nWelcome To ☞ " + str(ginfo.name) + " ☜" + "\nTEST")
             ZenTuRy.sendImageWithURL(op.param1,image)

        if op.type == 15:
           print ("MEMBER LEAVE TO GROUP")
           if settings["Sambutan"] == True:
             if op.param2 in ZenTuRyMID:
                 return
             ginfo = ZenTuRy.getGroup(op.param1)
             contact = ZenTuRy.getContact(op.param2)
             image = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
             ZenTuRy.sendImageWithURL(op.param1,image)
             ZenTuRy.sendMessage(op.param1,"Good Bye " + ZenTuRy.getContact(op.param2).displayName + "\nSee You Next Time")
#==============================================================================#   
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
