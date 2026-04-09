import pygame as pg
import color_rgb as cr
import random as rd

#初始化
pg.init()

#失败预设
font = pg.font.Font("C:\Windows\Fonts\STKAITI.TTF",25)
fontFallText = font.render("老弟你有啥用",True,cr.草绿)
locOfFail = fontFallText.get_rect(center = (600,200))

#成功预设
fontSuccessText = font.render("You win!",True,cr.草绿)
locOfSuccess = fontSuccessText.get_rect(center = (600,200))

#界面绘制
window = pg.display.set_mode((800,600))
pg.display.set_caption("2048") #设置标题
window.fill(cr.天蓝) #背景颜色

#绘制表格框架
pg.draw.rect(window,'black',(100,100,400,400),1)
pg.draw.line(window,'black',(100,200),(500,200),1)
pg.draw.line(window,'black',(100,300),(500,300),1)
pg.draw.line(window,'black',(100,400),(500,400),1)
pg.draw.line(window,'black',(200,100),(200,500),1)
pg.draw.line(window,'black',(300,100),(300,500),1)
pg.draw.line(window,'black',(400,100),(400,500),1)

#按钮
class Button():

    def __init__(self,x,y,height,width,text,callback):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.callback = callback
        self.color = (135, 206, 235)
        self.disabled = False  #设置禁用
        self.rect = pg.Rect(x,y,width,height)
        self.font = pg.font.Font(None,70)
        self.draw_button(window)

    def draw_button(self,window) :
        pg.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))
        text_ = self.font.render(self.text,True,(0,0,0))
        location = text_.get_rect(center = (self.x+0.5*self.width,self.y+0.5*self.height))
        window.blit(text_,location)

    def callback_button(self,event) :
        if self.disabled == False :
            self.draw_button(window)
            if event.type == pg.MOUSEMOTION :

                if self.rect.collidepoint(event.pos) :
                    self.color = (218, 165, 32)
                else :
                    self.color = (135, 206, 235)

            if event.type == pg.MOUSEBUTTONDOWN :

                if self.rect.collidepoint(event.pos) :
                    if event.button == 1 :
                        self.color = (218, 165, 32)
                        self.callback()

nums = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
        ]

#棋盘数字
class Digit():

    def __init__(self,location:list,):
        self.location = location
        self.value = nums[self.location[0]-1][self.location[1]-1]
        self.font = pg.font.Font(None,80)
        self.render()
    
    def render(self):
        self.value = nums[self.location[0]-1][self.location[1]-1]
        if self.value != 0:
            self.text_ = self.font.render(str(self.value),True,cr.土黄)
            text_rect = self.text_.get_rect(center = (self.location[0]*100+50,self.location[1]*100+50))
            window.blit(self.text_,text_rect)

    def clear(self):
        pg.draw.rect(window,cr.天蓝,(self.location[0]*100+1,self.location[1]*100+1,98,98))
    
#实例化方格处的数字对象
aa = Digit([1,1])
ab = Digit([1,2])
ac = Digit([1,3])
ad = Digit([1,4])
ba = Digit([2,1])
bb = Digit([2,2])
bc = Digit([2,3])
bd = Digit([2,4])
ca = Digit([3,1])
cb = Digit([3,2])
cc = Digit([3,3])
cd = Digit([3,4])
da = Digit([4,1])
db = Digit([4,2])
dc = Digit([4,3])
dd = Digit([4,4])

allDigits = [aa,ab,ac,ad,ba,bb,bc,bd,ca,cb,cc,cd,da,db,dc,dd]

#设置按钮
def reset():
    pg.draw.rect(window,cr.天蓝,(502,100,298,150))
    global nums

    nums = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
        ]

    i , m = rd.sample([0,1,2,3],2)
    j , n = rd.sample([0,1,2,3],2)
    nums[i][j] = rd.choice([2,2,2,4]) #75% 2 25% 4
    nums[m][n] = rd.choice([2,2,2,4])
    [digit.clear() for digit in allDigits]
    [digit.render() for digit in allDigits]
