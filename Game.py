import random

# ------游戏对象（游戏类）
class Game:
    # -------游戏初始化
    def __init__(self):
        self.board_list = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        # 得分
        self.score = 0
        # 空位:存储坐标（行，列）
        self.board_empty = []

    # -------开始打游戏
    def start(self):
        self.restart()
        while True:
            self.print_board()
            code = input('请输入指令>>>:')
            if code == 'w':
                # 向上
                self.move_up()
            elif code == 's':
                # 向下
                self.move_down()
            elif code == 'a':
                # 向左
                self.move_left()
            elif code == 'd':
                # 向右
                self.move_right()
            elif code == 'r':
                self.restart()
                continue
            elif code == 'q':
                # 退出
                exit('退出')
            else:
                print('你的输入有误，请重新输入：')
                continue

            # 判断游戏是否win
            if self.is_win():
                print('You win!')
                break
            if self.gameover():
                print('Game over!')
                break
            # 在空白的地方 随机添加2,4
            self.add_piece()

    # --------游戏赢了
    def is_win(self):
        self.board_empty = []
        for i in range(len(self.board_list)):
            for j in range(len(self.board_list[i])):
                if self.board_list[i][j] == 2048:
                    return True
                if self.board_list[i][j] == '':
                    self.board_empty.append((i, j))
        return False

    # --------游戏输了
    def gameover(self):
        if not self.board_empty:  # 如果不为空
            # 判断每行每列（满）、相邻的没有相等的元素
            # 判断每一行
            for i in range(len(self.board_list)):
                for j in range(len(self.board_list[i])-1):
                    if self.board_list[i][j] == self.board_list[i][j+1]:
                        return False
            # 判断每一列
            self.turn_right()
            for i in range(len(self.board_list)):
                for j in range(len(self.board_list[i])-1):
                    if self.board_list[i][j] == self.board_list[i][j+1]:
                        self.turn_left()
                        return False
            return True
        return False

    # --------打游戏按左时
    def move_left(self):
        for i in range(len(self.board_list)):
            self.board_list[i] = self.row_left_oper(self.board_list[i])

    # --------打游戏按上时
    def move_up(self):
        # 先左转90度
        self.turn_left()
        # 向左操作合并数字
        self.move_left()
        # 再左转回来
        self.turn_right()

    # --------打游戏按下时
    def move_down(self):
        # 先向右转90度
        self.turn_right()
        # 向左操作加数字
        self.move_left()
        # 再左转回来
        self.turn_left()

    # --------打游戏按右时
    def move_right(self):
        # 左转90度
        self.turn_left()
        # 向上操作
        self.move_up()
        # 再右转回来
        self.turn_right()

    # --------向左操作合并数字
    def row_left_oper(self, row):
        #l1 = [2, '', 2, 2]  # 变换思路[2,2,2]=====>[4,2]=====>[4, 2, '', '']
        # -------第一步：先提取非空项元素
        temp = []
        for item in row:
            if item:  # 也可以写成 item != ''，表示item不等于空的时候
                temp.append(item)
        # -------第二步：合并同类型（注意：temp长度不等，可能为0、1、2、3、4
        new_row = []
        flag = True  # 标志位。如果[2,2,2,'']变换之后=====>[4,2,'','']，第二次循环相邻的两个数的时候，前两项已经合并了，此时需要跳过第二个数
        for i in range(len(temp)):
            if flag:
                # 判断相邻的两个数是否相等
                if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                    new_row.append(temp[i] * 2)
                    flag = False  # 为FALSE时，就不会再进行判断了，即跳过了原本的第二个数
                else:
                    new_row.append(temp[i])
            else:
                flag = True
        #print(new_row)
        # -------第三步：补齐没有元素的位置
        n = len(row)
        for i in range(n - len(new_row)):
            new_row.append('')
        return new_row
    #----------------------------------------笨办法：
    # if len(temp) == 0:
    #     pass
    # if len(temp) < 2:
    #     new_row = temp
    # if len(temp) == 2:
    #     if temp[0] == temp[1]:
    #         new_row.append(temp[0]*2)
    #     else:
    #         new_row = temp
    #-----------------------------------------以此类推

    # --------向右旋转90度
    def turn_right(self):
        self.board_list = [list(x[::-1]) for x in zip(*self.board_list)]

    # --------向左旋转90度====>相当于右转270度
    def turn_left(self):
        for i in range(3):
            self.turn_right()

    # --------先随机位置(删除），再随机添加值
    def add_piece(self):
        if self.board_empty:
            p = self.board_empty.pop(random.randrange(len(self.board_empty)))
            self.board_list[p[0]][p[1]] = random.randrange(2, 5, 2)  # 随机产生2到5之间的数，包含2不包含5，步长为2.  即随机产生和4；

    # --------初始化 棋盘
    def restart(self):
        self.board_list = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
        ]
        # 随机两个位置
        # 随机两个值
        while True:
            t1 = (random.randrange(len(self.board_list)), random.randrange(len(self.board_list[0])))  # (行，列)
            t2 = (random.randrange(len(self.board_list)), random.randrange(len(self.board_list[0])))  # (行，列)
            if t1 != t2:
                break
        self.board_list[t1[0]][t1[1]] = random.randrange(2, 5, 2)
        self.board_list[t2[0]][t2[1]] = random.randrange(2, 5, 2)

    # --------打印棋盘
    def print_board(self):
        print('''SCORE:{}
	    +-----+-----+-----+-----+
	    |{:^5}|{:^5}|{:^5}|{:^5}|
	    +-----+-----+-----+-----+
	    |{:^5}|{:^5}|{:^5}|{:^5}|
	    +-----+-----+-----+-----+
	    |{:^5}|{:^5}|{:^5}|{:^5}|
	    +-----+-----+-----+-----+
	    |{:^5}|{:^5}|{:^5}|{:^5}|
	    +-----+-----+-----+-----+
	    w(up),s(down),a(left),d(right)
	    r(restart),q(exit)'''.format(self.score, *self.board_list[0], *self.board_list[1], *self.board_list[2],
                                    *self.board_list[3]))
    # {:^5}：    ^代表居中；   5代表长度；  冒号代表空格

# -------实例化---------主函数
if __name__ == '__main__':
    game = Game()
    game.start()


