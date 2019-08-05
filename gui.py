import sys

from base_gui import Ui_MainWindow
from pokemon import perms, BoxMon, Substruct0, Substruct1, Substruct2, Substruct3
from seed import seed_at, cycles_to, r_nature
from draw import save_spinda

from PyQt5 import QtCore, QtGui, QtWidgets

u32_exp = QtCore.QRegExp('[0-9a-fA-F]{1,8}')

MON_FIELDS = tuple(tup[0] for tup in BoxMon._fields_ if tup[0] not in ('markings', 'unknown', 'unused', 'secure',
                                                                       'hasSpecies', 'language'))
SUB0_FIELDS = tuple(tup[0] for tup in Substruct0._fields_)
SUB1_FIELDS = ('move0', 'move1', 'move2', 'move3', 'pp0', 'pp1', 'pp2', 'pp3')
SUB2_FIELDS = tuple(tup[0] for tup in Substruct2._fields_)
SUB3_FIELDS = tuple(tup[0] for tup in Substruct3._fields_ if tup[0] not in ('unk', 'isEgg')) + ('subIsEgg',)

pids = wild_pids = lambda *args, **kwargs: None


def slot_decorator(ui, field):
    def wrapper():
        return ui.update_mon_field(field)
    return wrapper


class GuiWindow(Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.mon = None

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)

        self.frame.editingFinished.connect(self.update_frame)
        self.seed.editingFinished.connect(self.update_seed)

        raw_ex = QtCore.QRegExp('[0-9a-fA-F]{160}')
        validator = QtGui.QRegExpValidator(raw_ex, self.raw)
        self.raw.setValidator(validator)
        validator = QtGui.QRegExpValidator(u32_exp, self.personality)
        self.personality.setValidator(validator)
        # Connect pokemon slots
        for field in ('raw',) + MON_FIELDS + SUB0_FIELDS + SUB1_FIELDS + SUB2_FIELDS + SUB3_FIELDS:
            getattr(self, field).editingFinished.connect(slot_decorator(self, field))
        self.legalButton.clicked.connect(self.force_legal)

        self.glitchButton.clicked.connect(self.glitch_move_update)

    def update_frame(self, frame=None):
        if frame is None:
            frame = int(self.frame.text())
        self.seed.setText('%08x' % seed_at(frame))
        self.seedPID.setText('%08x' % list(pids(frame=frame, limit=1))[0])
        self.wildPID.setText('%08x' % list(wild_pids(frame=frame, limit=1))[0])

    def update_seed(self):
        seed = int(self.seed.text(), base=16)
        frame = cycles_to(seed)
        self.frame.setText('%d' % frame)
        self.update_frame(frame=frame)

    def update_mon(self, encrypted=True):  # Update the pokemon display
        for k, v in self.mon.dump().items():
            if k in MON_FIELDS:
                getattr(self, k).setText(v)
        self.order.setText(str(perms[self.mon.personality%24]))
        if encrypted:
            self.mon.decrypt()
        # Substruct 0, Growth
        for k, v in self.mon.sub(0).type0.dump().items():
            getattr(self, k).setText(v)
        # Substruct 1, Attacks
        for k, v in self.mon.sub(1).type1.dump().items():
            getattr(self, k).setText(v)
        # Substruct 2, EVs and Condition
        for k, v in self.mon.sub(2).type2.dump().items():
            getattr(self, k).setText(v)
        # Substruct 3, Miscellaneous
        for k, v in self.mon.sub(3).type3.dump().items():
            if k == 'isEgg':
                self.subIsEgg.setText(v)
            elif k != 'unk':
                getattr(self, k).setText(v)
        if encrypted:
            self.mon.encrypt()

    def update_checksum(self, encrypted=True):
        if encrypted:
            self.mon.decrypt()
        self.statusbar.showMessage('Calculated checksum: %x' % self.mon.calc_checksum())
        if encrypted:
            self.mon.encrypt()

    def update_membank(self):  # Update the memory bank
        buffer = bytes(self.mon)
        for i in range(20):
            s = '%08X' % int.from_bytes(buffer[i*4:(i+1)*4], 'little')
            getattr(self, 'mem%s' % i).setText(s)

    def update_mon_field(self, field):  # Update the pokemon struct by a particular field
        if self.mon is None and field != 'raw':  # Generate a blank pokemon
            self.mon = BoxMon()
        field_text = getattr(self, field).text()
        if field_text == '':  # Treat empty fields as zero
            field_text = '0'

        if field == 'raw':  # Set up a new pokemon
            self.mon = BoxMon.from_buffer(bytearray.fromhex(field_text))
            self.mon.decrypt()
            self.update_mon(encrypted=False)
            self.update_checksum(encrypted=False)
            self.update_membank()
            self.mon.encrypt()
            self.raw.setText(bytes(self.mon).hex())
            return
        elif field in ('personality', 'otId', 'checksum'):  # Hex fields
            setattr(self.mon, field, int(field_text, base=16))
            if field in ('personality', 'otId'):  # Data could be reorganized, so update the whole pokemon
                self.mon.decrypt()
                self.update_mon(encrypted=False)
                self.update_checksum(encrypted=False)
                self.update_membank()
                self.mon.encrypt()
                self.raw.setText(bytes(self.mon).hex())
            return
        self.mon.decrypt()
        if field in MON_FIELDS:  # Other non-substructure fields
            setattr(self.mon, field, int(field_text))
        elif field in SUB0_FIELDS:  # Substruct 0 fields
            setattr(self.mon.sub(0).type0, field, int(field_text))
        elif field in SUB1_FIELDS:  # Substruct 1 fields
            if field[:2] == 'pp':
                index = int(field[2])
                self.mon.sub(1).type1.pp[index] = int(field_text)
            else:
                index = int(field[4])
                self.mon.sub(1).type1.moves[index] = int(field_text)
        elif field in SUB2_FIELDS:  # Substruct 2 fields
            setattr(self.mon.sub(2).type2, field, int(field_text))
        elif field == 'subIsEgg':
            self.mon.sub(3).type3.isEgg = int(field_text)
        else:  # Substruct 3 fields
            setattr(self.mon.sub(3).type3, field, int(field_text))

        self.update_checksum(encrypted=False)
        self.update_membank()
        self.mon.encrypt()
        self.raw.setText(bytes(self.mon).hex())

    def force_legal(self):
        if self.mon is None:
            return
        self.mon.decrypt()
        new_sum = self.mon.calc_checksum()
        self.mon.checksum = new_sum
        self.checksum.setText('%x' % new_sum)
        self.mon.encrypt()
        self.raw.setText(bytes(self.mon).hex())

    def glitch_move_update(self):
        if not self.aceID.text():
            otId = 0
        else:
            otId = int(self.aceID.text())
        offset = int(self.scentFrames.text())
        # for frame, pid in glitch_move(otId, frame=700+offset):
        #     self.spinda_update(frame)
        #     break

    def spinda_update(self, frame):
        offset = int(self.scentFrames.text())
        center_pid = None
        for i, wpid in enumerate(wild_pids(frame=frame-7, limit=14)):
            if i == 7:
                center_pid = wpid
            buffer = save_spinda(wpid)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(buffer.getbuffer())
            getattr(self, 'spinda%s' % i).setPixmap(pixmap)
            buffer.close()
        self.spindaPID.setText('%08x' % center_pid)
        self.spindaFrame.setText(str(frame-offset))
        self.spindaGender.setText('M' if (center_pid & 0xff) > 127 else 'F')
        self.spindaNature.setText(r_nature[center_pid % 25])

    def spinda_click(self):
        print('uhm')


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GuiWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
