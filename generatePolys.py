import math, random, sys
from PIL import Image, ImageDraw

first_arg = sys.argv[1]
second_arg = sys.argv[2]
third_arg = sys.argv[3]
fourth_arg = sys.argv[4]
fifth_arg = sys.argv[5]
sixth_arg = sys.argv[6]

def generatePolygon(ctrX=first_arg, ctrY=second_arg, aveRadius=third_arg, irregularity=fourth_arg, spikeyness=fifth_arg, numVerts=sixth_arg) :
   irregularity = int(irregularity)
   ctrX = int(ctrX)
   ctrY = int(ctrY)
   aveRadius = int(aveRadius)
   spikeyness = float(spikeyness)
   numVerts = int(numVerts)
   
   irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
   spikeyness = clip( spikeyness, 0,1 ) * aveRadius
   
   # generate n angle steps
   angleSteps = []
   lower = (2*math.pi / numVerts) - irregularity
   upper = (2*math.pi / numVerts) + irregularity
   sum = 0
   for i in range(numVerts) :
       tmp = random.uniform(lower, upper)
       angleSteps.append( tmp )
       sum = sum + tmp
       
   # normalize the steps so that point 0 and point n+1 are the same
   k = sum / (2*math.pi)
   for i in range(numVerts) :
       angleSteps[i] = angleSteps[i] / k

   # now generate the points
   points = []
   angle = random.uniform(0, 2*math.pi)
   for i in range(numVerts) :
       r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
       x = ctrX + r_i*math.cos(angle)
       y = ctrY + r_i*math.sin(angle)
       points.append( (int(x),int(y)) )

       angle = angle + angleSteps[i]

   print("Points: {}" .format(points))

   return points

def draw(points):
   black = (0,0,0)
   white=(255,255,255)
   im = Image.new('RGB', (500, 500), white)
   imPxAccess = im.load()
   draw = ImageDraw.Draw(im)
   tupVerts = list(map(tuple,points))
   
   # either use .polygon(), if you want to fill the area with a solid colour
   #draw.polygon( tupVerts, outline=black,fill=white )
   
   # or .line() if you want to control the line thickness, or use both methods together!
   draw.line( tupVerts+[tupVerts[0]], width=1, fill=black )
   
   im.show()
   
   return
   
def clip(x, min, max) :
   if( min > max ) :  return x    
   elif( x < min ) :  return min
   elif( x > max ) :  return max
   else :             return x
   
if __name__ == "__main__":
   generatePolygon()