Reset = Button(600,300,70,150,'Reset',reset)

#判断最大
def findMax():
    global nums
    maxium = max([max(nums[i]) for i in range(4)])
    return maxium

#判断失败
def fail():
    global nums
    numbers = [nums[i][j] for i in range(4) for j in range(4)]
    if 0 not in numbers and findMax() < 2048:
        for i in range(4):
            for j in range(3):
                if nums[i][j] == nums[i][j+1]:
                    return False
                
                if nums[j][i] == nums[j+1][i]:
                    return False
        return True
    else:
        return False

#新建数据
def creatNew():
    global nums
    numbers = [nums[i][j] for i in range(4) for j in range(4)]
    if 0 in numbers:
        blank = []
        for i in range(4):
            for j in range(4):
                if nums[i][j] == 0:
                    blank.append([i,j])
        i,j = rd.choice(blank)
        nums[i][j] = rd.choice([2,2,2,4])

#移动函数 删0 => 合并 => 补0 => 添加新数字 => 渲染
def moveLeft():
    global nums
    for i in range(4):
        while 0 in nums[i]:
            nums[i].remove(0)
        j = 0
        while j < len(nums[i]) - 1:
            if nums[i][j] == nums[i][j+1]:
                nums[i][j] *= 2
                nums[i].pop(j+1)
            else:
                j += 1
        while len(nums[i]) < 4:
            nums[i].append(0)
    
    creatNew()
    [digit.clear() for digit in allDigits]
    [digit.render() for digit in allDigits]

def moveRight():
    global nums
    for i in range(4):
        while 0 in nums[i]:
            nums[i].remove(0)
        j = len(nums[i]) - 1
        while j > 0:
            if j >= len(nums[i]):
                j -= 1
                continue
            if nums[i][j] == nums[i][j-1]:
                nums[i][j] *= 2
                nums[i].pop(j-1)
            else:
                j -= 1
        while len(nums[i]) < 4:
            nums[i].insert(0,0)
    
    creatNew()
    [digit.clear() for digit in allDigits]
    [digit.render() for digit in allDigits]

def moveUp():
    global nums
    for i in range(4):
        number = [nums[j][i] for j in range(4)]
        while 0 in number:
            number.remove(0)
        j = 0
        while j < len(number) - 1:
            if number[j] == number[j+1]:
                number[j] *= 2
                number.pop(j+1)
            else:
                j += 1
            
        while len(number) < 4:
            number.append(0)

        for j in range(4):
            nums[j][i] = number[j]
    
    creatNew()
    [digit.clear() for digit in allDigits]
    [digit.render() for digit in allDigits]

def moveDown():
    global nums
    for i in range(4):
        number = [nums[j][i] for j in range(4)]
        while 0 in number:
            number.remove(0)
        j = len(number) - 1
        while j > 0:
            if j >= len(number):
                j -= 1
                continue
            if number[j] == number[j-1]:
                number[j] *= 2
                number.pop(j-1)
            else:
                j -= 1
            
        while len(number) < 4:
            number.insert(0,0)

        for j in range(4):
            nums[j][i] = number[j]
    
    creatNew()
    [digit.clear() for digit in allDigits]
    [digit.render() for digit in allDigits]


#主循环
running = True

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        #处理按钮事件
        Reset.callback_button(event)

        if event.type == pg.KEYDOWN:
            # print(nums)
            if event.key == pg.K_LEFT:
                moveUp()
            if event.key == pg.K_RIGHT:
                moveDown()
            if event.key == pg.K_UP:
                moveLeft()
            if event.key == pg.K_DOWN:
                moveRight()

    if fail():
        window.blit(fontFallText,locOfFail)
    
    if findMax() >= 2048:
        window.blit(fontSuccessText,locOfSuccess)

    pg.display.update()
    pg.time.Clock().tick(60) #刷新率60Hz

pg.quit()