import tkinter as tk
import math
import pygame
import random
import pandas as pd
from PIL import Image, ImageTk

class RouletteApp():

    def __init__(self, file): #初期化，アプリと管理画面の起動
        # root
        self.root = tk.Tk()
        self.root.title("RouletteApp")
        self.win_w, self.win_h = self.root.maxsize()
        self.win_w =int(self.win_w*0.9)
        self.win_h =int(self.win_h*0.9)
        self.win_size = "{}x{}".format(self.win_w, self.win_h)
        self.root.geometry(self.win_size)
        self.root.resizable(0, 0)

        # window size
        self.player = self.load_player(file)
        self.fan_tags = self.player.tag.tolist()
        
        # sub
        self.sub = tk.Toplevel()
        self.sub_w = 500
        self.sub_h = 300
        self.sub.geometry("{}x{}".format(self.sub_w, self.sub_h))
        self.set_subwindow()
        self.create_display()
        self.reload_roulette()
        pygame.mixer.init()
        self.roulette_sound=pygame.mixer.Sound("./roulette-effect.mp3")
        self.winner_sound=pygame.mixer.Sound("./winner.mp3")
        self.static=True
        self.check_roulette(0)

    def load_player(self, file): #ロード
        player = pd.read_csv(file)
        return player

    def create_display(self): #ディスプレイ表示
        global img
        # Canvas
        self.canvas = tk.Canvas(self.root,
                                width=self.win_w,
                                height=self.win_h,
                                background="#FFFFFF")
        self.canvas.place(x=0, y=0)
        img=Image.open("background.jpg")
        img=img.resize((self.win_w,self.win_h))
        img.putalpha(64)
        img=ImageTk.PhotoImage(img)
        self.canvas.create_image(0,0,anchor='nw',image=img)
        # set buttons
        self.set_butttons()
        # set circle
        self.set_circle()
        
        self.select = 0
        # set result text
        self.set_result_text()

    def reload_roulette(self): # 画面のリロード，当選確率上昇を更新
        self.canvas.delete("all")
        self.fan_tags=[]
        for i in self.player.tag:
            if not self.win_or_not[i].get(): # 当たりの人以外描写
                for j in range(self.prob[i].get()*(1+self.presenter[i].get())):
                    self.fan_tags.append(i+"_"+str(j))
        self.create_display()

    def increment_roulette(self): # 自動でインクリメント
        for i, data in self.player.iterrows():
            value = self.prob[data.tag].get()
            self.prob[data.tag].set(value+data.increment)

    def set_subwindow(self): #管理画面
        self.prob = {}
        self.spin = {}
        self.win_or_not = {}
        self.check_btn = {}
        self.present_check_btn = {}
        self.presenter = {}
        fg_color=["black","red"]

        for i, data in self.player.iterrows():
            self.prob[data.tag] = tk.IntVar(self.sub) #当選枠数の変数
            self.prob[data.tag].set(data.init)
            self.spin[data.tag] = tk.Spinbox(self.sub,textvariable=self.prob[data.tag],
                       from_=0,to=20,increment=data.increment,width=10) 

            self.presenter[data.tag]=tk.BooleanVar() #プレゼントの提案者か否か
            self.present_check_btn[data.tag] = tk.Checkbutton(self.sub,text="presenter",variable=self.presenter[data.tag],fg=fg_color[data.increment>0])

            self.win_or_not[data.tag]=tk.BooleanVar() #当選したか否か
            self.check_btn[data.tag] = tk.Checkbutton(self.sub,text=data.tag,variable=self.win_or_not[data.tag],fg=fg_color[data.increment>0])
            
            self.present_check_btn[data.tag].grid(row=i%10,column=0+int(i/10)*3) #描画
            self.check_btn[data.tag].grid(row=i%10,column=1+int(i/10)*3)
            self.spin[data.tag].grid(row=i%10,column=2+int(i/10)*3)

        # increment, reloadボタンの表示
        self.increment_btn = tk.Button(self.sub,text="Next",font=("",18), command=self.increment_roulette)
        self.increment_btn.place(x=self.sub_w*3/5,y=250,width=100,height=50)
        self.reload_btn = tk.Button(self.sub,text="Reload",font=("",18), command=self.reload_roulette)
        self.reload_btn.place(x=self.sub_w*1/5,y=250,width=100,height=50)

    def set_butttons(self): #スタートとストップボタンの描画
        # Button
        btn_w = int(self.win_w / 5)
        btn_h = int(btn_w / 3)
        btn_margin = 50
        btn_x_start = 0+10
        btn_x_stop = btn_w * 4-10
        btn_y = self.win_h - (btn_h + btn_margin)
        self.btn_start = tk.Button(text="Start",
                              font=("", 24),
                              command=self.clk_start)
        self.btn_start.place(x=btn_x_start, y=btn_y, width=btn_w, height=btn_h,)
        self.btn_stop = tk.Button(text="Stop",
                             font=("", 24),
                             state="disabled",
                             command=self.clk_stop)
        self.btn_stop.place(x=btn_x_stop, y=btn_y, width=btn_w, height=btn_h)

    def set_circle(self): #ルーレットの表示
        # Circle Settings
        self.circle_r = int((self.win_h*4/5-(24+20))/1.2)/2
        circle_ltx = self.win_w / 2 - self.circle_r
        circle_lty = 150
        circle_rbx = circle_ltx + self.circle_r * 2
        circle_rby = circle_lty + self.circle_r * 2
        random.shuffle(self.fan_tags) #ランダムシャッフル
    
        # Circle
        angle = 360/len(self.fan_tags) #角度
        start = 0        
        for i in range(len(self.fan_tags)-1): #扇を作成
            self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                                    width=2,
                                    start=start, extent=angle,
                                    tag=self.fan_tags[i])
            self.draw_text_on_arc(circle_ltx, circle_lty, circle_rbx, circle_rby, start, angle, self.fan_tags[i])
            start += angle
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                                width=2,
                                start=start, extent=360-start,
                                tag=self.fan_tags[-1])
        self.draw_text_on_arc(circle_ltx, circle_lty, circle_rbx, circle_rby, start, 360-start, self.fan_tags[-1])

    def draw_text_on_arc(self, ltx, lty, rbx, rby, start, extent, tag):# 扇に対応する人を紐づけ
        radius = (rbx - ltx) / 2
        mid_angle = start + extent / 2
        mid_angle_rad = math.radians(360-mid_angle)
        center_x = (ltx + rbx) / 2
        center_y = (lty + rby) / 2
        text_x = center_x + radius * math.cos(mid_angle_rad)*1.2
        text_y = center_y + radius * math.sin(mid_angle_rad)*1.2
        self.canvas.create_text(text_x, text_y, text=tag.split("_")[0],font=("",18))

    def set_result_text(self): #当選候補者を表示する枠を描画
        rect_width = int(self.win_w/5)
        rect_height = 24+20
        txt_x = self.win_w / 2
        txt_y = rect_height+10

        self.txt_tag = "result_text"
        self.canvas.create_text(txt_x, txt_y,
                                text="",
                                font=("", 24),
                                tag=self.txt_tag)
        
        self.canvas.create_rectangle(txt_x-rect_width/2, txt_y-rect_height/2,
                                     txt_x+rect_width/2, txt_y+rect_height/2,
                                     outline="red", width=7)

    def rotate_fans(self): # 点滅させて，画面に当選者候補を表示
        self.roulette_sound.play(maxtime=100)
        self.canvas.itemconfig(self.fan_tags[self.select],outline="black",width=2)
        self.select=(self.select+1)%len(self.fan_tags)
        self.canvas.itemconfig(self.fan_tags[self.select],outline="red",width=10)
        self.canvas.itemconfig(self.txt_tag,text=self.fan_tags[self.select].split("_")[0])

    def check_roulette(self, flag): # 待ち状態時に点滅させてるだけ
        flag %=2
        color=["black","red"]
        width=[2,10]
        self.canvas.itemconfig(self.fan_tags[self.select],outline=color[flag],width=width[flag])
        if(self.static is True):
            flag+=1
        else:
            flag=1
        self.root.after(500,self.check_roulette,flag)
        
    def rotate_100ms(self): #ストップするまで100msで移動
        self.rotate_fans()
        self.after_id = self.root.after(100, self.rotate_100ms)

    def rotate_ms(self, msec, cnt): #ストップボタン後にランダム回数ごとに低速化
        self.rotate_fans()
        cnt -= 1
        if(cnt <= 0):
            self.root.after_cancel(self.after_id)
            if(msec < 800):
                cnt=2+random.randint(1,3)
                self.after_id = self.root.after(msec+200,self.rotate_ms,msec+200,cnt)
            else: #1sごとに移動し終えたら当たり
                self.winner_sound.play()
                self.static=True
                self.btn_start["state"] = "active"
            return 0
        self.after_id = self.root.after(msec, self.rotate_ms, msec, cnt)

    def clk_start(self): #ルーレットスタート
        self.static=False
        self.btn_start["state"] = "disable"
        self.btn_stop["state"] = "active"
        self.rotate_100ms()

    def clk_stop(self): #ルーレットストップ
        self.btn_stop["state"] = "disable"
        self.root.after_cancel(self.after_id)
        self.rotate_ms(200,random.randint(1,20))
        self.check_roulette(0)


if __name__ == '__main__':
    file = input("file name:")
    rouletteapp = RouletteApp(file)
    rouletteapp.root.mainloop()
