from PyQt5 import QtCore, QtGui, QtWidgets
from pickle import dump, load
from random import choice, shuffle
import sys


SLOI = 1 # какой слой.
ohi = "" # текст тех. строки          |1, 2, 3

sos = 0   # составленно ли расписание |1
gotovo = 0  # сохранено ли расписание |1
L = 0    # длина списка сотрудников   |1

sozdano = 0 # готова ли база данных.  |2

izm = 0  # есль ли кадровые изменения |3



# слой 1. | составление расписания
#################################################################################################################
def form_z(x):
    'формирование списка залов (обьединения и закрытие) исходя из количества сотрудников.\
    на выходе даёт: список рабочих залов и спиcок залов на закрытие.'
    zali = zali_0.copy()
    q = len(zali)
    j = 0
    while len(zali) != x and j != q:
        j += 1
        for i in zali[str(j)]:
            if i == "del":
                del (zali[str(j)])
            elif i != str(j) and i != "#":
                zali.setdefault("_" + i + "+" + str(j) + "_", ["#", str(j), i] if (list(zali[i]) + list(zali[str(j)])).count("#") == 2 else [])
                del (zali[str(j)])
                zali[i] = ["del"]
    spis_zakr = []
    zali1 = list(zali.copy())
    for i in zali1:
        if len(zali) != x and "#" in zali[i]:
            spis_zakr.append(i)
            del(zali[i])
    return list(zali), spis_zakr

def minys_sotr(rip):
    'удаление из временного списка отсуствующих сотрудников'

    for r in rip:
        for i in range(len(spis_sot_1)):
            if r == spis_sot_1[i][1]:
                del(spis_sot_1[i])
                break
    return spis_sot_1

def rasp_ed(rip, zali_r):
    'составление расписания на 1 день'
    global spis_sot_1
    spis_sot_1 = minys_sotr(rip)

    koloda = {i[1]: i[2::1] for i in spis_sot_1}
    for i in koloda:
        while len(koloda[i]) > len(zali_r) - 2 and len(zali_r) > 1:
            del koloda[i][0]
    koloda1 = {i: list(set(zali_r) - set(koloda[i])) for i in koloda}
    a = []
    q = 0
    while len(zali_r) != len(set(a)) and q != 500:
        a = [choice(koloda1[i]) for i in koloda1]

        q += 1
    if q >= 500:
        a = zali_r
        shuffle(a)
    rasp_den = [[list(koloda1)[i], a[i]] for i in range(len(a))]
    for i in rasp_den:
        for j, m in enumerate(spis_sot_1):

            if i[0] == m[1]:
                spis_sot_1[j].append(i[1])

                if len(i[1]) < 4:
                    spis_sot_1[j][0] += 1
                else:
                    spis_sot_1[j][0] += 2
    return rasp_den

def cost():
    ohi = ""
    ui.label_1_5.setText(ohi)
    ui.textBrowser_1_1.setText("")
    global zali_z, grafik, sos, rip, spis_sot_1
    L = 0
    try:
        with open("spis_sot.bin", "rb") as s:
            spis_sot_1 = load(s)
        L = len(spis_sot_1)
    except:
        ohi = "Увы… Нет списка сотрудников. "
    if L > 15:
        ohi = "Превышен максимум сотрудников."
    elif L == 0:
        ohi = "Увы… Нет списка сотрудников. "
    if len(ohi)!=0:
        ui.label_1_5.setText(ohi)
        return False

    dni = ui.spinBox_1_1.value()
    rip = []
    for i in ui.sp:
        if i.isChecked() == False:
            for j in spis_sot_1:

                if j[1] == i.text():
                    rip.append(j[1])

    zali_r, zali_z = form_z(len(spis_sot_1) - len(set(rip)))
    if len(zali_r) > len(spis_sot_1) - len(set(rip)):
        ohi = "увы... сотрудников недостаточно\n для работы музея."
        ui.label_1_5.setText(ohi)
        return False
    elif len(zali_r) < len(spis_sot_1) - len(set(rip)):
        ohi = "что-то пошло не так…\n сотрудников больше чем залов."

        ui.label_1_5.setText(ohi)
        return False

    else: #elif len(zali_r) == len(spis_sot_1) - len(set(rip)):
        grafik = []
        for i in range(dni):
            grafik.append(rasp_ed(rip, zali_r))
    stroka = "\n" + " " * 10 + "РАСПИСАНИЕ:" + "\n" + "-" * 37
    zakr = ", ".join(zali_z)
    for i, m in enumerate(grafik):
        stroka += "\n" + f"день {i + 1}: \n"

        for j in m:
            stroka += "\n" + f"{j[0]}: {j[1]} зал." + " " * (25 - len(j[0]) - len(j[1]))

        stroka += "\n"
        if len(zakr) != 0:
            stroka += "\n" + f"закрытые залы: {zakr}."
        stroka += "\n" + "-" * 37
    ui.textBrowser_1_1.setText(stroka)
    sos = 1

