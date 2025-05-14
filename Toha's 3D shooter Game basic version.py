from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluLookAt,gluPerspective

import random

import math
import OpenGL.GLUT as GLUT


font = GLUT.GLUT_BITMAP_8_BY_13

tempi=0
sx=500
sy=random.randint(50,450)
score = 0
invisiblescore = -1
bossL_or_R = random.randint(0,10)
speed_multiplier = 0.5

game_state = 'Playing'
shooterlist = [[250,70,9]]

bulletx,bullety=-1,-1*speed_multiplier
laserx,lasery=-1,-1*speed_multiplier
heartx,hearty=random.randint(50,450),470
invisiblex,invisibley=random.randint(50,250),470
fiveopponents,shooter,bulletcenter,bulletstate,opponentarea,missed_count,bulletmiss,laserpointlist,enemybulletlist=[],[],[],[],[],[],[],[],[]

heartflag=True
invisibleflag = False
bullet1flag = False

laserflag=False

bossflag = False
bosslist = [250,400,40]
bossbulletx,bossbullety = -1,-1
bosshealth=50
myhealthboss=9
bossbulletflag = [False,False,False,False,False]
bossbulletlist=[[bosslist[0]-90,bosslist[1]],[bosslist[0]-50,bosslist[1]],[bosslist[0],bosslist[1]],[bosslist[0]+50,bosslist[1]],[bosslist[0]+90,bosslist[1]]]

enemybulletflag=[False,False,False,False,False]

camera_mode = 'third'  # 'first' or 'third'
camera_angle = 0.0     # Angle for rotating left/right
camera_distance = 350  # Distance for third-person camera



starlist = []
for i in range(300):
    starlist.append([random.randint(0,500),random.randint(0,500)])
enemylist=[]
enemyarea=[]
l = [-1,-1,-1,-1,-1]
for i in range(5):
  enemyarea.append(l)
a = 0
b= a+80
for i in range(5):
    randomx = random.randint(a,b)
    randomy = random.randint(300,420)
    randomshape = random.choice(['Box','Cir','Trig'])
    a += 100
    b = a+80
    enemylist.append([randomx,randomy,3,randomshape,randomx,randomy])

enemylistafterboss = [-100,-100,3,'Cir',-100,-100]



