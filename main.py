import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
import sys


def builder():
    global open_folder
    Amplmas = []
    Freqmas = []
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText('Выберите файл ГШ в формате .csv ')
    msg.setWindowModality(QtCore.Qt.ApplicationModal)
    msg.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    msg.exec()
    open_folder = QtWidgets.QFileDialog.getOpenFileName()[0]

    print("Открытый файл : ", open_folder)
    mas = np.loadtxt(open_folder, delimiter=',')  # загружаем файл csv в массив mas1

    for x in range(len(mas)):
        Amplmas.append(float(mas[x][1]))
        Freqmas.append(float(mas[x][0] / 10 ** 6))

    Amplmas = np.array(Amplmas, dtype=np.float64)
    Freqmas = np.array(Freqmas, dtype=np.float64)

    fig1 = plt.figure(1)
    sub1 = fig1.add_subplot(111)
    sub1.clear()
    sub1.plot(Freqmas, Amplmas)
    sub1.set_xlabel('Частота, [МГц]')
    sub1.set_ylabel('Амплитуда, [дБмкВ]')
    # sub1.set_title('Цепь электропитания 220В, RBW = 10кГц')
    sub1.set_title(line_name + ', RBW = ' + RBW)
    sub1.grid(True)
    # поменять yticks, ylim, xlim тут...............................
    # yticks = np.array([0,10,18,25,30])
    # sub1.set_yticks(yticks)
    # ylabels = sub1.get_ylabel()
    sub1.set_ylim(top=60)
    # sub1.set_ylim(bottom=0)
    sub1.set_xlim(left=START, right=END)

    fig1.set_size_inches(15, 8)
    fig1.tight_layout()
    fig1.savefig(str(sys.argv)[2:str(sys.argv).rfind('/') + 1] + 'GW_' + line_name.replace('/', '_') + '_' + RBW
                 + '_' + str(START) + 'to' + str(END) + '.png', dpi=100, fmt='png')
    print('График сохранен в ' + str(sys.argv)[2:str(sys.argv).rfind('/') + 1] + 'GW_' + line_name + '_' + RBW + '.png')
    fig1.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    line_name = QtWidgets.QInputDialog.getItem(QtWidgets.QWidget(),
                                               'Окно ввода',
                                               'Выберите тип линии',
                                               ['Электрическая составляющая э/м поля',
                                                'Магнитная составляющая э/м поля',
                                                'Цепь электропитания 220В',
                                                'Линия связи',
                                                'Шина заземления',
                                                'АЧХ ГШ на выходе линии связи по витой паре',
                                                'АЧХ ГШ на выходе линии связи оптического приемо-передатчика',
                                                'АЧХ ГШ на контактах питания оптического приемо-передатчика'
                                                ],
                                               current=0, editable=True)[0]
    RBW = QtWidgets.QInputDialog.getItem(QtWidgets.QWidget(),
                                         'Окно ввода',
                                         'Введите RBW : [RBW Гц]',
                                         ['1кГц',
                                          '100кГц'],
                                         current=0, editable=True)[0]
    START = QtWidgets.QInputDialog.getInt(QtWidgets.QWidget(),
                                          'Окно ввода',
                                          'Введите Начальную точку диапазона в МГЦ-- "20"')[0]
    END = QtWidgets.QInputDialog.getInt(QtWidgets.QWidget(),
                                        'Окно ввода',
                                        'Введите Конечную точку диапазона в МГЦ-- "1000"')[0]
    builder()
    app.exit()
    sys.exit(app.exec_())
