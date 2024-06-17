import pygame
import win32gui
import win32con
import win32api
import random
import pygetwindow as gw

with open("opt") as f:
    e = str(f.read()).split("\n")
    d = []
    for i in e:
        d.append(i.split("#")[0])
    w,h = int(d[0]),int(d[1])
    g = d[2].split(",")
    friction = float(d[3])
    launch = float(d[4])
    bouncex = float(d[5])
    bouncey = float(d[6])
    bt = int(d[7])
    c = []
    for i in g:
        c.append(int(i))
    dc = []
    for i in c:
        dc.append(255-i)


screen = pygame.display.set_mode((w,h),pygame.NOFRAME)
pygame.display.set_caption("Block")
hwnd = pygame.display.get_wm_info()['window']

clock = pygame.time.Clock()

mpos = [[0,0],[0,0]]
cpos = [0,0]
veloc = pygame.math.Vector2(random.randint(-5,5),0)
pos = pygame.math.Vector2(random.randint(0,win32api.GetSystemMetrics(0)-w),0)

dt = 0
frame = 0

win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)

while 1:
    tbh = 48
    
    
    if frame % 10000 == random.randint(0,10000):
        if pos.y == win32api.GetSystemMetrics(1)-tbh-h:
            veloc.y = -2.5
            veloc.x = random.randint(-5,5)
    cpos = list(pygame.mouse.get_pos())
    veloc.y += 0.1
    veloc.x *= friction
    pos.y += veloc.y * dt
    pos.x += veloc.x * dt
    if pos.y > win32api.GetSystemMetrics(1)-tbh-h:
        pos.y = win32api.GetSystemMetrics(1)-tbh-h
        veloc.y *= -bouncey
    if pos.y < 0:
        pos.y = 0
        veloc.y *= -bouncey
    if pos.x < 0:
        pos.x = 0
        veloc.x *= -bouncex
    if pos.x > win32api.GetSystemMetrics(0)-w:
        pos.x = win32api.GetSystemMetrics(0)-w
        veloc.x *= -bouncex
    
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                exit()
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mpos[0] = list(pygame.mouse.get_pos())
        if e.type == pygame.MOUSEBUTTONUP:
            mpos[1] = list(pygame.mouse.get_pos())
            veloc.x = mpos[0][0] - mpos[1][0]
            veloc.x *= launch
            veloc.y = mpos[0][1] - mpos[1][1]
            veloc.y *= launch
    if pygame.Rect(pos.x,pos.y,w,h).collidepoint(cpos[0],cpos[1]):
        win32gui.ShowWindow(hwnd,5)
            
            
    screen.fill(c)
    pygame.draw.rect(screen,dc,pygame.Rect(0,0,w,h))
    pygame.draw.rect(screen,c,pygame.Rect(0+bt,0+bt,w-(bt*2),h-(bt*2)))
    
    if pygame.mouse.get_pressed()[0]:
        pygame.draw.line(screen,"red",mpos[0],pygame.mouse.get_pos(),5)
    
    pygame.display.set_window_position((round(pos.x),round(pos.y)))
    win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    pygame.display.flip()
    dt = clock.tick(60) / 60 * 15
    frame += 1