def dl_pe():
    'подготовка текстового файла для печати'
    ohi = ""
    ui.label_1_5.setText(ohi)
    if sos == 0:
        ohi = "нечего распечатывать."
        ui.label_1_5.setText(ohi)
        return False

    zakr = ", ".join(zali_z)
    a = "\n" + " " * 30 + "РАСПИСАНИЕ:" + "\n\n" + "-" * 75
    for i, m in enumerate(grafik):
        a += "\n"
        a += f"день {i + 1}: \n\n\n"
        q = 0
        for j in m:
            a += f"{j[0]}: {j[1]} зал." + " " * (20 - len(j[0]) - len(j[1]))
            q += 1
            if q % 3 == 0:
                a += "\n" * 3
        a += "\n"
        if len(zakr) != 0:
            a += f"закрытые залы: {zakr}."
            a += "\n"
        a += "-" * 75
    fa = open("dlia printera.txt", "w", encoding='utf-8')
    fa.write(a)
    fa.close()
    ohi = "      готово!"
    ui.label_1_5.setText(ohi)

def sohr():
    'сохранение результата'
    global gotovo
    ohi = ""
    ui.label_1_5.setText(ohi)
    if sos == 0:
        ohi = "нечего сохранять."
        ui.label_1_5.setText(ohi)
        return False
    elif gotovo == 1:
        ohi = "уже сохранено. для продолжения\n- перезапустите программу."
        ui.label_1_5.setText(ohi)
        return False

    for i, n in enumerate(spis_sot):
        for i_1, n_1 in enumerate(spis_sot_1):
            if n[1] == n_1[1]:
                spis_sot[i][0] = n_1[0]
                spis_sot[i] += n_1[len(spis_sot[i])::]
    with open("spis_sot.bin", "wb") as s:
       dump(spis_sot, s)
    ohi = "      готово!"
    ui.label_1_5.setText(ohi)
    gotovo = 1
################################################################################################################


