#!/usr/bin/env python3
import pygame
import sys
import time

"""
chart = [0] * 1000
chart[1] = 1
def f(x):
    if chart[x] == 0:
        n = x * f(x-1)
        chart[x] = n
        return n
    else: return chart[n]
    
def C(m, n):
    return f(m) // (f(n) * f(m-n))
"""

print('''
Usage: bezier4.py [accuracy]
accuracy is a float which defaults to 1e-3. The smaller it is, the more accurate the curve is and the slower the program.

COLOR CHART:
Red - The place where you pressed the mouse
Blue - the place you released mouse, which decides the ending way of the last curve segment.
Green - Auto calculated, used to decide the starting way of next segment of curve.
COMMAND CHART:
p - clear argument point
c - clean everything
g - generate one Bezier curve
e - erase''')

ACCURACY = 0.001

if len(sys.argv) >= 2:
    try:
        ACCURACY = float(sys.argv[1])
    except ValueError:
        pass

lastx, lasty = 0, 0
BUFFER_SURFACE = pygame.Surface((800, 600))

def clear():
    BUFFER_SURFACE.fill((0, 0, 0))
def plt(x, y):
    global lastx, lasty
    x = int(x)
    y = int(y)
    if lastx == 0 and lasty == 0:
        lastx = x
        lasty = y
        return
    pygame.draw.aaline(BUFFER_SURFACE, (255, 0, 0), (x, y), (lastx, lasty))
    lastx = x
    lasty = y
    
    
def bezier(arr, t):
    _t = 1 - t
    r = []
    X = len(arr)
    if X==1:
        plt(*arr[0])
    else:
        for i in range(X-1):
            co1, co2 = arr[i], arr[i+1]
            x1, y1 = co1
            x2, y2 = co2
            x = x1 * t + x2 * (1-t)
            y = y1 * t + y2 * (1-t)
            r.append([x, y])
        bezier(r, t)
        
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('SDL Bezier curve demo -- tangent ver.')
dots = []
# The dots are here: [Starting, support for the before, support for the next, latest?]
bufferx = 0
buffery = 0

adding = True
index1 = -1
index2 = -1
clock = pygame.time.Clock()
while True:
    haschange = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            haschange = True
            if event.key == pygame.K_c:
                dots = []
                clear()
                lastx = 0
                lasty = 0
            elif event.key == pygame.K_g:
                if len(dots) > 1:
                    for i in range(len(dots)-1):
                        lastx = lasty = 0
                        pair1 = dots[i]
                        pair2 = dots[i+1]
                        s1 = pair1[0]
                        s2 = pair2[0]
                        m1 = pair1[2]
                        m2 = pair2[1]
                        k = 0
                        while k <= 1:
                            bezier([s1, m1, m2, s2], k)
                            k += ACCURACY
                        lastx = lasty = 0
                        dots[i][3] = True
                  
                lastx = lasty = 0
            elif event.key == pygame.K_p:
                dots = []
            elif event.key == pygame.K_e:
                clear()
                for d in dots:
                    d[3] = False
            elif event.key == pygame.K_d:
                try:
                    del dots[index1]
                except IndexError:
                    pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            haschange = True
            x, y = pygame.mouse.get_pos()
            for d in range(len(dots)):
                for i in range(3):
                    xp, yp = dots[d][i]
                    if abs(xp-x) <= 5 and abs(yp-y) <= 5:
                        index1 = d
                        index2 = i
                        adding = False
                        break
            
            bufferx = x
            buffery = y
        elif event.type == pygame.MOUSEBUTTONUP:
            haschange = True
            clear()
            x, y = pygame.mouse.get_pos()
            if adding:
                
                co1 = [x, y]
                delta1 = x - bufferx
                delta2 = y - buffery
                co2 = [bufferx - delta1, buffery - delta2]
                index1 = len(dots)
                dots.append([[bufferx, buffery], co1, co2, False])
            else:
                d = index1
                i = index2
                dots[d][3] = False
                if d > 0:
                    dots[d-1][3] = False
                if i == 0:
                    delta1 = x - dots[d][0][0]
                    delta2 = y - dots[d][0][1]
                    dots[d][0][0] += delta1
                    dots[d][0][1] += delta2
                    dots[d][1][0] += delta1
                    dots[d][1][1] += delta2
                    dots[d][2][0] += delta1
                    dots[d][2][1] += delta2
                else:
                    co1 = [x, y]
                    delta1 = x - dots[d][0][0]
                    delta2 = y - dots[d][0][1]
                    co2 = [dots[d][0][0] - delta1, dots[d][0][1] - delta2]
                    dots[d][1] = co1
                    dots[d][2] = co2
                adding = True
                    
    
    # BEGIN SECTION
    if haschange:
        if len(dots) > 1:
            for i in range(len(dots)-1):
                lastx = lasty = 0
                pair1 = dots[i]
                pair2 = dots[i+1]
                s1 = pair1[0]
                s2 = pair2[0]
                m1 = pair1[2]
                m2 = pair2[1]
                # if dots[i][3] == True:
                #     continue
                k = 0
                while k <= 1:
                    bezier([s1, m1, m2, s2], k)
                    k += ACCURACY
                lastx = lasty = 0
                dots[i][3] = True
                      
        lastx = lasty = 0
    # END SECTION
    screen.blit(BUFFER_SURFACE, (0, 0))
    for d in dots:
        pygame.draw.circle(screen, (0, 255, 0), d[0], 5)
        pygame.draw.aaline(screen, (255, 255, 0), d[2], d[1])
        pygame.draw.circle(screen, (0, 0, 255), d[1], 5)
        pygame.draw.circle(screen, (255, 0, 0), d[2], 5)
        
    
    pygame.display.update()
    clock.tick(30)


    
