import random
import pyglet
import math
from pyglet.graphics import draw
from pyglet.util import DecodeException
from pyglet.window import mouse
from pyglet import shapes, text, graphics, sprite
import dataclasses


window = pyglet.window.Window(1000,1000)
window.set_location(0,25)
numboids = 100
visrange = 75
boundmargin = 100
batch = graphics.Batch()
border = shapes.BorderedRectangle(boundmargin/2,boundmargin/2,window.width-boundmargin,window.height-boundmargin,border=1,color=(0,255,0))
boids=[]
# instance picture once
img = pyglet.image.load('./src/boid.png')
img.anchor_x = img.width // 2
img.anchor_y = img.height // 2

class boid:
    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.sprite = sprite.Sprite(img, x,y, batch=batch,subpixel=True)
        self.sprite.scale = 0.015
    def rotate(self):
        self.sprite.rotation = math.degrees(math.atan2(self.dx,self.dy))
    
    

#function for setting up initial boids
def drawboids():
    for _ in range(numboids):
        b=boid(random.random()*100+500,random.random()*100+500,random.random()*10-5,random.random()*10-5)
        boids.append(b)
    print("done")

# calculate distance between 2 boids
def boiddist(boid1,boid2):
    return math.sqrt(
        (boid1.sprite.x - boid2.sprite.x) * (boid1.sprite.x - boid2.sprite.x) +
        (boid1.sprite.y - boid2.sprite.y) * (boid1.sprite.y - boid2.sprite.y)
    )

# fly towards center of another boid in visual distance
def flytoboid(boid):
    centeringFactor = 0.005
    centerx = 0
    centery = 0
    numneighbors = 0
    for b in boids:
        if boiddist(boid, b) < visrange:
            centerx += b.sprite.x
            centery += b.sprite.y
            numneighbors += 1
    if numneighbors :
        centerx = centerx / numneighbors
        centery = centery / numneighbors

        boid.dx += (centerx - boid.sprite.x) * centeringFactor
        boid.dy += (centery - boid.sprite.y) * centeringFactor

# keep the boids seperate from eachother
def avoidothers(boid):
    mindist = 25
    avoidfac = 0.05
    movex = 0
    movey = 0
    for b in boids:
        if boid != b:
            if(boiddist(boid,b) < mindist):
                movex += boid.sprite.x - b.sprite.x
                movey += boid.sprite.y - b.sprite.y
    boid.dx += movex*avoidfac
    boid.dy += movey*avoidfac

# keeping the boids on the screen
def keepinbound(boid):
    margin = boundmargin
    turnfac = 3
    if(boid.sprite.x < margin):
        boid.dx += turnfac
    if(boid.sprite.x > window.width - margin):
        boid.dx -= turnfac
    if(boid.sprite.y < margin):
        boid.dy += turnfac
    if(boid.sprite.y > window.height - margin):
        boid.dy -= turnfac
    
# limiting the speed of the boids 
def limitspeed(boid):
    speedlimit = 15
    speed = math.sqrt(boid.dx * boid.dx + boid.dy * boid.dy)
    if(speed > speedlimit):
        boid.dx = (boid.dx / speed) * speedlimit
        boid.dy = (boid.dy / speed) * speedlimit

# keep the boids grouped and aligned
def matchvelocity(boid):
    matchfac = 0.05
    avgdx = 0
    avgdy = 0
    numneighbors = 0
    for b in boids:
        if (boiddist(boid,b) < visrange):
            avgdx += b.dx
            avgdy += b.dy
            numneighbors += 1
            
    avgdx = avgdx / numneighbors
    avgdy = avgdy / numneighbors
    boid.dx += (avgdx - boid.dx) * matchfac
    boid.dy += (avgdy - boid.dy) * matchfac
    
        
# main update function
def update(t):
    for b in boids:
        flytoboid(b)
        avoidothers(b)
        matchvelocity(b)
        limitspeed(b)
        keepinbound(b)
        b.sprite.x += b.dx
        b.sprite.y += b.dy
        b.rotate()
        
    window.clear()
    # border.draw()
    batch.draw()
    

drawboids()
pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()
