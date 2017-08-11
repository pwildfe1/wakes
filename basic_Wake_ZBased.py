import rhinoscriptsyntax as rs
import math as m

def vecRotate(vec,ang,axis):
    cos = m.cos(m.pi/180*ang)
    sin = m.sin(m.pi/180*ang)
    v = vec
    u = vecUnitize(axis)
    R1,R2,R3 = [] , [] , []
    c = 1-cos

    R1.append(cos+m.pow(u[0],2)*c)
    R1.append(u[0]*u[1]*c-u[2]*sin)
    R1.append(u[0]*u[2]*c+u[1]*sin)
    
    R2.append(u[1]*u[0]*c+u[2]*sin)
    R2.append(cos+m.pow(u[1],2)*c)
    R2.append(u[1]*u[2]*c-u[0]*sin)
    
    R3.append(u[2]*u[0]*c-u[1]*sin)
    R3.append(u[2]*u[1]*c+u[0]*sin)
    R3.append(cos+m.pow(u[2],2)*c)
    
    x = vecDot(v,R1)
    y = vecDot(v,R2)
    z = vecDot(v,R3)
    
    return [x,y,z]

def vecMag(vec):
    sum = 0    
    for i in range(len(vec)):
        sum = sum+m.pow(vec[i],2)
    sum = m.pow(sum,.5)
    return sum

def transpose(matrix):
    transpose = []    
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            transpose.append(matrix[j][i])
    return transpose

def vecUnitize(vec):
    mag = vecMag(vec)
    for i in range(len(vec)):
        vec[i] = vec[i]/mag
    return vec

def vecDot(v1,v2):
    sum = 0    
    for i in range(len(v1)):
        sum = v1[i]*v2[i] + sum
    return sum

def vecAng(v1,v2):
    v1 = vecUnitize(v1)
    v2 = vecUnitize(v2)
    val = vecDot(v1,v2)
    ang = m.acos(val)
    return ang


def focalParabola(x,py):
    y = m.pow(x,2)/(2*py)+py
    return y

def Main():
    paths = rs.GetObjects("please select path curves",rs.filter.curve)
    srf = rs.GetObject("please select surface",rs.filter.surface)
    for n in range(len(paths)):
        crvs = []
        pts = []
        amnt = 10
        py=10
        r = 25
        nParam = 0
        for i in range(amnt):
            nParam = 1/amnt*i
            f = (nParam+1/amnt)
            param = rs.CurveParameter(paths[n],nParam)
            focal = rs.EvaluateCurve(paths[n],param)
            tan = rs.CurveTangent(paths[n],param)
            factor = abs(vecDot(tan,[0,0,1]))
            srfParam = rs.SurfaceClosestPoint(srf,focal)
            axis = rs.SurfaceNormal(srf,srfParam)
            r = 12*m.pow(f,.75)+10
            py = 40*m.pow(1-factor,2) + .01
            x = rs.VectorRotate(tan,90,axis)*(-r/2)
            xPt = rs.PointAdd(focal,x)
            print(r)
            for j in range(int(r)):
                x = rs.VectorRotate(tan,90,axis)
                xPt = rs.PointAdd(xPt,x)
                y = focalParabola((j-r/2),py)
                pt = rs.PointAdd(xPt,tan*y)
                srfParam = rs.SurfaceClosestPoint(srf,pt)
                axis = rs.SurfaceNormal(srf,srfParam)
                pts.append(pt)
            crv = rs.PullCurve(srf,rs.AddCurve(pts),True)
            crvs.append(crv)
            pts = []

Main()