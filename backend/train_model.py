from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
import json

# =========================
# IMAGE SETTINGS
# =========================

IMG_SIZE = 224

BATCH_SIZE = 16

# =========================
# DATA GENERATOR
# =========================

train_datagen = ImageDataGenerator(

    rescale=1./255,

    validation_split=0.2,

    rotation_range=20,

    zoom_range=0.2,

    horizontal_flip=True

)

# =========================
# TRAIN DATA
# =========================

train_data = train_datagen.flow_from_directory(

    'dataset',

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode='categorical',

    subset='training'

)

# =========================
# VALIDATION DATA
# =========================

val_data = train_datagen.flow_from_directory(

    'dataset',

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode='categorical',

    subset='validation'

)

# =========================
# CNN MODEL
# =========================

model = Sequential()

model.add(Conv2D(

    32,

    (3,3),

    activation='relu',

    input_shape=(224,224,3)

))

model.add(MaxPooling2D(2,2))

model.add(Conv2D(

    64,

    (3,3),

    activation='relu'

))

model.add(MaxPooling2D(2,2))

model.add(Conv2D(

    128,

    (3,3),

    activation='relu'

))

model.add(MaxPooling2D(2,2))

model.add(Flatten())

model.add(Dense(

    128,

    activation='relu'

))

model.add(Dropout(0.5))

model.add(Dense(

    train_data.num_classes,

    activation='softmax'

))

# =========================
# COMPILE MODEL
# =========================

model.compile(

    optimizer='adam',

    loss='categorical_crossentropy',

    metrics=['accuracy']

)

# =========================
# TRAIN MODEL
# =========================

model.fit(

    train_data,

    validation_data=val_data,

    epochs=10

)

# =========================
# SAVE MODEL
# =========================

model.save("model.h5")

print(

    "✅ Model Trained Successfully"

)

class_names = [
    class_name
    for class_name, class_index in sorted(
        train_data.class_indices.items(),
        key=lambda item: item[1]
    )
]

with open("class_names.json", "w") as label_file:
    json.dump(class_names, label_file)

print("Class order:", class_names)
