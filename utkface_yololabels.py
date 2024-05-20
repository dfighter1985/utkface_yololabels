'''
Copyright (C) 2024 dfighter1985

Creates Yolo style annotations for the UTKFace dataset with the following classes:

* male child
* female child
* male teenager
* female teenager
* adult male
* adult female
* senior male
* senior female

Age classes are the following:

* 0-12 child
* 13-17 teenager
* 18-64 adult
* 65-116 senior

Usage:
* Create a directory structure for the dataset:

    utkface_yolo
         |
         |
      training
      |      |
      |      |
    images  labels
    
* Copy images into the images directory.
* Copy the script to the training directory.
* Run the script from the training directory. Annotations will be created in the labels sub-directory.

* Create a data.yaml file in the utkface_yolo directory with contents similar to this:

train: D:\\projects\\yolo\\utkface_yolo\\training\\images
val: D:\\projects\\yolo\\utkface_yolo\\training\\images
nc: 8
names: [ 'male child', 'female child', 'male teenager', 'female teenager', 'adult male', 'adult female', 'senior male', 'senior female' ]

'''
import os
import shutil

ageClassNames = [ 'child', 'teenager', 'adult', 'senior' ]
genderName = [ 'male', 'female' ]

srcDir = 'images'
labelDir = 'labels'

yoloClassNames = [
    'male child',
    'female child',
    'male teenager',
    'female teenager',
    'adult male',
    'adult female',
    'senior male',
    'senior female'
]

yoloClassLut = [
    [ 0, 2, 4, 6 ],
    [ 1, 3, 5, 7 ]
]

def getYoloClass( gender, ageClass ):
    return yoloClassLut[ gender ][ ageClass ]
    
def writeLabelForFile( fileName, gender, ageClass ):
    yoloClass = getYoloClass( gender, ageClass )
    
    parts = fileName.split( '.' )    
    dstFile = labelDir + '/' + parts[ 0 ] + '.' + parts[ 1 ] + '.' + parts[ 2 ] + '.txt'    
    f = open( dstFile, 'w' )
    f.write( str( yoloClass ) + ' ' + '0.5 0.5 1.0 1.0' )
    f.close()
    
def writeClassesFile():
    f = open( labelDir + '/' + 'classes.txt', 'w' )
    
    for name in yoloClassNames:
        f.write( name + '\n' )
        
    f.close()


files = os.listdir( srcDir )

for file in files:
    parts = file.split( '_' )
    age = int( parts[ 0 ] )
    gender = int( parts[ 1 ] )
    
    ageClass = 0
        
    if age <= 12:
        ageClass = 0        
    elif age < 18:
        ageClass = 1
    elif age < 65:
        ageClass = 2
    else:
        ageClass = 3    
        
    writeLabelForFile( file, gender, ageClass )
        
    print( file + ' => ' + 'age:' + str( age ) + ',age class:' + ageClassNames[ ageClass ] + ',gender:' + genderName[ gender ] )
    
writeClassesFile()
