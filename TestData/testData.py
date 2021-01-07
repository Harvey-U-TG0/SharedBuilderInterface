import numpy as np

class ITestData:
    arrangementA = {
        "bricks": [
            {
                "type": "2x2",
                "position": [
                    1,
                    2
                ],
                "colour": "green"
            },
            {
                "type": "1x1",
                "position": [
                    0,
                    0
                ],
                "colour": "red"
            }
        ],
    }

# Brick config test data
class StudConfigTestData:
    studConfigA = np.array([[6,6,5,5,7,7],
                            [6,6,5,5,7,7],
                            [5,5,5,5,5,5],
                            [5,5,5,5,5,5],
                            [8,8,5,5,0,0],
                            [8,8,5,5,0,0]])

class BrickConfigTestData:
    # Bricks are stored using id and colour values as mapped in data.py
    brickConfigA = [
            {
                'shapeID': 0,
                "position": [0,0],
                "colourID": 6
            },
            {
                'shapeID': 11,
                "position": [0,4],
                "colourID": 7
            },
            {
                'shapeID': 11,
                "position": [3,3],
                "colourID": 8
            },

        ]

                          