def draw_points(x, y,ps=1):
    glPointSize(ps)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def midpoint_circle(cx, cy, r,half=False,heart=False):
    d = 1 - r
    x = 0
    y = r
    if half == True and heart== False:
        draw_points(x + cx, y + cy)
        draw_points(-x + cx, y + cy)

    if heart == True and half== False:
        draw_points(x + cx, y + cy)
        draw_points(y + cx, x + cy)
        draw_points(-x + cx, y + cy)
        draw_points(-y + cx, x + cy)

    if heart == False and half== False:
        draw_points(x + cx, y + cy)
        draw_points(-x + cx, y + cy)
        draw_points(-y + cx, x + cy)
        draw_points(-y + cx, -x + cy)
        draw_points(-x + cx, -y + cy)
        draw_points(x + cx, -y + cy)
        draw_points(y + cx, -x + cy)
        draw_points(y + cx, x + cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3 # e
            x += 1
        else:
            d = d + 2 * x - 2 * y + 5  #se
            x += 1
            y -= 1
        
        if half == True and heart== False:
            draw_points(x + cx, y + cy)
            draw_points(-x + cx, y + cy)

        if heart == True and half== False:
            draw_points(x + cx, y + cy)
            draw_points(y + cx, x + cy)
            draw_points(-x + cx, y + cy)
            draw_points(-y + cx, x + cy)
        
        if heart == False and half== False:
            draw_points(x + cx, y + cy)
            draw_points(-x + cx, y + cy)
            draw_points(-y + cx, x + cy)
            draw_points(-y + cx, -x + cy)
            draw_points(-x + cx, -y + cy)
            draw_points(x + cx, -y + cy)
            draw_points(y + cx, -x + cy)
            draw_points(y + cx, x + cy)

def midpoint(x1,y1,x2,y2):
    zone = myzone(x1, y1, x2, y2)
    x1, y1 = n_to_zero(x1,y1,zone)
    x2, y2 = n_to_zero(x2, y2,zone)
    dx = x2 - x1
    dy = y2 - y1
    dinit = 2 * dy - dx
    dne = 2 * dy - 2 * dx
    de = 2 * dy
    for i in range(int(x1), int(x2)):
        a, b = zero_to_n(x1,y1,zone)
        if dinit >= 0:
            dinit = dinit + dne
            draw_points(a, b)
            x1 += 1
            y1 += 1
        else:
            dinit = dinit + de
            draw_points(a, b)
            x1 += 1

def myzone(x1, y1, x2, y2):
    dx = x2-x1
    dy = y2-y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6


def zero_to_n(x,y,zone):
    if zone == 0:
        return x,y
    if zone == 1:
        return y,x
    if zone == 2:
        return -y,x
    if zone == 3:
        return -x,y
    if zone == 4:
        return -x,-y
    if zone == 5:
        return -y,-x  
    if zone == 6:
        return y, -x
    if zone == 7:
        return x,-y
    
def n_to_zero(x,y,zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def exit_sign():
    glColor3f(1,0,0)
    midpoint(470, 470, 490, 490)
    midpoint(470, 490, 490, 470)

def pause_sign():
    glColor3f(1,1,0)
    midpoint(245, 470, 245, 490)
    midpoint(255, 470, 255, 490)

def resume_sign():
    glColor3f(1,1,0)
    midpoint(245, 470, 245, 490)
    midpoint(245, 470, 265, 480)
    midpoint(245, 490, 265, 480)

def back_sign():
    glColor3f(0,1,1)
    midpoint(10, 480, 40, 480)
    midpoint(10, 480, 25, 490)
    midpoint(10, 480, 25, 470)



def specialKeyListener(key, x, y):
    global shooter,game_state,laserpointlist,laserflag
    if key == GLUT_KEY_LEFT and game_state == 'Playing':
        laserflag=False
        shooterlist[0][0] -= 20
        if shooterlist[0][0] < 20:
          shooterlist[0][0] = 20
       
    elif key == GLUT_KEY_RIGHT and game_state == 'Playing':
        laserflag=False
        shooterlist[0][0] += 20
        if shooterlist[0][0] >480:
          shooterlist[0][0] = 480
       
    elif key == GLUT_KEY_UP and game_state == 'Playing':
        laserflag=False
        shooterlist[0][1] += 20
        if shooterlist[0][1] > 200:
          shooterlist[0][1] = 200
        
    elif key == GLUT_KEY_DOWN and game_state == 'Playing':
        laserflag=False
        shooterlist[0][1] -= 20
        if shooterlist[0][1] < 54:
          shooterlist[0][1] = 54
        

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global game_state, score,fiveopponents,shooter,bulletcenter,bulletstate,opponentarea,missed_count,bulletmiss
    actualx = x
    actualy = 500 - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 470 <= actualx <= 490 and 470 <= actualy <= 490:  # Exit icon
            glutLeaveMainLoop()




def keyboardListener(key, x, y):
    global bullet1flag,bulletx,bullety,shooterlist,laserflag,laserx,lasery,laserpointlist,enemybulletflag,bossflag,bossbulletflag,bosslist
    global bossbulletlist
    global speed_multiplier
    global camera_mode, camera_angle
    
    if key == b'v':
        camera_mode = 'first' if camera_mode == 'third' else 'third'
    elif key == b'j':  # Rotate Left
        camera_angle -= 5
    elif key == b'k':  # Rotate Right
        camera_angle += 5
    if key==b' ' and game_state == 'Playing' and bullet1flag == False:
        bulletx,bullety = shooterlist[0][0], shooterlist[0][1] + 1
        bullet1flag = True
    
    
    elif key==b'l' and game_state == 'Playing' and laserflag == False:
        laserx,lasery=shooterlist[0][0], shooterlist[0][1] + 1
        laserflag=True
        bullet1flag=True
    elif key==b'l' and game_state == 'Playing' and laserflag == True:
        laserflag=False
        bullet1flag=False
    
    if bossflag == False:
        if key==b'1' and game_state == 'Playing' and enemybulletflag[0] == False:
            enemybulletflag[0] = True
        elif key==b'2' and game_state == 'Playing' and enemybulletflag[1] == False:
            enemybulletflag[1] = True

        elif key==b'3' and game_state == 'Playing' and enemybulletflag[2] == False:
            enemybulletflag[2] = True

        elif key==b'4' and game_state == 'Playing' and enemybulletflag[3] == False:
            enemybulletflag[3] = True

        elif key==b'5' and game_state == 'Playing' and enemybulletflag[4] == False:
            enemybulletflag[4] = True
        elif key == b'+':
            speed_multiplier = min(speed_multiplier + 0.1, 2.0)
        elif key == b'-':
            speed_multiplier = max(speed_multiplier - 0.1, 0.1)
        elif key == b'r':
            restart_game()
    else:
        if  key==b'a'and game_state == 'Playing':
            if bosslist[0]>=105:
                bosslist[0]=bosslist[0]-10
                for i in range(5):
                    bossbulletlist[i][0] -= 10

        if  key==b'd'and game_state == 'Playing':
            if bosslist[0]<=395:
                bosslist[0]=bosslist[0]+10
                for i in range(5):
                    bossbulletlist[i][0] += 10
            
        if key==b'1' and game_state == 'Playing' and bossbulletflag[0] == False:
            
            bossbulletflag[0] = True
            
        elif key==b'2' and game_state == 'Playing' and bossbulletflag[1] == False:
            bossbulletflag[1] = True

        elif key==b'3' and game_state == 'Playing' and bossbulletflag[2] == False:
            bossbulletflag[2] = True

        elif key==b'4' and game_state == 'Playing' and bossbulletflag[3] == False:
            bossbulletflag[3] = True

        elif key==b'5' and game_state == 'Playing' and bossbulletflag[4] == False:
            bossbulletflag[4] = True

        elif key == b'+':
            speed_multiplier = min(speed_multiplier + 0.1, 2.0)
        elif key == b'-':
            speed_multiplier = max(speed_multiplier - 0.1, 0.1)
        elif key == b'r':
            restart_game()

def restart_game():
    global shooterlist, bulletx, bullety, bullet1flag, laserflag,speed_multiplier
    global enemylist, enemybulletflag, score, game_state
    global heartx, hearty, heartflag, invisiblex, invisibley, invisibleflag, invisiblescore
    global bossflag, bosslist, bossbulletlist, bossbulletflag, bossbulletx, bossbullety 
    global starlist, sx, sy
    
    
    # Reset shooter
    shooterlist = [[250, 70, 9]]
    bulletx,bullety = -1,-1*speed_multiplier
    bullet1flag = False
    laserflag = False

    # Reset enemies
    enemylist = []
    enemybulletflag = []
    for i in range(5):
        ex = random.randint(i*100, (i+1)*100)
        ey = random.randint(300, 420)
        shape = random.choice(['Box', 'Cir', 'Trig'])
        enemylist.append([ex, ey, 3, shape, ex, ey])
        enemybulletflag.append(False)

    score = 0
    game_state = 'Playing'

    # Reset stars
    starlist = [[random.randint(0, 500), random.randint(0, 500)] for _ in range(100)]
    sx = 0
    sy = 0

    # Reset heart and invisibility
    heartx = random.randint(50, 450)
    hearty = 470
    heartflag = True

    invisiblex = random.randint(50, 250)
    invisibley = 470
    invisibleflag = False
    invisiblescore = -1

    # Reset boss
    bossflag = False
    bosslist = [250, 400, 20]
    bossbulletlist = []
    bossbulletflag = []
    for _ in range(5):
        bossbulletlist.append([bosslist[0], bosslist[1]])
        bossbulletflag.append(False)
    

    print("Game restarted")
    

def shooter(x, y, health, mode='normal'):
    glPushMatrix()
    glTranslatef(x, y, 0)
    if mode == 'invisible':
        glColor4f(1.0, 1.0, 1.0, 0.3)
    else:
        glColor3f(0.0, 1.0, 0.0)
    glutSolidCube(20)
    glPopMatrix()

def bullet(x, y, r, g, b):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(r, g, b)
    glutSolidSphere(5, 10, 10)  # Use a small sphere for bullet
    glPopMatrix()

def enemy(x, y, health, shape):
    glPushMatrix()
    glTranslatef(x, y, 0)

    if shape == 'Box':
        glColor3f(1, 0, 0)
        glScalef(1.5, 1.5, 1.5)
        glutSolidCube(20)
    elif shape == 'Cir':
        glColor3f(0, 1, 0)
        glutSolidSphere(10, 20, 20)
    elif shape == 'Trig':
        glColor3f(0, 0, 1)
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(10, 20, 20, 20)
    
    glPopMatrix()

def boss(x, y, health):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(0.5, 0, 0.5)  # Purple boss
    glScalef(3, 3, 3)
    glutSolidCube(30)
    glPopMatrix()



    #outer body
    midpoint(x-100,y,x+100,y)
    midpoint(x-80,y+40,x+80,y+40)
    midpoint(x-100,y,x-80,y+40)
    midpoint(x+100,y,x+80,y+40)

    #face
    
    midpoint(x-20,y+5,x+20,y+5)
    midpoint_circle(x-60,y+25,8)
    midpoint_circle(x+60,y+25,8)
    midpoint_circle(x-60,y+25,2)
    midpoint_circle(x+60,y+25,2)
    midpoint_circle(x,y-50,70,True)

    #sparks
    midpoint(x,y-10,x-10,y)
    midpoint(x,y-10,x+10,y)
    midpoint(x-50,y-10,x-50-10,y)
    midpoint(x-50,y-10,x-50+10,y)
    midpoint(x-90,y-10,x-90-10,y)
    midpoint(x-90,y-10,x-90+10,y)
    midpoint(x+50,y-10,x+50-10,y)
    midpoint(x+50,y-10,x+50+10,y)
    midpoint(x+90,y-10,x+90-10,y)
    midpoint(x+90,y-10,x+90+10,y)

 
def bossbullet(x, y, damage):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(1, 0.2, 0)
    glRotatef(90, 1, 0, 0)
    glutSolidCone(5, 15, 10, 10)
    glPopMatrix()

def drawLaser():
    global laserx, lasery
    glPushMatrix()
    glTranslatef(laserx, lasery, 0)
    glColor3f(1, 0, 0)
    glScalef(1, 200, 1)  # Long vertical beam
    glutSolidCube(1.5)
    glPopMatrix()

    

def drawstar(list1):
    glColor3f(1,1,1)
    for i in list1:
        draw_points(i[0],i[1])

def drawheart(x, y):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(1, 0, 0)
    glutSolidSphere(8, 20, 20)
    glPopMatrix()


def drawinvisible(x, y):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(0, 1, 1)  # Cyan
    glutSolidSphere(7, 20, 20)
    glPopMatrix()



def drawshootstar(sx,sy):
    glColor3f(0.5,0.5,0.5)
    draw_points(sx,sy,15)
    glColor3f(1,1,1)
    draw_points(sx,sy,8)

def checkcolission():
    global bulletx,bullety, enemylist, enemyarea,bullet1flag,laserx,lasery,tempi
    if bullet1flag==True:
        for i in range(len(enemyarea)):      
            if enemyarea[i][0] <= bulletx  <= enemyarea[i][1] and enemyarea[i][2] <= bullety <= enemyarea[i][3]:
                return i
            elif enemyarea[i][0] <= bulletx-15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety <= enemyarea[i][3]:
                return i
            elif enemyarea[i][0] <= bulletx+15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety <= enemyarea[i][3]:
                return i
            elif enemyarea[i][0] <= bulletx-15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety+30 <= enemyarea[i][3]:
                return i
            elif enemyarea[i][0] <= bulletx+15 <= enemyarea[i][1] and enemyarea[i][2] <= bullety+30 <= enemyarea[i][3]:
                return i
            elif enemyarea[i][0] <= bulletx <= enemyarea[i][1] and enemyarea[i][2] <= bullety+30 <= enemyarea[i][3]:
                return i
    elif laserflag==True:
            for i in range(len(enemyarea)):      
                if enemyarea[i][0] < laserx < enemyarea[i][1]:

                    return str(i)   

    return None


 
def checkclash():
    global  enemyarea,shooterlist
    for i in range(len(enemyarea)):     
        if enemyarea[i][0] <=  shooterlist[0][0] <= enemyarea[i][1] and enemyarea[i][2] <= shooterlist[0][1] <= enemyarea[i][3]:
            return i  
        if enemyarea[i][0] <=  shooterlist[0][0]-20 <= enemyarea[i][1] and enemyarea[i][2] <= shooterlist[0][1]-40 <= enemyarea[i][3]:
            return i  
        if enemyarea[i][0] <=  shooterlist[0][0]+20 <= enemyarea[i][1] and enemyarea[i][2] <= shooterlist[0][1]-40 <= enemyarea[i][3]:
            return i                     

    return None


def afterbossanimate(): #after boss appears this will be the animate function  #stanley
    global bosslist,bullet1flag,bulletx,bullety,bossL_or_R,bossbulletlist,shooterlist,myhealthboss

    #-------------------------------------------------------------------- boss to me
    if bullet1flag == True:
        if bosslist[0] - 100 <= bulletx  <= bosslist[0] + 100 and bosslist[1] <= bullety <= bosslist[1] +40:   #boss hit by my bullet
            bullet1flag = False
            bosslist[2] -= 2
    elif laserflag==True:     
                if bosslist[0] - 100 <= laserx <= bosslist[0] + 100:
                    bosslist[2] -= 1          #boss hit by my laser
                   
#-------------------------------------------------------------------- me to boss
    for i in range(len(bossbulletflag)):   
        if bossbulletflag[i] ==True:
            
            bossbulletlist[i][1]=bossbulletlist[i][1]-10

    for i in range(5):
        if  bossbulletflag[i] == True:
            if bossbulletlist[i][1] < 0:
                bossbulletlist[i][1] = bosslist[1]
                bossbulletflag[i] = False
            
            if shooterlist[0][0] - 20 <= bossbulletlist[i][0]  <= shooterlist[0][0] + 20 and shooterlist[0][1] -40 <= bossbulletlist[i][1] <= shooterlist[0][1] :
                bossbulletflag[i] = False
                bossbulletlist[i][1] = bosslist[1]



                shooterlist[0][2] = shooterlist[0][2]-3
               
 

            
def animate():
    global shooterlist,starlist,bulletx,bullety,bullet1flag,enemybulletflag,enemylist,enemybulletlist,enemyarea,score,laserflag
    global hearty,heartx,heartflag,invisiblex,invisibley,invisibleflag, invisiblescore,bossflag,bossbulletlist
    global tempi,sx,sy
    if score == 10:
        score=0
        bossflag = True
        shooterlist[0][2]=9

#------------------------------------------------------------  Enemny x displacement
    if bossflag==False:         #tahura
        a = random.randint(1,2)
        if a==1:
            for i in range(len(enemylist)):
                for j in range(50):
                    disr=enemylist[i][0]+0.02* speed_multiplier
                    if disr+15 >=500:
                        pass
                    else:
                        enemylist[i][0] +=0.02* speed_multiplier
        elif a==2:
            for i in range(len(enemylist)):
                for j in range(50):
                    disl=enemylist[i][0]-0.02* speed_multiplier
                    if disl-15<=0:
                        pass
                    else:
                        enemylist[i][0] -=0.02* speed_multiplier
#-------------------------------------------------------------------------  new enemy after y=0
        for i in range(len(enemylist)):
            enemylist[i][1]-=0.5* speed_multiplier
            enemylist[i][5]-=0.5* speed_multiplier
            enemylist[i][4] = enemylist[i][0]
            if enemylist[i][1] + 40 < 0:
                randomx = random.randint(i*100,(i*100)+80)
                randomy = random.randint(300,420)
                randomshape = random.choice(['Box','Cir','Trig'])
                enemylist[i]=[randomx,randomy,3,randomshape,randomx,randomy]
                
#--------------------------------------------------------------------------- Enemy bullet
        for i in range(len(enemybulletflag)):
            if enemybulletflag[i] == True:
                enemylist[i][5] -= 20* speed_multiplier
                if shooterlist[0][0] - 20 <= enemylist[i][4] <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= enemylist[i][5] <= shooterlist[0][1]:
                    if invisibleflag == False:
                        shooterlist[0][2] -= 1
                        
            if enemylist[i][5] < 0:
                enemylist[i][5] = enemylist[i][1]
                enemybulletflag[i] =False

        for i in range(len(enemyarea)):
            enemyarea[i] = [enemylist[i][0] -15,enemylist[i][0] +15,enemylist[i][1],enemylist[i][1] +30]


        idx = checkcolission()
    
        if idx != None:
            if type(idx)==str:
                idx=int(idx)
                enemylist[idx][2] -= 0.1
            else:
                enemylist[idx][2] -= 1
                bullet1flag=False 
            if enemylist[idx][2]<=0:
                laserflag=False
                randomx = random.randint(idx*100,(idx*100)+80)
                randomy = random.randint(300,420)
                randomshape = random.choice(['Box','Cir','Trig'])
                enemylist[idx]=[randomx,randomy,3,randomshape,randomx,randomy]      #scored
                bulletx,bullety = -1, -1
                score += 1
                print("SCORE: ",score)
                
            
        clash = checkclash()
        if clash != None:
            shooterlist[0][2] -= 3
            randomx = random.randint(clash*100,(clash*100)+80)
            randomy = random.randint(300,420)
            randomshape = random.choice(['Box','Cir','Trig'])
            enemylist[clash]=[randomx,randomy,3,randomshape,randomx,randomy]      #scored
    else:
        afterbossanimate()
        

    #-------------------------------------------------------------------------------------------------------------------------------------------------
    for i in starlist:
        i[1] -= 2
        if i[1] == 0:
            starlist.append([random.randint(0,500),500])
        elif i[1] == -1:
            starlist.append([random.randint(0,500),500])
    
    if bullet1flag == True:
        bullety += 40
    if bullety >500:
        bullet1flag = False
 
    sx=(sx-3)%500
    sy=(sy-3)%500

    hearty=hearty-2*speed_multiplier

    if hearty+20<0:
        #heartflag=True #ignore
        hearty=470
        heartx=random.randint(50,450)

    if  shooterlist[0][2]<=6:
        if  shooterlist[0][0] - 20 <= heartx <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= hearty <= shooterlist[0][1]:
            shooterlist[0][2]+=3
            heartflag=True
            hearty=470
            heartx=random.randint(50,450)

    if bossflag == False:
        invisibley = (invisibley- 1)%500
        invisiblex = (invisiblex+ 3)%500
    if bossflag==True:
        invisibley=1000000
        invisibley=1000000
        

    if invisibleflag == False:

        if  shooterlist[0][0] - 20 <= invisiblex <= shooterlist[0][0] + 20 and shooterlist[0][1] - 40 <= invisibley <= shooterlist[0][1]:
            invisibleflag = True
            invisiblescore = score
            invisiblex,invisibley = random.randint(50,250),470

    if invisiblescore != score:
        invisibleflag = False
        invisiblescore = -1

    glutPostRedisplay()


def setCamera():
    global camera_mode, camera_angle, camera_distance
    if camera_mode == 'third':
        # Orbiting third-person camera
        camX = 250 + camera_distance * math.sin(math.radians(camera_angle))
        camZ = 250 + camera_distance * math.cos(math.radians(camera_angle))
        gluLookAt(camX, 250, camZ,
                  250, 250, 0,
                  0, 1, 0)
    else:
        # First-person camera from shooter’s perspective
        for i in shooterlist:
            eyeX = i[0]
            eyeY = i[1]
            eyeZ = i[2] + 20  # camera height
            dirX = eyeX + 100 * math.sin(math.radians(camera_angle))
            dirZ = eyeZ + 100 * math.cos(math.radians(camera_angle))
            gluLookAt(eyeX, eyeY + 30, eyeZ,
                      dirX, eyeY + 30, dirZ,
                      0, 1, 0)

def showScreen():
    global game_state, shooterlist, bossflag, enemylist, starlist, bulletx, bullety, enemybulletflag, enemylist, laserx, lasery, laserpointlist, laserflag, enemybulletlist
    global heartx, hearty, heartflag, invisiblex, invisibley, invisibleflag, bosslist, bossbulletx, bossbullety, bossbulletflag, bossbulletlist
    global sx, sy, score, font

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    setupLighting()

    # Set Camera Mode
    setCamera()

    iterate()
    drawstar(starlist)
    exit_sign()

    for i in shooterlist:
        if i[2] == 0:
            game_state = 'Game Over'
        if invisibleflag:
            shooter(i[0], i[1], i[2], 'invisible')
        else:
            shooter(i[0], i[1], i[2])

    if not bossflag:
        for i in enemylist[:]:
            if i[2] == 0:
                enemylist.remove(i)
            enemy(i[0], i[1], i[2], i[3])

    for i in range(len(enemybulletflag)):
        if enemybulletflag[i]:
            bullet(enemylist[i][4], enemylist[i][5], 1, 0.5, 0.4)

    if bossflag:
        boss(bosslist[0], bosslist[1], bosslist[2])
        for i in range(len(bossbulletflag)):
            if bossbulletflag[i]:
                bossbullet(bossbulletlist[i][0], bossbulletlist[i][1], 5)

        if bosslist[2] <= 0:
            game_state = 'Game Over'

    if bullet1flag and not laserflag:
        bullet(bulletx, bullety, 1, 0.5, 0)

    if laserflag:
        drawLaser()

    if heartflag:
        drawheart(heartx, hearty)
        
    drawinvisible(invisiblex, invisibley)

    # Score Display
    y_pos= 480
    instructions=[f"Score: {score}",
    f"Health: {shooterlist[0][2]}",
    f"Boss Health: {bosslist[2]}",
    "Press 'Space' to Shoot",
    "'L' to Laser",
    "'R' to Restart",
    "'J' to Move the plane Left",
    "'K' to Move the plane Right",
    "'V' for first person camera",
    "'Down Arrow' to Move player Backward",
    "'Up Arrow' to Move player Forward",
    "'Right Arrow' to Move player Right",
    "'Left Arrow' to Move player Left",
    "'D' to Move BossEnemy Right",
    "'A' to Move BossEnemy Left",
    "'1,2,3,4,5' to shoot enemy(boss) bullets",]
    glColor3f(.5, .5, .5) if not bossflag else glColor3f(0.5, 0.5, 0.5)
    for instruction in instructions:
        glRasterPos2f(10, y_pos)
        for char in instruction:
            glutBitmapCharacter(font, ctypes.c_int(ord(char)))
        y_pos -= 20  # Move down for the next line
        

    if game_state == 'Game Over':
        glColor3f(1, 0, 0)
        glRasterPos2f(200, 250)
        for char in "Game Over":
            glutBitmapCharacter(font, ctypes.c_int(ord(char)))

        glColor3f(1, 1, 1)
        glRasterPos2f(200, 200)
        win_str = "You Win!" if bosslist[2] <= 0 else "You Lose!"
        for char in win_str:
            glutBitmapCharacter(font, ctypes.c_int(ord(char)))

    glutSwapBuffers()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    

def setupLighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    light_position = [1.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    ambient_light = [0.2, 0.2, 0.2, 1.0]
    diffuse_light = [0.8, 0.8, 0.8, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Game")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glEnable(GL_DEPTH_TEST)
glClearColor(0.0, 0.0, 0.0, 1.0)
glutMainLoop()
