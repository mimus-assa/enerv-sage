

def text_page_1(lines):
    text_settings_page1 = [
        {'x': 30, 'y': 41, 'text': lines[0], 'size': 5, 'style': '', 'align': 'C', 'cell_height': 10, 'line_height': 10, 'border': 1},
        {'x': 30, 'y': 55, 'text': lines[1], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 30, 'y': 65, 'text': lines[2], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 63, 'y': 65, 'text': lines[3], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 95, 'y': 65, 'text': lines[4], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 128, 'y': 65, 'text': lines[5], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 30, 'y': 74, 'text': lines[6], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 76, 'y': 74, 'text': lines[7], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 128, 'y': 74, 'text': lines[8], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 30, 'y': 84, 'text': lines[9], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 76, 'y': 84, 'text': lines[10], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},

        {'x': 33,  'y': 103, 'text': lines[11], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 98,  'y': 103, 'text': lines[12], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 30,  'y': 112, 'text': lines[13], 'size': 6, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 63,  'y': 112, 'text': lines[14], 'size': 6, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 95,  'y': 112, 'text': lines[15], 'size': 6, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 128, 'y': 112, 'text': lines[16], 'size': 6, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 30,  'y': 121, 'text': lines[17], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 76,  'y': 121, 'text': lines[18], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 128, 'y': 121, 'text': lines[19], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 30,  'y': 131, 'text': lines[20], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 76,  'y': 131, 'text': lines[21], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},

        {'x': 82,  'y': 145, 'text': lines[22], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 130,  'y': 145, 'text': lines[23], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},  

        {'x': 51,  'y': 159, 'text': lines[24], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 91,  'y': 159, 'text': lines[25], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},  
        {'x': 117,  'y': 159, 'text': lines[26], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},  

        {'x': 30,  'y': 177, 'text': lines[27], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},  
        {'x': 98,  'y': 177, 'text': lines[28], 'size': 8, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},  


        {'x': 30,  'y': 198, 'text': lines[29], 'size':  5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 65,  'y': 198, 'text': lines[30], 'size':  5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 130,  'y': 198, 'text': lines[31], 'size':  5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},

        {'x': 30,  'y': 238, 'text': lines[32], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 80,  'y': 253, 'text': lines[33], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},
        {'x': 130,  'y': 253, 'text': lines[34], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 10, 'border': 0},

    ]

    return text_settings_page1


def text_page_2(lines):

    text_settings_page2 = [
        {'x': 30, 'y': 45, 'text': lines[35], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 3, 'border': 0},
        {'x': 30, 'y': 56, 'text': lines[36], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 3, 'border': 0},
        {'x': 30, 'y': 59, 'text': lines[37], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 3, 'border': 0},

        {'x': 50, 'y': 96, 'text': lines[38], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 3, 'border': 0},
        {'x': 50, 'y': 101, 'text': lines[39], 'size': 5, 'style': '', 'align': 'J', 'cell_height': 10, 'line_height': 3, 'border': 0},
        # Agrega más configuraciones aquí si necesitas más líneas de texto
    ]
    return text_settings_page2