# слой 2.  | создание базы данных
################################################################################################################
def sozd():
    "создание базы данных, по сотрудникам и залам."
    global spis_sot, zali, sozdano
    zali = dict()
    spis_sot = []
    ui.label_2_12.setText("")

    if len(ui.textEdit_2_1.toPlainText()) == 0 or ui.spinBox_2_1.value() == 0:
        ui.label_2_12.setText("не хватает информации")
        return False

    sot = ui.textEdit_2_1.toPlainText().split("\n")  # сотрудники
    for i in sot:
        if len(i) != 0:
            spis_sot.append([0, i])
    zali = {str(i + 1): [str(i + 1)] for i in range(ui.spinBox_2_1.value())} # залы
    for i in zali:
        if ui.spinBox_2_2.value() == int(i) or ui.spinBox_2_3.value() == int(i) or ui.spinBox_2_4.value() == int(i) \
                or ui.spinBox_2_5.value() == int(i) or ui.spinBox_2_6.value() == int(i):
            zali[i].append("#")
    pari = []
    if ui.spinBox_2_7.value() != 0 and ui.spinBox_2_8.value() != 0:
        pari.append([ui.spinBox_2_7.value(), ui.spinBox_2_8.value()])
    if ui.spinBox_2_9.value() != 0 and ui.spinBox_2_10.value() != 0:
        pari.append([ui.spinBox_2_9.value(), ui.spinBox_2_10.value()])
    if ui.spinBox_2_11.value() != 0 and ui.spinBox_2_14.value() != 0:
        pari.append([ui.spinBox_2_11.value(), ui.spinBox_2_14.value()])
    if ui.spinBox_2_12.value() != 0 and ui.spinBox_2_13.value() != 0:
        pari.append([ui.spinBox_2_12.value(), ui.spinBox_2_13.value()])
    for i in pari:
        if i[0] == i[1]:
            ui.label_2_12.setText(f"зал {i[0]}, не может быть объединён сам с собой.")
            return False
        if i[0] > ui.spinBox_2_1.value():
            ui.label_2_12.setText(f"нет зала под номером {i[0]}.")
            return False
        if i[1] > ui.spinBox_2_1.value():
            ui.label_2_12.setText(f"нет зала под номером {i[1]}.")
            return False
    for i in pari:
        zali[str(i[0])].append(str(i[1]))
        zali[str(i[1])].append(str(i[0]))

    zali = {i: set(zali[i]) for i in zali}
    tekst = "сотрудники:\n\n" # текст в черновик
    for i in spis_sot:
        tekst += i[1]+"\n"
    tekst += "\n" + "-"*30 + "\n" + f"всего залов {ui.spinBox_2_1.value()}.\n"
    for i in zali:
        tekst += f"\n{i}й зал."
        if "#" in zali[i]:
            tekst += "\nможет быть закрыт."
        if not ("#" in zali[i]) and len(zali[i]) > 1 or len(zali[i]) > 2:
            for j in zali[i]:
                if j != i and j != "#":
                    tekst += f"\nможно обьеденить с {j}м залом."
        tekst += "\n" + "-"*30
    ui.textBrowser_2_1.setText(tekst)
    sozdano = 1

def sohran():
    "сохранение инфы в файлы"
    ui.label_2_12.setText("")
    if sozdano == 0:
        ui.label_2_12.setText("увы. пока что нечего сохранять.")
        return False
    try:
        with open("spis_sot.bin", "wb") as s:
            dump(spis_sot, s)
        with open("zali.bin", "wb") as z:
            dump(zali, z)
        ui.label_2_12.setText("    готово.")

    except:
        ui.label_2_12.setText("увы. ошибка сохранения.")
################################################################################################################


# слой 3.   | кадровые правки
################################################################################################################
def dekor(b):
    'общие декор коректирующих кнопок'
    def c():
        ohi = ""
        ui.label_3_5.setText(ohi)
        s = 0
        for i in ui.sp_3:
            if i.isChecked() == True:
                s += 1
        if s > 1:
            ohi = "Cлишком много «галочек»."
            ui.label_3_5.setText(ohi)
            return False
        b()
        tekst = "сотрудники:\n\n"  # текст в черновик
        for i in spis_sot:
            tekst += i[1] + "\n"
        ui.textBrowser_3_1.setText(tekst)
    return c

def sohr_3():
    'вненение изменений в базу'
    if izm == 0:
        ohi = "Нечего сохранять. Всё как было, так и есть. "
        ui.label_3_5.setText(ohi)
        return False
    try:
        with open("spis_sot.bin", "wb") as s:
            dump(spis_sot, s)
        ohi = "готово."
        ui.label_3_5.setText(ohi)
    except:
        ui.label_3_5.setText("увы. ошибка сохранения.")

