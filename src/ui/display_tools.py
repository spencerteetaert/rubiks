'''
File for display tools (console, 3d, training visualization/graphs)
'''

def display_console(cube, letter=0):
    cube = cube.state
    if letter == 0:
        print("       ", cube[0][3], cube[0][4], cube[0][5])
        print("       ", cube[1][3], cube[1][4], cube[1][5])
        print("       ", cube[2][3], cube[2][4], cube[2][5])
        print("")
        print(cube[0][0], cube[0][1], cube[0][2], " ", cube[0][6], cube[0][7], cube[0][8], " ", cube[0][12], cube[0][13], cube[0][14], " ", cube[0][15], cube[0][16], cube[0][17])
        print(cube[1][0], cube[1][1], cube[1][2], " ", cube[1][6], cube[1][7], cube[1][8], " ", cube[1][12], cube[1][13], cube[1][14], " ", cube[1][15], cube[1][16], cube[1][17])
        print(cube[2][0], cube[2][1], cube[2][2], " ", cube[2][6], cube[2][7], cube[2][8], " ", cube[2][12], cube[2][13], cube[2][14], " ", cube[2][15], cube[2][16], cube[2][17])
        print("")
        print("       ", cube[0][9], cube[0][10], cube[0][11])
        print("       ", cube[1][9], cube[1][10], cube[1][11])
        print("       ", cube[2][9], cube[2][10], cube[2][11])
        print("")
    else:
        cubeLetter = [["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"]]
        for i in range(3):
            for j in range(18):
                if cube[i][j] == 0:
                    cubeLetter[i][j] = "L"
                if cube[i][j] == 1:
                    cubeLetter[i][j] = "U"
                if cube[i][j] == 2:
                    cubeLetter[i][j] = "F"
                if cube[i][j] == 3:
                    cubeLetter[i][j] = "D"
                if cube[i][j] == 4:
                    cubeLetter[i][j] = "R"
                if cube[i][j] == 5:
                    cubeLetter[i][j] = "B"

        print("       ", cubeLetter[0][3], cubeLetter[0][4], cubeLetter[0][5])
        print("       ", cubeLetter[1][3], cubeLetter[1][4], cubeLetter[1][5])
        print("       ", cubeLetter[2][3], cubeLetter[2][4], cubeLetter[2][5])
        print("")
        print(cubeLetter[0][0], cubeLetter[0][1], cubeLetter[0][2], " ", cubeLetter[0][6], cubeLetter[0][7], cubeLetter[0][8], " ", cubeLetter[0][12], cubeLetter[0][13], cubeLetter[0][14], " ", cubeLetter[0][15], cubeLetter[0][16], cubeLetter[0][17])
        print(cubeLetter[1][0], cubeLetter[1][1], cubeLetter[1][2], " ", cubeLetter[1][6], cubeLetter[1][7], cubeLetter[1][8], " ", cubeLetter[1][12], cubeLetter[1][13], cubeLetter[1][14], " ", cubeLetter[1][15], cubeLetter[1][16], cubeLetter[1][17])
        print(cubeLetter[2][0], cubeLetter[2][1], cubeLetter[2][2], " ", cubeLetter[2][6], cubeLetter[2][7], cubeLetter[2][8], " ", cubeLetter[2][12], cubeLetter[2][13], cubeLetter[2][14], " ", cubeLetter[2][15], cubeLetter[2][16], cubeLetter[2][17])
        print("")
        print("       ", cubeLetter[0][9], cubeLetter[0][10], cubeLetter[0][11])
        print("       ", cubeLetter[1][9], cubeLetter[1][10], cubeLetter[1][11])
        print("       ", cubeLetter[2][9], cubeLetter[2][10], cubeLetter[2][11])
        print("")


def display_3d(cube):
    pass
