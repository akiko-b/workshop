from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import sys

args = sys.argv

#学習済みモデルResNet50の読込
model = ResNet50(weights='imagenet')

#画像判定の為の関数
def predict(filename, featuresize):
    img = image.load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(preprocess_input(x))
    results = decode_predictions(preds, top=featuresize)[0]
    return results

#画像を判定
results = predict(args[1], 3)
for result in results:
    print("[Score] {} %, [Label] {}".format(round(result[2]*100, 2), result[1]))
