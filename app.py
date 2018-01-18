#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtGui, uic
from common.pydrs import SerialDRS
import serial
import glob
import sys

class TestFbpWindow(QWidget):

    def __init__(self, *args):
        super(TestFbpWindow, self).__init__(*args)
        uic.loadUi('wizard.ui', self)

        self._initialize_widgets()
        self._initialize_signals()
        self._list_serial_ports()

        self._current_ps_id = {'Fonte 1': 1, 'Fonte 2': 2, 'Fonte 3': 3,
                                'Fonte 4': 4, 'Todas': 5}
        self._bsmp_var = {'soft_intlk': 25, 'hard_intlk': 26, 'iload': 27,
                            'vload': 28, 'vdclink': 29, 'temp': 30}

        self._drs = SerialDRS()

    def _initialize_widgets(self):
        self.pb_disconnect.setEnabled(False)
        self.pb_off_1.setEnabled(False)
        self.pb_off_2.setEnabled(False)
        self.pb_off_3.setEnabled(False)
        self.pb_off_4.setEnabled(False)
        self.pb_close_loop_1.setEnabled(False)
        self.pb_close_loop_2.setEnabled(False)
        self.pb_close_loop_3.setEnabled(False)
        self.pb_close_loop_4.setEnabled(False)
        self.le_iload_1.setReadOnly(True)
        self.le_iload_2.setReadOnly(True)
        self.le_iload_3.setReadOnly(True)
        self.le_iload_4.setReadOnly(True)
        self.le_vload_1.setReadOnly(True)
        self.le_vload_2.setReadOnly(True)
        self.le_vload_3.setReadOnly(True)
        self.le_vload_4.setReadOnly(True)
        self.le_vdclink_1.setReadOnly(True)
        self.le_vdclink_2.setReadOnly(True)
        self.le_vdclink_3.setReadOnly(True)
        self.le_vdclink_4.setReadOnly(True)
        self.le_temp_1.setReadOnly(True)
        self.le_temp_2.setReadOnly(True)
        self.le_temp_3.setReadOnly(True)
        self.le_temp_4.setReadOnly(True)
        self.combo_iref_id.addItems(['Fonte 1', 'Fonte 2', 'Fonte 3',
                                    'Fonte 4', 'Todas'])
        self.combo_intlk_id.addItems(['Fonte 1', 'Fonte 2', 'Fonte 3',
                                    'Fonte 4'])

    def _initialize_signals(self):
        self.pb_connect.clicked.connect(self._connect_serial)
        self.pb_disconnect.clicked.connect(self._disconnect_serial)
        self.pb_on_1.clicked.connect(self._turn_on_1)
        self.pb_on_2.clicked.connect(self._turn_on_2)
        self.pb_on_3.clicked.connect(self._turn_on_3)
        self.pb_on_4.clicked.connect(self._turn_on_4)
        self.pb_off_1.clicked.connect(self._turn_off_1)
        self.pb_off_2.clicked.connect(self._turn_off_2)
        self.pb_off_3.clicked.connect(self._turn_off_3)
        self.pb_off_4.clicked.connect(self._turn_off_4)
        self.pb_open_loop_1.clicked.connect(self._open_loop_1)
        self.pb_open_loop_2.clicked.connect(self._open_loop_2)
        self.pb_open_loop_3.clicked.connect(self._open_loop_3)
        self.pb_open_loop_4.clicked.connect(self._open_loop_4)
        self.pb_close_loop_1.clicked.connect(self._close_loop_1)
        self.pb_close_loop_2.clicked.connect(self._close_loop_2)
        self.pb_close_loop_3.clicked.connect(self._close_loop_3)
        self.pb_close_loop_4.clicked.connect(self._close_loop_4)
        self.pb_send_iref.clicked.connect(self._send_iref)
        self.pb_read_intlk.clicked.connect(self._read_intlk)
        self.pb_reset_intlk.clicked.connect(self._reset_intlk)
        self.pb_iload_1.clicked.connect(self._read_iload_1)
        self.pb_iload_2.clicked.connect(self._read_iload_2)
        self.pb_iload_3.clicked.connect(self._read_iload_3)
        self.pb_iload_4.clicked.connect(self._read_iload_4)
        self.pb_vload_1.clicked.connect(self._read_vload_1)
        self.pb_vload_2.clicked.connect(self._read_vload_2)
        self.pb_vload_3.clicked.connect(self._read_vload_3)
        self.pb_vload_4.clicked.connect(self._read_vload_4)
        self.pb_vdclink_1.clicked.connect(self._read_vdclink_1)
        self.pb_vdclink_2.clicked.connect(self._read_vdclink_2)
        self.pb_vdclink_3.clicked.connect(self._read_vdclink_3)
        self.pb_vdclink_4.clicked.connect(self._read_vdclink_4)
        self.pb_temp_1.clicked.connect(self._read_temp_1)
        self.pb_temp_2.clicked.connect(self._read_temp_2)
        self.pb_temp_3.clicked.connect(self._read_temp_3)
        self.pb_temp_4.clicked.connect(self._read_temp_4)

    def _list_serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsuported platform')

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.combo_com.addItem(port)
            except (OSError, serial.SerialException):
                pass

    """*************************************************
    ******************* PyQt Slots *********************
    *************************************************"""
    @pyqtSlot()
    def _connect_serial(self):
        try:
            print('Entrou aqui')
            #port = combo_com.currentText()
            port = "/dev/virtualcom0"
            baud = '6000000'
            con = self._drs.Connect(port, baud)
            print(con)
            if con:
                self.pb_connect.setEnabled(False)
                self.pb_disconnect.setEnabled(True)
                self.combo_com.setEnabled(False)
            else:
                self.pb_disconnect.setEnabled(False)
                self.pb_connect.setEnabled(True)
                self.combo_com.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _disconnect_serial(self):
        try:
            self._drs.Disconnect()
            self.pb_disconnect.setEnabled(False)
            self.pb_connect.setEnabled(True)
            self.combo_com.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _turn_on_1(self):
        self._drs.SetSlaveAdd(1)
        try:
            self._drs.turn_on()
            self.pb_on_1.setEnabled(False)
            self.pb_off_1.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _turn_on_2(self):
        self._drs.SetSlaveAdd(2)
        try:
            self._drs.turn_on()
            self.pb_on_2.setEnabled(False)
            self.pb_off_2.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _turn_on_3(self):
        self._drs.SetSlaveAdd(3)
        try:
            self._drs.turn_on()
            self.pb_on_3.setEnabled(False)
            self.pb_off_3.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _turn_on_4(self):
        self._drs.SetSlaveAdd(4)
        try:
            self._drs.turn_on()
            self.pb_on_4.setEnabled(False)
            self.pb_off_4.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _turn_off_1(self):
        self._drs.SetSlaveAdd(1)
        try:
            self._drs.turn_off()
            self.pb_on_1.setEnabled(True)
            self.pb_off_2.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _turn_off_2(self):
        self._drs.SetSlaveAdd(2)
        self.pb_on_2.setEnabled(True)
        self.pb_off_2.setEnabled(False)
        try:
            self._drs.turn_off()
        except:
            pass

    @pyqtSlot()
    def _turn_off_3(self):
        self._drs.SetSlaveAdd(3)
        try:
            self._drs.turn_off()
            self.pb_on_3.setEnabled(True)
            self.pb_off_3.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _turn_off_4(self):
        self._drs.SetSlaveAdd(4)
        try:
            self._drs.turn_off()
            self.pb_on_4.setEnabled(True)
            self.pb_off_4.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _open_loop_1(self):
        self._drs.SetSlaveAdd(1)
        try:
            self._drs.open_loop()
            self.pb_open_loop_1.setEnabled(False)
            self.pb_close_loop_1.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _open_loop_2(self):
        self._drs.SetSlaveAdd(2)
        try:
            self._drs.open_loop()
            self.pb_open_loop_2.setEnabled(False)
            self.pb_close_loop_2.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _open_loop_3(self):
        self._drs.SetSlaveAdd(3)
        try:
            self._drs.open_loop()
            self.pb_open_loop_3.setEnabled(False)
            self.pb_close_loop_3.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _open_loop_4(self):
        self._drs.SetSlaveAdd(4)
        try:
            self._drs.open_loop()
            self.pb_open_loop_4.setEnabled(False)
            self.pb_close_loop_4.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def _close_loop_1(self):
        self._drs.SetSlaveAdd(1)
        try:
            self._drs.close_loop()
            self.pb_open_loop_1.setEnabled(True)
            self.pb_close_loop_1.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _close_loop_2(self):
        self._drs.SetSlaveAdd(2)
        try:
            self._drs.close_loop()
            self.pb_open_loop_2.setEnabled(True)
            self.pb_close_loop_2.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _close_loop_3(self):
        self._drs.SetSlaveAdd(3)
        try:
            self._drs.close_loop()
            self.pb_open_loop_3.setEnabled(True)
            self.pb_close_loop_3.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _close_loop_4(self):
        self._drs.SetSlaveAdd(4)
        try:
            self._drs.close_loop()
            self.pb_open_loop_4.setEnabled(True)
            self.pb_close_loop_4.setEnabled(False)
        except:
            pass

    @pyqtSlot()
    def _send_iref(self):
        ps = self.combo_iref_id.currentText()
        if ps == 'Todas':
            try:
                ref = float(self.le_iref.text())
                self._drs.set_slowref_fbp(ref)
            except:
                pass
        else:
            add = self._current_ps_id[ps]
            try:
                self._drs.SetSlaveAdd(add)
                ref = float(self.le_iref.text())
                self._drs.set_slowref(ref)
            except:
                pass

    @pyqtSlot()
    def _read_intlk(self):
        ps = self.combo_intlk_id.currentText()
        try:
            add = self._current_ps_id[ps]
            self._drs.SetSlaveAdd(add)
            i = self._drs.read_bsmp_variable(self._bsmp_var['hard_intlk'],
                                                            'uint16_t')
            self.le_iload_1.setText(str(i))
        except:
            pass

    @pyqtSlot()
    def _reset_intlk(self):
        ps = self.combo_intlk_id.currentText()
        try:
            add = self._current_ps_id[ps]
            self._drs.SetSlaveAdd(ps)
            intlk = self._drs.ResetInterlocks()
            self.le_intlk.clear()
        except:
            pass

    @pyqtSlot()
    def _read_iload_1(self):
        try:
            self._drs.SetSlaveAdd(1)
            i = self._drs.read_bsmp_variable(self._bsmp_var['iload'], 'float')
            self.le_iload_1.setText(str(i))
        except:
            pass

    @pyqtSlot()
    def _read_iload_2(self):
        try:
            self._drs.SetSlaveAdd(2)
            i = self._drs.read_bsmp_variable(self._bsmp_var['iload'], 'float')
            self.le_iload_2.setText(str(i))
        except:
            pass

    @pyqtSlot()
    def _read_iload_3(self):
        try:
            self._drs.SetSlaveAdd(3)
            i = self._drs.read_bsmp_variable(self._bsmp_var['iload'], 'float')
            self.le_iload_3.setText(str(i))
        except:
            pass

    @pyqtSlot()
    def _read_iload_4(self):
        try:
            self._drs.SetSlaveAdd(4)
            i = self._drs.read_bsmp_variable(self._bsmp_var['iload'], 'float')
            self.le_iload_4.setText(str(i))
        except:
            pass

    @pyqtSlot()
    def _read_vload_1(self):
        try:
            self._drs.SetSlaveAdd(1)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vload'], 'float')
            self.le_vload_1.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vload_2(self):
        try:
            self._drs.SetSlaveAdd(2)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vload'], 'float')
            self.le_vload_2.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vload_3(self):
        try:
            self._drs.SetSlaveAdd(3)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vload'], 'float')
            self.le_vload_3.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vload_4(self):
        try:
            self._drs.SetSlaveAdd(4)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vload'], 'float')
            self.le_vload_4.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vdclink_1(self):
        try:
            self._drs.SetSlaveAdd(1)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vdclink'], 'float')
            self.le_vdclink_1.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vdclink_2(self):
        try:
            self._drs.SetSlaveAdd(2)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vdclink'], 'float')
            self.le_vdclink_2.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vdclink_3(self):
        try:
            self._drs.SetSlaveAdd(3)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vdclink'], 'float')
            self.le_vdclink_3.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_vdclink_4(self):
        try:
            self._drs.SetSlaveAdd(4)
            v = self._drs.read_bsmp_variable(self._bsmp_var['vdclink'], 'float')
            self.le_vdclink_4.setText(str(v))
        except:
            pass

    @pyqtSlot()
    def _read_temp_1(self):
        try:
            self._drs.SetSlaveAdd(1)
            t = self._drs.read_bsmp_variable(self._bsmp_var['temp'], 'float')
            self.le_vdclink_1.setText(str(t))
        except:
            pass

    @pyqtSlot()
    def _read_temp_2(self):
        try:
            self._drs.SetSlaveAdd(2)
            t = self._drs.read_bsmp_variable(self._bsmp_var['temp'], 'float')
            self.le_vdclink_2.setText(str(t))
        except:
            pass

    @pyqtSlot()
    def _read_temp_3(self):
        try:
            self._drs.SetSlaveAdd(3)
            t = self._drs.read_bsmp_variable(self._bsmp_var['temp'], 'float')
            self.le_vdclink_3.setText(str(t))
        except:
            pass

    @pyqtSlot()
    def _read_temp_4(self):
        try:
            self._drs.SetSlaveAdd(4)
            t = self._drs.read_bsmp_variable(self._bsmp_var['temp'], 'float')
            self.le_vdclink_4.setText(str(t))
        except:
            pass

app = QApplication(sys.argv)
widget = TestFbpWindow()
widget.show()
sys.exit(app.exec_())
