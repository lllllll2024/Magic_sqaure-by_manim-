class magic_square(Scene):
    # 定义n x n个小正方形的数独
    # 其中l为每个小正方形的边长，pos为数独的三维中心坐标(类型为列表)
    def sudoku(self, n, l, pos):
        # 创建二维列表，用来储存nxn个位置
        pos_list = [[[0,0,0] for i in range(n)] for i in range(n)]
        # 建立组
        square_v = VGroup()
        # 循环生成9个不同位置的正方形
        for i in range(n):
            for j in range(n):
                # 每次都从中心点开始
                sqr = Square(side_length=l).move_to(pos)
                # 复制列表时，如果直接用 a = a，源列表的值会发生变化
                new_pos = pos.copy()
                sqr = sqr.copy().shift((1 - j) * l * LEFT, (1 - i) * l * UP)
                new_pos[0] -= (1 - j) * l
                new_pos[1] += (1 - i) * l
                pos_list[i][j][0] = new_pos[0]
                pos_list[i][j][1] = new_pos[1]
                square_v.add(sqr)
        return (square_v, pos_list)

    # 蓝色小正方形闪烁的函数
    def shift_shine(self,pos,blue_square):
        for i in range(3):
            self.add(blue_square)
            self.wait(0.5)
            self.remove(blue_square)
            self.wait(0.5)

    # 现实的状态以及提交动作
    def status_action(self,pos,status,action):
        t = Text(f"状态：{status} ，动作：{action}", font_size=20).move_to(pos)
        self.add(t)
        self.wait()
        return t

    def construct(self):
        long = 0.5  # 小正方形的长度
        n = 3 # nxn个小正方形
        '''
        # 1. 创建原点位置的3x3的数独
        s0 = self.sudoku(n, long, [0, 0, 
        0])
        sudoku = s0[0]
        pos_list = s0[1]
        # 播放数独的动画
        self.play(Create(sudoku))
        self.wait()
        '''
        # 2. 创建左上角的数独
        s1 = self.sudoku(n, long, [-2, 2, 0])
        sudoku1 = s1[0]
        pos_list1 = s1[1]
        # 添加数独
        self.add(sudoku1)

        # 初始的行数、列数
        h,l=0,1

        # 提示信息：状态：无数，动作：填数
        t = self.status_action([-2, 3.5, 0], "无数", "填数")
        blue_square = Square(side_length=long, fill_opacity=0.5, color=BLUE).move_to(pos_list1[h][l])
        for i in range(1,n*n+1):
            # 蓝色正方形移动
            self.play(blue_square.animate.move_to(pos_list1[h][l]))
            # 提示信息：
            self.remove(t)
            t = self.status_action([-2, 3.5, 0], "无数", "填数")
            # 闪烁
            self.shift_shine(pos_list1[h][l],blue_square)
            # 放数且标记此位置已经放数
            number = Text(str(i), font_size=30, color=RED).move_to(pos_list1[h][l])
            self.add(number)
            pos_list1[h][l][2]=1 # 标记
            self.wait()
            # 当最后1个数填好后，就结束了
            if i==n*n:
                self.remove(t)
                self.wait(0.1)
                break
            new_pos = pos_list1[h][l].copy() # 移动前将当前位置保存下来
            # 左上移动
            h-=1
            l-=1
            new_pos[0] -= long
            new_pos[1] += long
            # 判断是否越界，如果越界，调整到指定位置
            if (0<=h<=n-1) and (0<=l<=n-1):    # 不越界
                # 判断当前位置是否有数
                if pos_list1[h][l][2]==0: # 如果没数的话就可以放下一个数
                    continue
                else:    # 如果有数，就返返回原来位置并下移一格（之后暂不用再判断是否越界，目前3*3没有越界
                    # 蓝色正方形移动
                    self.play(blue_square.animate.move_to(pos_list1[h][l]))
                    # 提示信息
                    self.remove(t)
                    t = self.status_action([-2, 3.5, 0], "有数", "调整位置")
                    # 闪烁
                    self.shift_shine(pos_list1[h][l],blue_square) # 当前位置有数字闪烁提醒
                    # 调整位置
                    h+=1
                    l+=1
                    # 下移一格
                    h+=1
            else:  # 越界了就将位置调整至不越界
                # 蓝色正方形移动
                self.play(blue_square.animate.move_to(new_pos))
                # 提示信息
                self.remove(t)
                t = self.status_action([-2, 3.5, 0], "越界", "调整位置")
                # 闪烁
                self.shift_shine(new_pos,blue_square) # 越界了需要闪烁
                # 将未越界前的h和l值储存起来
                h1 = h+1
                l1 = l+1
                if h<0:h=n-1
                if l<0:l=n-1
                if pos_list1[h][l][2]==0: # 如果没数的话就可以放下一个数
                    continue
                else:    # 如果有数，就返返回原来位置并下移一格（之后暂不用再判断是否越界，目前3*3没有越界）
                    # 蓝色正方形移动
                    self.play(blue_square.animate.move_to(pos_list1[h][l]))
                    # 提示信息
                    self.remove(t)
                    t = self.status_action([-2, 3.5, 0], "有数", "调整位置")
                    # 闪烁
                    self.shift_shine(new_pos, blue_square)
                    # 回到原来未越界前的位置
                    h = h1
                    l = l1
                    # 下移一格
                    h+=1