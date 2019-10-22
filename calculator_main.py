import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import calculator


class MainCode(QMainWindow, calculator.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        calculator.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn = QPushButton("1")
        self.btn.clicked.connect(self.show_msg)
        print(self.btn)
        print(self.Num_1)
        self.Num_0.clicked.connect(self.show_msg)
        self.Num_1.clicked.connect(self.show_msg)
        self.Num_2.clicked.connect(self.show_msg)
        self.Num_3.clicked.connect(self.show_msg)
        self.Num_4.clicked.connect(self.show_msg)
        self.Num_5.clicked.connect(self.show_msg)
        self.Num_6.clicked.connect(self.show_msg)
        self.Num_7.clicked.connect(self.show_msg)
        self.Num_8.clicked.connect(self.show_msg)
        self.Num_9.clicked.connect(self.show_msg)
        self.Num_dot.clicked.connect(self.show_msg)
        self.OP_equal.clicked.connect(self.show_msg)
        self.OP_plus.clicked.connect(self.show_msg)
        self.OP_minus.clicked.connect(self.show_msg)
        self.OP_time.clicked.connect(self.show_msg)
        self.OP_divide.clicked.connect(self.show_msg)
        self.OP_CE.clicked.connect(self.show_msg)

        self.char_stack = []  # 操作符号的栈
        self.num_stack = []  # 操作数的栈
        self.nums = [chr(i) for i in range(48, 58)]
        self.operators = ['+', '-', '*', '/']
        self.empty_flag = True  # 这个flag的含义是来判断计算器是不是第一次启动，在显示屏幕中无数据
        self.after_operator = False  # 看了计算器的计算，比如1+2在输入+后，1海显示在屏幕上，输入了2之后，1就被替换了， 这个flag的作用就是这样的
        self.char_top = ''  # 保留栈顶的操作符号
        self.num_top = 0  # 保留栈顶的数值
        self.res = 0  # 保留计算结果，看计算器计算一次后，在继续按等号，还会重复最近一次的计算1+2,得到3之后，在按等号就是3+2， 以此类推.

        # >先计算, 为什么同样的符号改成了后计算, 是为了方便做一项操作,
        # 就是在你计算一个表达式之后，在继续按住等号, 以及会执行最后一次的符号运算
        self.priority_map = {
            '++': '>', '+-': '>', '-+': '>', '--': '>',
            '+*': '<', '+/': '<', '-*': '<', '-/': '<',
            '**': '>', '//': '>', '*+': '>', '/+': '>',
            '*-': '>', '/-': '>', '*/': '>', '/*': '>'
        }

    def clear_lineEdit(self):
        self.lineEdit.clear()
        self.lineEdit.setText('0')
        self.res = 0
        # 清空，就相当于刚打开计算器一样
        self.empty_flag = True

    def deal_num_btn(self, sender_text):
        # 这个after_operatpr就是判断是不是在输入了操作符号后，有输入数字
        # 比如 1+ 这时候在输入2， 这种情况, 这时候，应该把1清理掉，去显示2
        if self.after_operator:
            self.lineEdit.clear()
            self.after_operator = False
        _str = self.lineEdit.text()
        # 对lineEdit是否有数据，有数据就继续往里面追加，没有就是重新开始
        if _str == '0' or _str == 'Error' or self.empty_flag:
            _str = ''
        self.lineEdit.setText(_str + sender_text)
        # 加入了数据，empty_falg就改变了
        self.empty_flag = False

    def deal_operator_btn(self, sender_text):
        # 操作符号 +, -, *, /
        self.empty_flag = False
        _str = self.lineEdit.text()

        # 比如刚打开计算器 你直接输入了一个 +
        if _str == '0' or _str == 'Error':
            # 就是需要上一次的计算结果, 需要把上一次的计算结果送入数字栈，操作符送入符号栈
            self.num_stack.append(self.res)
            self.char_stack.append(sender_text)
        else:
            # 在你输入操作符号之前，可能输入了数字或者一个操作符
            # 如果输入的是一个操作符那么，num_stack和char_stack的长度是一样的，可以来判断
            # 1++ 第二个加号并没有进入数字栈，所以可以看出, 他俩的长度是一样的
            self.num_top = float(_str) if _str.count('.') != 0 \
                else int(_str)
            self.num_stack.append(self.num_top)
            self.char_top = sender_text
            num_stack_len, char_stack_len = len(self.num_stack), len(self.char_stack)
            if (num_stack_len == char_stack_len) and num_stack_len != 0:
                # 在这里处理类似 输入 1+- 这种情况就是 1-后一个字符替换前面的
                self.char_stack[-1] = sender_text
            else:
                # 是正常的输入，1+2+此时，2入数字栈
                # 1+2*..... 类似输入
                if len(self.char_stack) == 0:
                    self.char_stack.append(self.char_top)
                else:
                    # 考虑符号的优先级, 1+2*这个时候只需要*入栈即可， 1*2+就要去计算1*2了
                    operator_cmp_key = self.char_stack[-1] + sender_text
                    if self.priority_map[operator_cmp_key] == '>':
                        print(self.num_stack, self.char_stack)
                        self.calculate(sender_text)
                    self.char_stack.append(sender_text)
                # 你输入一个操作符号, 那么接下里输入的时候，需要把前的lineEdit 内容清空
                self.after_operator = True

    def deal_point_btn(self):
        _str = self.lineEdit.text()
        self.empty_flag = False
        # 计算lineEdit中有多少小数点
        point_count = self.lineEdit.text().count('.')
        if point_count == 0:
            _str += '.'
        self.lineEdit.setText(_str)

    def deal_equal_btn(self):
        _str = self.lineEdit.text()
        self.empty_flag = True
        try:
            # 在等号前 处理的数字 可能是上一次的计算结果，也可能是输入的数据的最后一个指，所以不能直接保存在num_top中，考虑如果是上一次的计算结果是，直接保存在num_top会是什么结果
            tmp_num = float(_str) if _str.count('.') != 0 \
                else int(_str)
            self.num_stack.append(tmp_num)
            if len(self.num_stack) == 1:
                # 你刚做完一个计算， 结果还保留在屏幕上，这时候再按=，
                # 例如 1+2， 此时屏幕显示3，你再按=就是计算3+2， 再按就是5+2
                # 需要上一次的结果, 所以要在数字栈中加入num_top, 符号栈中加入char_top
                self.char_stack.append(self.char_top)
                self.num_stack.append(self.num_top)
            else:
                # lineEdit的值不是上一次的计算结果，我们就把他保存在num_top中。
                self.num_top = tmp_num
        except Exception as e:
            # 可能出现异常的原因是 我忘了，可能抓不到异常，如果发现请告诉我
            self.num_stack.append(self.num_top)
            print('Error: {}'.format(e.args))
        self.calculate()
        self.num_stack.clear()
        self.char_stack.clear()

    def show_msg(self):
        sender = self.sender()
        sender_text = sender.text()
        if sender_text == 'CE':
            self.clear_lineEdit()
        elif sender_text in self.nums:
            self.deal_num_btn(sender_text)
        elif sender_text == '.':
            self.deal_point_btn()
        elif sender_text in self.operators:
            self.deal_operator_btn(sender_text)
        elif sender_text == '=':
            self.deal_equal_btn()

    def auxiliary_calculate(self, first_num, second_num, operator: str):
        # 辅助计算
        if operator == '/':
            if second_num == 0:
                _str = 'Error'
                self.res = 0
                self.lineEdit.setText(_str)
                return None
            else:
                return first_num / second_num
        elif operator == '*':
            return first_num * second_num
        elif operator == '+':
            return first_num + second_num
        else:
            return first_num - second_num

    def calculate(self, operator='='):
        # 这里就很好理解了
        if operator == '=':
            # 要最后的结果
            print(self.num_stack)
            print(self.char_stack)
            error_falg = False
            while len(self.char_stack) >= 1:
                n1 = self.num_stack.pop()
                n2 = self.num_stack.pop()
                op = self.char_stack.pop()
                result = self.auxiliary_calculate(n2, n1, op)
                if result is None:
                    self.num_stack.clear()
                    self.char_stack.clear()
                    error_falg = True
                    break
                else:
                    self.num_stack.append(result)
            if not error_falg:
                self.res = self.num_stack.pop()
                if self.res == int(self.res):
                    self.res = int(self.res)
                self.lineEdit.setText(str(self.res))
            else:
                self.lineEdit.setText('Error')
        else:
            op = self.char_stack.pop()
            while len(self.char_stack) >= 0 and (self.priority_map[op + operator] == '>'):
                n1 = self.num_stack.pop()
                n2 = self.num_stack.pop()
                result = self.auxiliary_calculate(n2, n1, op)
                if result is None:
                    self.num_stack.clear()
                    self.char_stack.clear()
                    break
                self.num_stack.append(self.auxiliary_calculate(n2, n1, op))
                try:
                    op = self.char_stack.pop()
                except Exception as e:
                    break
            self.res = self.num_stack[-1]
            if self.res == int(self.res):
                self.res = int(self.res)
            self.lineEdit.setText(str(self.res))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cal = MainCode()
    cal.show()
    sys.exit(app.exec_())