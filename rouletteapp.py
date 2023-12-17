import tkinter as tk
import math
import pygame
import random
import pandas as pd

class RouletteApp():

    def __init__(self, file):
        # window size
        self.win_w = 900
        self.win_h = 1000
        self.win_size = "{}x{}".format(self.win_w, self.win_h)
        self.player = self.load_player(file)
        self.fan_tags = self.player.tag.tolist()

        # root
        self.root = tk.Tk()
        self.root.title("RouletteApp")
        self.root.geometry(self.win_size)
        self.root.resizable(0, 0)
        
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

    def load_player(self, file):
        player = pd.read_csv(file)
        return player

    def create_display(self):
        # Canvas
        self.canvas = tk.Canvas(self.root,
                                width=self.win_w,
                                height=self.win_h,
                                background="#FFFFFF")
        self.canvas.place(x=0, y=0)
        # set buttons
        self.set_butttons()
        # set circle
        self.set_circle()
        
        self.select = 0
        # set result text
        self.set_result_text()

    def reload_roulette(self):
        self.canvas.delete("all")
        self.fan_tags=[]
        for i in self.player.tag:
            if not self.win_or_not[i].get():
                for j in range(self.prob[i].get()):
                    self.fan_tags.append(i+"_"+str(j))
        self.create_display()


    def set_subwindow(self):
        self.prob = {}
        self.spin = {}
        self.win_or_not = {}
        self.check_btn = {}
        fg_color=["black","red"]
        for i, data in self.player.iterrows():
            self.prob[data.tag] = tk.IntVar(self.sub)
            self.prob[data.tag].set(data.init)
            self.spin[data.tag] = tk.Spinbox(self.sub,textvariable=self.prob[data.tag],
                       from_=0,to=15,increment=data.increment,)
            self.win_or_not[data.tag]=tk.BooleanVar()
            self.check_btn[data.tag] = tk.Checkbutton(self.sub,text=data.tag,variable=self.win_or_not[data.tag],fg=fg_color[data.increment>0])
            self.check_btn[data.tag].grid(row=i%10,column=0+int(i/10)*2)
            self.spin[data.tag].grid(row=i%10,column=1+int(i/10)*2)
        
        self.reload_btn = tk.Button(self.sub,text="Reload",font=("",18), command=self.reload_roulette)
        self.reload_btn.place(x=self.sub_w*2/5,y=250,width=100,height=50)

    def set_butttons(self):
        # Button
        btn_w = int(self.win_w / 5)
        btn_h = int(btn_w / 2)
        btn_margin = 50
        btn_x_start = btn_w * 1
        btn_x_stop = btn_w * 3
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

    def set_circle(self):
        # Circle Settings
        self.circle_r = 300
        circle_ltx = self.win_w / 2 - self.circle_r
        circle_lty = 150
        circle_rbx = circle_ltx + self.circle_r * 2
        circle_rby = circle_lty + self.circle_r * 2
        random.shuffle(self.fan_tags)
    
        # Circle
        angle = 360/len(self.fan_tags)
        start = 0        
        for i in range(len(self.fan_tags)-1):
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

    def draw_text_on_arc(self, ltx, lty, rbx, rby, start, extent, tag):# show tags
        radius = (rbx - ltx) / 2
        mid_angle = start + extent / 2
        mid_angle_rad = math.radians(360-mid_angle)
        center_x = (ltx + rbx) / 2
        center_y = (lty + rby) / 2
        text_x = center_x + radius * math.cos(mid_angle_rad)*1.2
        text_y = center_y + radius * math.sin(mid_angle_rad)*1.2
        self.canvas.create_text(text_x, text_y, text=tag.split("_")[0],font=("",18))

    def set_result_text(self):
        txt_x = self.win_w / 2
        txt_y = self.win_h / 2 - self.circle_r - 170
        self.txt_tag = "result_text"
        self.canvas.create_text(txt_x, txt_y,
                                text="",
                                font=("", 24),
                                tag=self.txt_tag)
        
        rect_width = 200
        rect_height = 24+20
        self.canvas.create_rectangle(txt_x-rect_width/2, txt_y-rect_height/2,
                                     txt_x+rect_width/2, txt_y+rect_height/2,
                                     outline="red", width=7)

    def rotate_fans(self):
        self.roulette_sound.play(maxtime=100)
        self.canvas.itemconfig(self.fan_tags[self.select],outline="black",width=2)
        self.select=(self.select+1)%len(self.fan_tags)
        self.canvas.itemconfig(self.fan_tags[self.select],outline="red",width=10)
        self.canvas.itemconfig(self.txt_tag,text=self.fan_tags[self.select].split("_")[0])

    def check_roulette(self, flag):
        flag %=2
        color=["black","red"]
        width=[2,10]
        self.canvas.itemconfig(self.fan_tags[self.select],outline=color[flag],width=width[flag])
        if(self.static is True):
            flag+=1
        else:
            flag=1
        self.root.after(500,self.check_roulette,flag)
        
    def rotate_10ms(self):
        self.rotate_fans()
        self.after_id = self.root.after(100, self.rotate_10ms)

    def rotate_ms(self, msec, cnt):
        self.rotate_fans()
        cnt -= 1
        if(cnt <= 0):
            self.root.after_cancel(self.after_id)
            if(msec < 800):
                cnt=3
                self.after_id = self.root.after(msec+200,self.rotate_ms,msec+200,cnt)
            else:
                self.winner_sound.play()
                self.static=True
                self.btn_start["state"] = "active"
            return 0
        self.after_id = self.root.after(msec, self.rotate_ms, msec, cnt)

    def clk_start(self):
        self.static=False
        self.btn_start["state"] = "disable"
        self.btn_stop["state"] = "active"
        self.rotate_10ms()

    def clk_stop(self):
        self.btn_stop["state"] = "disable"
        self.root.after_cancel(self.after_id)
        self.rotate_ms(200,random.randint(1,20))
        self.check_roulette(0)


if __name__ == '__main__':
    file = input("file name:")
    rouletteapp = RouletteApp(file)
    rouletteapp.root.mainloop()
