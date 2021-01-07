import numpy as np

class appData:
    
    # Static reference for colour infomration 
    colours=[
    {
        'colour': 'Red', # String name of colour
        'colourID': 1, # ID number for colour
        'visRGB': np.uint8([0,69,255]) # RGB colour for visulisation purposes
    }
    ]

    # Note, the stud colour mappings are used for both stud config and brick config
    studColourIDMappings = {
        0: 'null', 
        1: 'shadow',
        2: 'unused',
        3: 'unused',
        4: 'unused',
        5: 'buildPlate',
        6: 'red',
        7: 'green',
        8: 'blue',
        9: 'yellow'
    }

    colourIDtoVis = {
        0: np.uint8([0,0,0]),
        1: np.uint8([0,0,255]) #BGR
    }




    # A dictionary of all bricks where the key is the brick ID
    # Name is in format width x height
    # Origin of brick is always in top left
    bricksRef = {

        #Vertical 1 stud wide
        0: {
            'name': '1x1', # Sting name reference for each brick
            'shape': np.array([[0,0]]) # Coordinates for each stud of the brick (row,col)
        },
        1: {
            'name': '1x2', 
            'shape': np.array([[0,0],[1,0]]) 
        },
        2: {
            'name': '1x3', 
            'shape': np.array([[0,0],[1,0],[2,0]]) 
        },
        3: {
            'name': '1x4',
            'shape': np.array([[0,0],[1,0],[2,0],[3,0]]) 
        },
        4: {
            'name': '1x6', 
            'shape': np.array([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0]]) 
        },
        5: {
            'name': '1x8',
            'shape': np.array([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]]) 
        },


        # Horiztonal 1 stud wide
        6: {
            'name': '2x1', 
            'shape': np.array([[0,0],[0,1]]) 
        },
        7: {
            'name': '3x1', 
            'shape': np.array([[0,0],[0,1],[0,2]]) 
        },
        8: {
            'name': '4x1', 
            'shape': np.array([[0,0],[0,1],[0,2],[0,3]]) 
        },
        9: {
            'name': '6x1', 
            'shape': np.array([[0,0],[0,1],[0,2],[0,3],[0,4],[0,5]]) 
        },
        10: {
            'name': '8x1', 
            'shape': np.array([[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]]) 
        },




        # Vertical 2 studs wide
        11: {
            'name': '2x2', 
            'shape': np.array([[0,0],[1,0],[0,1],[1,1]]) 
        },
        12: {
            'name': '2x3', 
            'shape': np.array([[0,0],[1,0],[2,0],[0,1],[1,1],[2,1]]) 
        },
        13: {
            'name': '2x4',
            'shape': np.array([[0,0],[1,0],[2,0],[3,0],[0,1],[1,1],[2,1],[3,1]]) 
        },
        14: {
            'name': '2x6', 
            'shape': np.array([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[0,1],[1,1],[2,1],[3,1],[4,1],[5,1]]) 
        },
        15: {
            'name': '2x8',
            'shape': np.array([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1]]) 
        },




        # Horizontal 2 studs wide
        16: {
            'name': '3x2', 
            'shape': np.array([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]]) 
        },
        17: {
            'name': '4x2', 
            'shape': np.array([[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3]]) 
        },
        18: {
            'name': '6x2', 
            'shape': np.array([[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5]]) 
        },
        19: {
            'name': '8x2', 
            'shape': np.array([[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7]]) 
        },
    }
