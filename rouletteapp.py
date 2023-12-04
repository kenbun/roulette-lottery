import tkinter as tk
import numpy as np


class RouletteApp():

    def __init__(self):
        # window size
        self.win_w = 800
        self.win_h = 800
        self.win_size = "{}x{}".format(self.win_w, self.win_h)
        # root
        self.root = tk.Tk()
        self.root.title("RouletteApp Part6")
        self.root.geometry(self.win_size)
        self.root.resizable(0, 0)
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
        self.fan_tags = ["fan01", "fan02", "fan03", "fan04", "fan05", "fan06"]
        # set triangle
        self.set_triangle()
        # set result text
        self.set_result_text()
        # check roulette
        self.color_dict = {"#C7000B":"Red", "#D28300":"Orange", "#DFD000":"Yellow",
                           "#00873C":"Green", "#005AA0":"Blue", "#800073":"Purple"}

    def set_butttons(self):
        # Button
        btn_w = int(self.win_w / 5)
        btn_h = int(btn_w / 2)
        btn_margin = 50
        btn_x_start = btn_w * 1
        btn_x_stop = btn_w * 3
        btn_y = self.win_h - (btn_h + btn_margin)
        btn_start = tk.Button(text="Start",
                              font=("", 24),
                              command=self.clk_start)
        btn_start.place(x=btn_x_start, y=btn_y, width=btn_w, height=btn_h,)
        btn_stop = tk.Button(text="Stop",
                             font=("", 24),
                             command=self.clk_stop)
        btn_stop.place(x=btn_x_stop, y=btn_y, width=btn_w, height=btn_h)

    def set_circle(self):
        # Circle Settings
        self.circle_r = 200
        circle_ltx = self.win_w / 2 - self.circle_r
        circle_lty = 200
        circle_rbx = circle_ltx + self.circle_r * 2
        circle_rby = circle_lty + self.circle_r * 2
        # Circle
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                               width=2,
                               start=30, extent=60,
                               fill="#C7000B",
                               tag="fan01")
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                               width=2,
                               start=90, extent=60,
                               fill="#D28300",
                               tag="fan02")
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                               width=2,
                               start=150, extent=60,
                               fill="#DFD000",
                               tag="fan03")
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                               width=2,
                               start=210, extent=60,
                               fill="#00873C",
                               tag="fan04")
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                               width=2,
                               start=270, extent=60,
                               fill="#005AA0",
                               tag="fan05")
        self.canvas.create_arc(circle_ltx, circle_lty, circle_rbx, circle_rby,
                               width=2,
                               start=330, extent=60,
                               fill="#800073",
                               tag="fan06")

    def set_triangle(self):
        tri_edge_half = round((30 * np.cos(np.radians(30))), 1)
        tri_edge = tri_edge_half * 2
        tri_edge_height = round(tri_edge * np.cos(np.radians(30)), 1)
        (tri_btm_x, tri_btm_y) = (self.win_w / 2, self.win_h / 2 - self.circle_r - 10)
        (tri_lt_x, tri_lt_y) = (tri_btm_x - tri_edge_half, tri_btm_y - tri_edge_height)
        (tri_rt_x, tri_rt_y) = (tri_btm_x + tri_edge_half, tri_btm_y - tri_edge_height)
        self.canvas.create_polygon(tri_btm_x, tri_btm_y,
                                   tri_lt_x, tri_lt_y,
                                   tri_rt_x, tri_rt_y,
                                   tri_btm_x, tri_btm_y,
                                   outline="",
                                   joinstyle=tk.MITER,
                                   fill="#000000")

    def set_result_text(self):
        txt_x = self.win_w / 2
        txt_y = self.win_h / 2 - self.circle_r - 125
        self.txt_tag = "result_text"
        self.canvas.create_text(txt_x, txt_y,
                                text="Result",
                                font=("", 24),
                                tag=self.txt_tag)

    def rotate_fans(self):
        for fan_tag in self.fan_tags:
            start_angle = self.canvas.itemcget(fan_tag, "start")
            start_angle = str(float(start_angle) - 10)
            self.canvas.itemconfig(fan_tag, start=start_angle)

    def check_roulette(self):
        for fan_tag in self.fan_tags:
            start_angle = float(self.canvas.itemcget(fan_tag, "start"))
            if(start_angle <= 90 and 90 < (start_angle + 60)):
                color = self.canvas.itemcget(fan_tag, "fill")
                self.canvas.itemconfig(self.txt_tag, text=self.color_dict[color])

    def rotate_10ms(self):
        self.rotate_fans()
        self.after_id = self.root.after(10, self.rotate_10ms)

    def rotate_ms(self, msec, cnt):
        self.rotate_fans()
        cnt -= 1
        if(cnt <= 0):
            self.root.after_cancel(self.after_id)
            return
        self.after_id = self.root.after(msec, self.rotate_ms, msec, cnt)

    def clk_start(self):
        self.canvas.itemconfig(self.txt_tag, text="")
        self.rotate_10ms()

    def clk_stop(self):
        self.root.after_cancel(self.after_id)
        cnt = np.random.randint(18, 36)
        self.rotate_ms(100, cnt)
        cnt = np.random.randint(12, 18)
        self.rotate_ms(500, cnt)
        self.check_roulette()


if __name__ == '__main__':
    rouletteapp = RouletteApp()
    rouletteapp.root.mainloop()
