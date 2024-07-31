# Save by engin on 2024_06_23-11.35.14; build 2019 2018_09_24-19.41.51 157541
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import math as mt
import csv
import os


csvPath = r"C:\Users\engin\Desktop"  # path storing the polygon data
os.chdir(csvPath)

ellipsoid_dict = {}

with open('esoid.csv') as fob:
    lines = csv.reader(fob)
    next(lines)
    for line in lines:
        intl = list(map(float, line))
        if not ellipsoid_dict.get(intl[0]):
            ellipsoid_dict[intl[0]] = []
        ellipsoid_dict[intl[0]].append(intl[1:])

for k in ellipsoid_dict.keys():
    ellips = ellipsoid_dict[k][0]
    
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -100.0), point2=(0.0, 100.0))
    mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].EllipseByCenterPerimeter(
        axisPoint1=(ellips[0], 0.0), axisPoint2=(0.0, ellips[1]), center=(0.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-ellips[0], 0.0), point2=
        (ellips[0], 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[5])
    mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models['Model-1'].sketches['__profile__'].geometry[3], entity2=
        mdb.models['Model-1'].sketches['__profile__'].geometry[5])
    mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
        addUndoState=False, entity1=
        mdb.models['Model-1'].sketches['__profile__'].vertices[3], entity2=
        mdb.models['Model-1'].sketches['__profile__'].geometry[3])
    mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(-45.0, 
        0.0), point2=(51.25, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry[6])
    mdb.models['Model-1'].sketches['__profile__'].autoTrimCurve(curve1=
        mdb.models['Model-1'].sketches['__profile__'].geometry[3], point1=(
        -0.0, ellips[1]))
    mdb.models['Model-1'].sketches['__profile__'].move(objectList=(
        mdb.models['Model-1'].sketches['__profile__'].geometry[2], 
        mdb.models['Model-1'].sketches['__profile__'].geometry[5], 
        mdb.models['Model-1'].sketches['__profile__'].geometry[6], 
        mdb.models['Model-1'].sketches['__profile__'].geometry[7]), vector=(ellips[6], ellips[7]))
    mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
        constructionGeometry=ON)
    mdb.models['Model-1'].sketches['__profile__'].assignCenterline(line=
        mdb.models['Model-1'].sketches['__profile__'].geometry[6])
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-{}'.format(int(k)), type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-1'].BaseSolidRevolve(angle=360.0, 
        flipRevolveDirection=OFF, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-{}-1'.format(int(k)), 
        part=mdb.models['Model-1'].parts['Part-{}'.format(int(k))])
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-{}-1'.format(int(k)), ), 
        vector=(0.0, 0.0, ellips[8]))
    mdb.models['Model-1'].rootAssembly.rotate(angle=ellips[3], axisDirection=(ellips[6], ellips[7], ellips[8]), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-{}-1'.format(int(k)), ))
    # Save by engin on 2024_06_24-13.29.08; build 2019 2018_09_24-19.41.51 157541



