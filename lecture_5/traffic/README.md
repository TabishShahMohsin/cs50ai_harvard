Here is what I experimented with: 

Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Layer (type)               ┃ Output Shape        ┃    Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ dense (Dense)              │ (None, 30, 30, 8)   │         32 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_1 (Dense)            │ (None, 30, 30, 8)   │         72 │
├────────────────────────────┼─────────────────────┼────────────┤
│ flatten (Flatten)          │ (None, 7200)        │          0 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_2 (Dense)            │ (None, 43)          │    309,643 │
└────────────────────────────┴─────────────────────┴────────────┘
 Total params: 309,747 (1.18 MB)
 Trainable params: 309,747 (1.18 MB)
 Non-trainable params: 0 (0.00 B)
This produces: 333/333 - 0s - 724us/step - accuracy: 0.9276 - loss: 0.0136
This in itself is a very simple model and fast to train but yet it achieved this.

Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Layer (type)               ┃ Output Shape        ┃    Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ conv2d (Conv2D)            │ (None, 28, 28, 32)  │        896 │
├────────────────────────────┼─────────────────────┼────────────┤
│ flatten (Flatten)          │ (None, 25088)       │          0 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense (Dense)              │ (None, 128)         │  3,211,392 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_1 (Dense)            │ (None, 8)           │      1,032 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_2 (Dense)            │ (None, 43)          │        387 │
└────────────────────────────┴─────────────────────┴────────────┘
 Total params: 3,213,707 (12.26 MB)
 Trainable params: 3,213,707 (12.26 MB)
 Non-trainable params: 0 (0.00 B)
This produces: 333/333 - 1s - 2ms/step - accuracy: 0.0561 - loss: 0.1042
This model uses the flatten layer too early and as a result it looses the spatial information from the iamges, making it harder for the model to learn


Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Layer (type)               ┃ Output Shape        ┃    Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ conv2d (Conv2D)            │ (None, 29, 29, 10)  │        130 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense (Dense)              │ (None, 29, 29, 128) │      1,408 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_1 (Dense)            │ (None, 29, 29, 128) │     16,512 │
├────────────────────────────┼─────────────────────┼────────────┤
│ flatten (Flatten)          │ (None, 107648)      │          0 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_2 (Dense)            │ (None, 43)          │  4,628,907 │
└────────────────────────────┴─────────────────────┴────────────┘
 Total params: 4,646,957 (17.73 MB)
 Trainable params: 4,646,957 (17.73 MB)
 Non-trainable params: 0 (0.00 B)
This produces: 333/333 - 6s - 19ms/step - accuracy: 0.9493 - loss: 0.5037
This result is great but it utilized various p&c of layers, like just shifting the flatten layer before other layers pushed the accuracy to a ground. 

Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Layer (type)               ┃ Output Shape        ┃    Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ flatten (Flatten)          │ (None, 2700)        │          0 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense (Dense)              │ (None, 128)         │    345,728 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_1 (Dense)            │ (None, 8)           │      1,032 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_2 (Dense)            │ (None, 43)          │        387 │
└────────────────────────────┴─────────────────────┴────────────┘
 Total params: 347,147 (1.32 MB)
 Trainable params: 347,147 (1.32 MB)
 Non-trainable params: 0 (0.00 B)
This produces: 333/333 - 0s - 452us/step - accuracy: 0.0560 - loss: 3.4983
Again due to using the flatten layer before the dense layers

Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Layer (type)               ┃ Output Shape        ┃    Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ dense (Dense)              │ (None, 30, 30, 8)   │         32 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_1 (Dense)            │ (None, 30, 30, 43)  │        387 │
├────────────────────────────┼─────────────────────┼────────────┤
│ flatten (Flatten)          │ (None, 38700)       │          0 │
├────────────────────────────┼─────────────────────┼────────────┤
│ dense_2 (Dense)            │ (None, 43)          │  1,664,143 │
└────────────────────────────┴─────────────────────┴────────────┘
 Total params: 1,664,562 (6.35 MB)
 Trainable params: 1,664,562 (6.35 MB)
 Non-trainable params: 0 (0.00 B)
This produces: 333/333 - 1s - 2ms/step - accuracy: 0.9502 - loss: 0.0107
Again such simple and light model still had a good accuracy
