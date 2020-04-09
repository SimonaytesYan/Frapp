import dlib
from skimage import io
from scipy.spatial import distance
import os
data = []
with open(os.path.join("db", "number.txt"), "r") as f:
    for line in f:
        data.append(line)
n = int(data[0])
def update_db():
    data = []
    with open(os.path.join("db", "number.txt"), "r") as f:
        for line in f:
            data.append(line)
    n = int(data[0])
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    img = io.imread(os.path.join("db","IMG_{}.jpg".format(n-1)))
    dets = detector(img, 1)
    print(dets)
    for k, d in enumerate(dets):
        shape = sp(img, d)

    #Извлекаем дескриптор из лица
    face_descriptor1 = facerec.compute_face_descriptor(img, shape)
    #записываем дескриптор в файл
    f = open(os.path.join("db","IMG_{}.txt".format(n-1)), "w")
    for i in face_descriptor1:
        f.write(str(i))
        f.write("\n")

def what_difference():
    #извлекаем модели
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    
    #Второе лицо
    img = io.imread(os.path.join("db", "IMG_now.jpg"))

    dets_webcam = detector(img, 1)
    f = False
    for k, d in enumerate(dets_webcam):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        shape = sp(img, d)
        f = True
    if (f):
        face_descriptor2 = facerec.compute_face_descriptor(img, shape)
        a = []
        for i in range(n):
            face_descriptor1 = []
            with open(os.path.join("db","IMG_{}.txt".format(i)), "r") as f:
                for line in f:
                    face_descriptor1.append([float(x) for x in line.split()])
            #Рассчитываем Евклидово расстояние между двумя дексрипторами лиц
            a.append(float(distance.euclidean(face_descriptor1, face_descriptor2)))
        print(a)
        return a
    else:
        print("Face not found")
        return 0
    