@dekor
def dob():
    'добавление сотрудника'
    global izm
    for i in ui.sp_3:
        if i.isChecked() == True:
            ohi = "Непорядок. Отмечен сотрудник."
            ui.label_3_5.setText(ohi)
            return False
    if len(ui.textEdit_3_1.toPlainText()) == 0:
        ohi = "А кого добавить-то?"
        ui.label_3_5.setText(ohi)
        return False
    spis_sot.append([0, ui.textEdit_3_1.toPlainText()])
    izm = 1

@dekor
def prav():
    'замен/переименование сотрудника'
    global izm
    t = 0
    for i in ui.sp_3:
        if i.isChecked() == True:
            t += 1
    if t == 0:
        ohi = "А кого заменить-то?"
        ui.label_3_5.setText(ohi)
        return False
    if len(ui.textEdit_3_1.toPlainText()) == 0:
        ohi = "А на кого заменить-то?"
        ui.label_3_5.setText(ohi)
        return False
    for j in ui.sp_3:
        if j.isChecked():
            for i, n in enumerate(spis_sot):
                if n[1] == j.text():
                    spis_sot[i][1] = ui.textEdit_3_1.toPlainText()
    izm = 1

@dekor
def yda():
    'даление сотрудника'
    global izm
    t = 0
    for i in ui.sp_3:
        if i.isChecked() == True:
            t += 1
    if t == 0:
        ohi = "А кого далить-то?"
        ui.label_3_5.setText(ohi)
        return False

    for j in ui.sp_3:
        if j.isChecked():
            for i, n in enumerate(spis_sot):
                if n[1] == j.text():
                    del spis_sot[i]
    izm = 1
