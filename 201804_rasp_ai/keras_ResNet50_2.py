from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import sys, os, time, subprocess, pickle

model = ResNet50(weights='imagenet')
devnull = open('os.devnull', 'w')
ipaddr = subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()
commd = "http://"+ipaddr+":9000/?action=snapshot"

while True:
    subprocess.run(["wget", "-O", "photo.jpg", commd], stdout=devnull, stderr=subprocess.STDOUT)

    img_path = 'photo.jpg'
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    #print('Predicted:', decode_predictions(preds, top=3)[0])

    print('***********************************')
    for p in decode_predictions(preds, top=5)[0]:
            print("[Score] {} %, [Label] {}".format(round(p[2]*100, 2), p[1]))
    time.sleep(3)
    #count = 0
