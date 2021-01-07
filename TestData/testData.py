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
    brickConfigA = {
        'bricks': [
            {
                'id': 4,
                "position": [
                    1,
                    2
                ],
                "colour": 7
            }
        ]
    }
                          