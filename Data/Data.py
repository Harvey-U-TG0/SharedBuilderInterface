class applicationData:
    
    # Static reference for colour infomration 
    colours=[
    {
        'colour': 'Red', # String name of colour
        'colourID': 1, # ID number for colour
        'visRGB': np.uint8([0,69,255]) # RGB colour for visulisation purposes
    }
    ]

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