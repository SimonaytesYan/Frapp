import dlib
from skimage import io
from scipy.spatial import distance
import os
def update_db(n, path):
        
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    img = io.imread(path)
    io.imsave(os.path.join("db","IMG_{}.jpg".format(n-1)), img)
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

def what_difference(n):
    #извлекаем модели
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    face_descriptor1 = []
    with open(os.path.join("db","IMG_{}.txt".format(n)), "r") as f:
        for line in f:
            face_descriptor1.append([float(x) for x in line.split()])
    #Второе лицо
    img = io.imread("IMG_now.jpg")
    win2 = dlib.image_window()
    win2.clear_overlay()
    win2.set_image(img)
    dets_webcam = detector(img, 1)
    f = False
    for k, d in enumerate(dets_webcam):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        shape = sp(img, d)
        win2.clear_overlay()
        win2.add_overlay(d)
        win2.add_overlay(shape)
        f = True
    if (f):
        face_descriptor2 = facerec.compute_face_descriptor(img, shape)

        #Рассчитываем Евклидово расстояние между двумя дексрипторами лиц
        a = distance.euclidean(face_descriptor1, face_descriptor2)
        print(a)
        return a
    else:
        return -1
    