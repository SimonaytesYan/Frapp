import dlib
from skimage import io
from scipy.spatial import distance

#извлекаем модели
def what_difference(n):
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    img = io.imread('db\\IMG_{}.jpg'.format(n))

    #Вывод фотографии
    win1 = dlib.image_window()
    win1.clear_overlay()
    win1.set_image(img)

    #Находим лицо на фотографии
    dets = detector(img, 1)
    print(dets)
    for k, d in enumerate(dets):
        
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        shape = sp(img, d)
        win1.clear_overlay()
        win1.add_overlay(d)
        win1.add_overlay(shape)

    #Извлекаем дескриптор из лица
    face_descriptor1 = facerec.compute_face_descriptor(img, shape)

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
        print("Лицо на изображении не найдено")
        a = -1
        return a
    