###################################################################################################################




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global ohi, spis_sot, L, spis_sot_1, zali_0
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(940, 810)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 400, 70))
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(795, 5, 140, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        if SLOI != 2:
            self.pushButton = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton.setGeometry(QtCore.QRect(35, 735, 260, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton.setFont(font)
            self.pushButton.clicked.connect(slo_2)
            self.pushButton.setObjectName("pushButton")
        if SLOI != 3:
            self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_2.setGeometry(QtCore.QRect(335, 735, 260, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_2.setFont(font)
            self.pushButton_2.clicked.connect(slo_3)
            self.pushButton_2.setObjectName("pushButton_2")
        if SLOI != 1:
            self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3.setGeometry(QtCore.QRect(635, 735, 260, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_3.setFont(font)
            self.pushButton_3.clicked.connect(slo_1)
            self.pushButton_3.setObjectName("pushButton_3")

        if SLOI == 1:
            try:
                with open("spis_sot.bin", "rb") as s:
                    spis_sot = load(s)
                with open("spis_sot.bin", "rb") as s:
                    spis_sot_1 = load(s)
                L = len(spis_sot_1)
            except:
                ohi = "Увы… Нет списка сотрудников. "

            if L > 15:
                ohi = "Превышен максимум сотрудников."
            elif L == 0:
                ohi = "Увы… Нет списка сотрудников. "
            if L != 0:
                try:
                    with open("zali.bin", "rb") as z:
                        zali_0 = load(z)
                except:
                    ohi = "Увы… Нет списка залов. "

            self.sp = []
            self.label_1_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_1_2.setGeometry(QtCore.QRect(90, 100, 140, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_1_2.setFont(font)
            self.label_1_2.setObjectName("label_1_2")

            self.label_1_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_1_10.setGeometry(QtCore.QRect(500, 390, 100, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_1_10.setFont(font)
            self.label_1_10.setObjectName("label_1_10")

            self.textBrowser_1_1 = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser_1_1.setGeometry(QtCore.QRect(500, 435, 410, 290))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            self.textBrowser_1_1.setFont(font)
            self.textBrowser_1_1.setObjectName("textBrowser")

            self.pushButton_1_2 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_1_2.setGeometry(QtCore.QRect(730, 240, 150, 70))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_1_2.setFont(font)
            self.pushButton_1_2.clicked.connect(dl_pe)
            self.pushButton_1_2.setObjectName("pushButton_1_2")

            j = 0
            for i in range(L):
                self.checkBox_1_1 = QtWidgets.QCheckBox(self.centralwidget)
                self.checkBox_1_1.setGeometry(QtCore.QRect(30, 150 + j, 400, 40))
                font = QtGui.QFont()
                font.setFamily("Segoe Script")
                font.setPointSize(12)
                self.checkBox_1_1.setFont(font)
                self.checkBox_1_1.setCheckState(2)
                self.checkBox_1_1.setObjectName("checkBox_1_1")
                j += 30
                self.sp.append(self.checkBox_1_1)

            self.label_1_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_1_4.setGeometry(QtCore.QRect(450, 100, 310, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_1_4.setFont(font)
            self.label_1_4.setObjectName("label_1_4")

            self.label_1_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_1_5.setGeometry(QtCore.QRect(20, 670, 450, 60))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_1_5.setFont(font)
            self.label_1_5.setText(ohi)
            self.label_1_5.setObjectName("label_1_5")

            self.label_1_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_1_6.setGeometry(QtCore.QRect(25, 110, 30, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_1_6.setFont(font)
            self.label_1_6.setObjectName("label_1_6")

            self.spinBox_1_1 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_1_1.setGeometry(QtCore.QRect(770, 100, 60, 50))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_1_1.setFont(font)

            self.pushButton_1_1 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_1_1.setGeometry(QtCore.QRect(500, 170, 150, 70))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_1_1.setFont(font)
            self.pushButton_1_1.clicked.connect(cost)
            self.pushButton_1_1.setObjectName("pushButton_1_3")

            self.pushButton_1_3 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_1_3.setGeometry(QtCore.QRect(500, 310, 150, 70))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_1_3.setFont(font)
            self.pushButton_1_3.clicked.connect(sohr)
            self.pushButton_1_3.setObjectName("pushButton_1_4")

            self.label_1_1 = QtWidgets.QLabel(self.centralwidget)
            self.label_1_1.setGeometry(QtCore.QRect(670, 330, 210, 70))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(10)
            self.label_1_1.setFont(font)
            self.label_1_1.setObjectName("label_1_1")

        if SLOI == 2:
            self.label_2_1 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_1.setGeometry(QtCore.QRect(440, 10, 120, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_1.setFont(font)
            self.label_2_1.setObjectName("label_2_1")

            self.spinBox_2_1 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_1.setGeometry(QtCore.QRect(460, 50, 70, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_1.setFont(font)
            self.spinBox_2_1.setObjectName("spinBox_2_1")

            self.label_2_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_2.setGeometry(QtCore.QRect(20, 90, 430, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_2.setFont(font)
            self.label_2_2.setObjectName("label_2_2")

            self.textEdit_2_1 = QtWidgets.QTextEdit(self.centralwidget)
            self.textEdit_2_1.setGeometry(QtCore.QRect(20, 130, 431, 411))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            self.textEdit_2_1.setFont(font)
            self.textEdit_2_1.setObjectName("textEdit_2_1")

            self.label_2_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_4.setGeometry(QtCore.QRect(590, 90, 310, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_4.setFont(font)
            self.label_2_4.setObjectName("label_2_4")

            self.spinBox_2_2 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_2.setGeometry(QtCore.QRect(550, 130, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_2.setFont(font)
            self.spinBox_2_2.setObjectName("spinBox_2_2")

            self.spinBox_2_3 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_3.setGeometry(QtCore.QRect(630, 130, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_3.setFont(font)
            self.spinBox_2_3.setObjectName("spinBox_2_3")

            self.spinBox_2_4 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_4.setGeometry(QtCore.QRect(710, 130, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_4.setFont(font)
            self.spinBox_2_4.setObjectName("spinBox_2_4")

            self.spinBox_2_5 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_5.setGeometry(QtCore.QRect(790, 130, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_5.setFont(font)
            self.spinBox_2_5.setObjectName("spinBox_2_5")

            self.spinBox_2_6 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_6.setGeometry(QtCore.QRect(870, 130, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_6.setFont(font)
            self.spinBox_2_6.setObjectName("spinBox_2_6")

            self.label_2_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_5.setGeometry(QtCore.QRect(590, 200, 310, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_5.setFont(font)
            self.label_2_5.setObjectName("label_2_5")

            self.spinBox_2_7 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_7.setGeometry(QtCore.QRect(550, 240, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_7.setFont(font)
            self.spinBox_2_7.setObjectName("spinBox_2_7")

            self.spinBox_2_8 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_8.setGeometry(QtCore.QRect(640, 240, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_8.setFont(font)
            self.spinBox_2_8.setObjectName("spinBox_2_8")

            self.label_2_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_6.setGeometry(QtCore.QRect(613, 250, 20, 20))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_6.setFont(font)
            self.label_2_6.setObjectName("label_2_6")

            self.label_2_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_7.setGeometry(QtCore.QRect(843, 250, 20, 20))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_7.setFont(font)
            self.label_2_7.setObjectName("label_2_7")

            self.spinBox_2_9 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_9.setGeometry(QtCore.QRect(780, 240, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_9.setFont(font)
            self.spinBox_2_9.setObjectName("spinBox_2_9")

            self.spinBox_2_10 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_10.setGeometry(QtCore.QRect(870, 240, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_10.setFont(font)
            self.spinBox_2_10.setObjectName("spinBox_2_10")

            self.spinBox_2_12 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_12.setGeometry(QtCore.QRect(777, 300, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_12.setFont(font)
            self.spinBox_2_12.setObjectName("spinBox_2_12")

            self.spinBox_2_13 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_13.setGeometry(QtCore.QRect(870, 300, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_13.setFont(font)
            self.spinBox_2_13.setObjectName("spinBox_2_13")

            self.label_2_9 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_9.setGeometry(QtCore.QRect(840, 310, 20, 20))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_9.setFont(font)
            self.label_2_9.setObjectName("label_2_9")

            self.label_2_8 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_8.setGeometry(QtCore.QRect(613, 310, 20, 20))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_8.setFont(font)
            self.label_2_8.setObjectName("label_2_8")

            self.spinBox_2_11 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_11.setGeometry(QtCore.QRect(550, 300, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_11.setFont(font)
            self.spinBox_2_11.setObjectName("spinBox_2_11")

            self.spinBox_2_14 = QtWidgets.QSpinBox(self.centralwidget)
            self.spinBox_2_14.setGeometry(QtCore.QRect(640, 300, 50, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.spinBox_2_14.setFont(font)
            self.spinBox_2_14.setObjectName("spinBox_2_14")

            self.label_2_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_10.setGeometry(QtCore.QRect(590, 370, 101, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_10.setFont(font)
            self.label_2_10.setObjectName("label_2_10")

            self.textBrowser_2_1 = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser_2_1.setGeometry(QtCore.QRect(550, 410, 370, 265))
            font = QtGui.QFont()  #
            font.setFamily("Segoe Script")  #
            font.setPointSize(12)  #
            self.textBrowser_2_1.setFont(font)  #
            self.textBrowser_2_1.setObjectName("textBrowser_2_1")

            self.pushButton_2_1 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_2_1.setGeometry(QtCore.QRect(40, 600, 150, 75))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_2_1.setFont(font)
            self.pushButton_2_1.clicked.connect(sozd)
            self.pushButton_2_1.setObjectName("pushButton_2_1")

            self.pushButton_2_2 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_2_2.setGeometry(QtCore.QRect(280, 600, 150, 75))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_2_2.setFont(font)
            self.pushButton_2_2.clicked.connect(sohran)
            self.pushButton_2_2.setObjectName("pushButton_2")

            self.label_2_12 = QtWidgets.QLabel(self.centralwidget)
            self.label_2_12.setGeometry(QtCore.QRect(20, 555, 510, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_2_12.setFont(font)
            self.label_2_12.setObjectName("label_12")

        if SLOI == 3:
            L = 0
            try:
                with open("spis_sot.bin", "rb") as s:
                    spis_sot = load(s)
                L = len(spis_sot)
            except:
                ohi = "Увы… Нет списка сотрудников. "
            if L > 15:
                ohi = "Превышен максимум сотрудников."

            self.sp_3 = []

            self.label_3_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_3_2.setGeometry(QtCore.QRect(20, 100, 141, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_3_2.setFont(font)
            self.label_3_2.setObjectName("label_3_2")

            self.label_3_10 = QtWidgets.QLabel(self.centralwidget)
            self.label_3_10.setGeometry(QtCore.QRect(590, 370, 101, 30))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_3_10.setFont(font)
            self.label_3_10.setObjectName("label_3_10")

            self.textBrowser_3_1 = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser_3_1.setGeometry(QtCore.QRect(550, 410, 370, 265))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            self.textBrowser_3_1.setFont(font)
            self.textBrowser_3_1.setObjectName("textBrowser_3_1")

            self.pushButton_3_1 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3_1.setGeometry(QtCore.QRect(760, 320, 150, 75))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_3_1.setFont(font)
            self.pushButton_3_1.clicked.connect(sohr_3)
            self.pushButton_3_1.setObjectName("pushButton_3_1")

            j = 0
            for i in range(L):
                self.checkBox_3_1 = QtWidgets.QCheckBox(self.centralwidget)
                self.checkBox_3_1.setGeometry(QtCore.QRect(20, 150 + j, 400, 40))
                font = QtGui.QFont()
                font.setFamily("Segoe Script")
                font.setPointSize(12)
                self.checkBox_3_1.setFont(font)
                self.checkBox_3_1.setObjectName("checkBox_3_1")
                self.sp_3.append(self.checkBox_3_1)
                j += 30

            self.label_3_4 = QtWidgets.QLabel(self.centralwidget)
            self.label_3_4.setGeometry(QtCore.QRect(450, 100, 470, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_3_4.setFont(font)
            self.label_3_4.setObjectName("label_3_4")

            self.textEdit_3_1 = QtWidgets.QTextEdit(self.centralwidget)
            self.textEdit_3_1.setGeometry(QtCore.QRect(480, 140, 400, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            self.textEdit_3_1.setFont(font)
            self.textEdit_3_1.setObjectName("textEdit_3_1")

            self.pushButton_3_2 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3_2.setGeometry(QtCore.QRect(470, 210, 130, 75))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_3_2.setFont(font)
            self.pushButton_3_2.clicked.connect(dob)
            self.pushButton_3_2.setObjectName("pushButton_3_2")

            self.pushButton_3_3 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3_3.setGeometry(QtCore.QRect(620, 210, 130, 75))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_3_3.setFont(font)
            self.pushButton_3_3.clicked.connect(prav)
            self.pushButton_3_3.setObjectName("pushButton_3_3")

            self.pushButton_3_4 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3_4.setGeometry(QtCore.QRect(770, 210, 130, 75))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_3_4.setFont(font)
            self.pushButton_3_4.clicked.connect(yda)
            self.pushButton_3_4.setObjectName("pushButton_3_4")

            self.label_3_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_3_5.setGeometry(QtCore.QRect(20, 620, 470, 50))
            font = QtGui.QFont()
            font.setFamily("Segoe Script")
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.label_3_5.setFont(font)
            self.label_3_5.setObjectName("label_3_5")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 940, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if SLOI == 1:
            MainWindow.setWindowTitle(_translate("MainWindow", "составление расписания"))
        elif SLOI == 2:
            MainWindow.setWindowTitle(_translate("MainWindow", "создание базы "))
        elif SLOI == 3:
            MainWindow.setWindowTitle(_translate("MainWindow", "корректировка штата"))

        self.label_3.setText(_translate("MainWindow", "СПб ГБУК «Санкт-Петербургский\n                музей *****»"))
        self.label_11.setText(_translate("MainWindow", "разработчик Тарасов Д. Л."))
        if SLOI != 2:
            self.pushButton.setText(_translate("MainWindow", "создание базы"))
        if SLOI != 3:
            self.pushButton_2.setText(_translate("MainWindow", "кадровые изменения"))
        if SLOI != 1:
            self.pushButton_3.setText(_translate("MainWindow", "создание расписания"))

        if SLOI == 1:
            self.label_1_2.setText(_translate("MainWindow", "сотрудники:"))
            self.label_1_10.setText(_translate("MainWindow", "черновик:"))
            j = 0
            for i in self.sp:
                i.setText(_translate("MainWindow", spis_sot[j][1]))
                j += 1
            self.label_1_4.setText(_translate("MainWindow", "на сколько дней расписание:"))
            self.label_1_5.setText(_translate("MainWindow", ohi))#"тех. строка******************************"
            self.label_1_6.setText(_translate("MainWindow", "всё\nок:"))
            self.pushButton_1_1.setText(_translate("MainWindow", "составить"))
            self.pushButton_1_2.setText(_translate("MainWindow", "для печати"))
            self.pushButton_1_3.setText(_translate("MainWindow", "сохранить*"))
            self.label_1_1.setText(_translate("MainWindow", "* необходимо для"
                                                            "\n корректного составления\n расписания в будующем."))

        elif SLOI == 2:
            self.label_2_1.setText(_translate("MainWindow", "всего залов:"))
            self.label_2_2.setText(_translate("MainWindow", "сотрудники  (каждого вводить с новой строки):"))

            self.label_2_4.setText(_translate("MainWindow", "залы могут быть закрыты:"))
            self.label_2_5.setText(_translate("MainWindow", "залы могут быть объедены:"))
            self.label_2_6.setText(_translate("MainWindow", "и"))
            self.label_2_7.setText(_translate("MainWindow", "и"))
            self.label_2_9.setText(_translate("MainWindow", "и"))
            self.label_2_8.setText(_translate("MainWindow", "и"))
            self.label_2_10.setText(_translate("MainWindow", "черновик:"))

            self.pushButton_2_1.setText(_translate("MainWindow", "составить"))
            self.pushButton_2_2.setText(_translate("MainWindow", "сохранить"))
            self.label_2_12.setText(_translate("MainWindow", ohi)) #"тех. строка*************************************"
        elif SLOI == 3:
            self.label_3_2.setText(_translate("MainWindow", "сотрудники:"))
            self.label_3_10.setText(_translate("MainWindow", "черновик:"))
            self.pushButton_3_1.setText(_translate("MainWindow", "сохранить"))
            j = 0
            for i in self.sp_3:
                i.setText(_translate("MainWindow", spis_sot[j][1]))
                j += 1
            self.label_3_4.setText(_translate("MainWindow", "заменить (если сотрудник отмечен), либо добавить:"))
            self.pushButton_3_2.setText(_translate("MainWindow", "добавить"))
            self.pushButton_3_3.setText(_translate("MainWindow", "заменить"))
            self.pushButton_3_4.setText(_translate("MainWindow", "удалить"))
            self.label_3_5.setText(_translate("MainWindow", ohi))  #"тех. строка*************************************"



# кнопки слоёв.
####################################################################################################################
def slo_1():
    'третья кнопка. составление расписания.'
    global SLOI, ohi
    ohi = ""
    SLOI = 1
    ui.setupUi(MainWindow)

def slo_2():
    'перая кнопка. составление базы.'
    global SLOI, ohi
    ohi = ""
    SLOI = 2
    ui.setupUi(MainWindow)

def slo_3():
    'вторая кнопка. кадровые изменения'
    global SLOI, ohi
    ohi = ""
    SLOI = 3
    ui.setupUi(MainWindow)
###################################################################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
