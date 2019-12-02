# -*- coding: utf-8 -*- 
import numpy as np
import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.models import model_from_json
k = 0
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
print("Loaded saved model from disk.")
 
# evaluate loaded model on test data
def identify_number(image):
    cv2.imwrite('./tmp'+str(k)+'.jpg' ,image)
    image_resize = cv2.resize(image, (28,28))    
    image_resize_2 = image_resize.reshape(1,1,28,28)   
    loaded_model_pred = loaded_model.predict_classes(image_resize_2 , verbose = 0)

    return loaded_model_pred[0]

def extract_number(sudoku):
    global k
    sudoku = cv2.resize(sudoku, (900,900))
    #cv2.imwrite('./tmo5.jpg', sudoku[0:50,0:50])


    # split sudoku
    grid = np.zeros([9,9])
    for i in range(9):
        for j in range(9):
            image = sudoku[i*100:(i+1)*100,j*100:(j+1)*100]

            if image.sum() > 450000:
                print(image.sum())
                k = k + 1
                grid[i][j] = identify_number(image)
            else:
                print("QQQQQQQQQQQQQQ")
                grid[i][j] = 0
    return grid.astype(int)




