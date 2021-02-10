import sys
import os.path

from PyQt5 import QtCore, QtGui, QtWidgets

from base_gui import Ui_MainWindow
from pokemon import perms, BoxMon, Substruct0, Substruct1, Substruct2, Substruct3
from seed import seed_at, cycles_to, r_nature, seeds, rand, battle_seeds, acc_calc, crit_dmg_calc, wild_mons
from charmap import decode_str


MON_FIELDS = tuple(tup[0] for tup in BoxMon._fields_ if tup[0] not in ('markings', 'unknown', 'unused', 'secure'))
SUB0_FIELDS = tuple(tup[0] for tup in Substruct0._fields_)
SUB1_FIELDS = ('move0', 'move1', 'move2', 'move3', 'pp0', 'pp1', 'pp2', 'pp3')
SUB2_FIELDS = tuple(tup[0] for tup in Substruct2._fields_)
# TODO: Support pokeBall, IVs, altAbility
SUB3_FIELDS = tuple(tup[0] for tup in Substruct3._fields_ if tup[0] not in ('unk', 'isEgg', 'pokeBall', 'altAbility')) + ('isEgg_3',)
IV_FIELDS = ('hpIV', 'attackIV', 'defenseIV', 'spAttackIV', 'spDefenseIV', 'speedIV')

raw_re = QtCore.QRegExp(r'[A-Fa-f0-9]{160}')  # Exactly 80 hex bytes


def field_closure(field, func):
    def closed(*args, **kwargs):  # TODO: functools
        return func(field, *args, **kwargs)
    return closed


class GuiWindow(Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.old_cycle = 0
        self.encrypted = False
        self.mon = BoxMon()
        self.last_mon_dir = os.path.expanduser('~')

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        self.tabWidget.currentChanged.connect(self.switch_tabs)
        self.openAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('folder'), '&Open...')
        self.openAction.setShortcut('Ctrl+O')
        self.menuFile.addAction(self.openAction)
        self.saveAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('document-save-as'), '&Save as...')
        self.saveAction.setShortcut('Ctrl+S')
        self.menuFile.addAction(self.saveAction)
        self.switch_tabs()
        # Setup RNG search
        self.rng.editingFinished.connect(self.rng_changed)
        self.cycle.valueChanged.connect(self.cycle_changed)
        self.cycle.editingFinished.connect(self.update_table)
        # Link fields with frame table
        for name in ('limit', 'move_acc', 'acc_stage', 'evade', 'min_dmg', 'chance', 'slots', 'rate'):
            getattr(self, name).editingFinished.connect(self.update_table)
        for tri in ('hit', 'crit', 'quick_claw'):  # Set tristates
            getattr(self, tri).setCheckState(1)
        for field in ('hit', 'crit', 'quick_claw', 'diff', 'bike'):  # Link checkboxes with frame table
            getattr(self, field).stateChanged.connect(self.update_table)
        self.tabWidget_3.currentChanged.connect(self.update_table)  # Switching tabs updates table
        self.frameTable.cellDoubleClicked.connect(self.cell_clicked)  # Link double click to frame table
        # Pokemon tab
        self.raw.setValidator(QtGui.QRegExpValidator(raw_re, self.raw))
        self.raw.editingFinished.connect(self.load_raw)
        self.pid.editingFinished.connect(self.update_pid)
        self.checksum.valueChanged.connect(self.check_legal)
        for hex_field in ('species', 'heldItem', 'move0', 'move1', 'move2', 'move3'):
            getattr(self, hex_field).valueChanged.connect(field_closure(hex_field, self.update_hex_box))
        for field in MON_FIELDS + SUB0_FIELDS + SUB1_FIELDS + SUB2_FIELDS + SUB3_FIELDS:
            if field in ('personality',):
                continue
            try:
                getattr(self, field).editingFinished.connect(field_closure(field, self.update_raw))
            except AttributeError:
                getattr(self, field).stateChanged.connect(field_closure(field, self.update_raw))
        action = QtWidgets.QAction('Corrupt PID', self.toolButton)
        action.triggered.connect(field_closure('pid', self.corrupt_id))
        self.toolButton.addAction(action)
        action = QtWidgets.QAction('Corrupt OTID', self.toolButton)
        action.triggered.connect(field_closure('otId', self.corrupt_id))
        self.toolButton.addAction(action)
        action = QtWidgets.QAction('Make legal', self.toolButton)
        action.triggered.connect(self.make_legal)
        self.toolButton.addAction(action)

    def rng_changed(self):
        self.old_cycle = None

    def cycle_changed(self, value):
        if self.old_cycle is None:
            self.old_cycle = value
            return
        seed = int(self.rng.text(), 16) if self.rng.text() else 0
        if value > self.old_cycle:  # Advance RNG
            seed = next(seeds(seed, value-self.old_cycle, 1))
            self.rng.setText(f'{seed:08X}')
        elif value < self.old_cycle:  # Reverse RNG
            for _ in range(self.old_cycle-value):
                seed = 0xffffffff & (seed - 0x6073) * 0xeeb9eb65
            self.rng.setText(f'{seed:08X}')
        self.old_cycle = value

    def switch_tabs(self, *args, **kwargs):
        tab = self.tabWidget.currentWidget()
        if tab is self.rngTab:
            self.openAction.setEnabled(False)
            self.saveAction.setEnabled(False)
        elif tab is self.pokemonTab:
            self.openAction.setEnabled(True)
            self.saveAction.setEnabled(True)
            try:
                self.openAction.disconnect()
            except:
                pass
            self.openAction.triggered.connect(self.open_mon)
            try:
                self.saveAction.disconnect()
            except:
                pass
            self.saveAction.triggered.connect(self.save_mon)

    def update_table(self, *args, **kwargs):
        self.frameTable.clearContents()
        self.frameTable.setRowCount(0)
        currentTab = self.tabWidget_3.currentWidget()
        self.cycle.setSingleStep(currentTab.property('step_cycles'))
        if currentTab is self.acc_tab:
            self.acc_table()
        elif currentTab is self.crit_tab:
            self.crit_table()
        elif currentTab is self.quick_tab:
            self.quick_table()
        else:
            self.wild_table()

    def acc_table(self):
        seed = int(self.rng.text(), 16) if self.rng.text() else 0
        hit_filter = self.hit.checkState()
        table = self.frameTable
        table.horizontalHeaderItem(3).setText('Hit')
        table.horizontalHeaderItem(4).setText('Acc')
        offset = 3  # 2 frames are skipped
        for i, base in enumerate(battle_seeds(seed, limit=self.limit.value())):
            rng = rand(base, offset)
            hit, acc = acc_calc(rng, self.acc_stage.value(), self.evade.value(), self.move_acc.value())
            if hit_filter == 0 and hit or hit_filter == 2 and not hit:
                continue
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{base:08X}'))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{2*i+self.cycle.value()}'))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{i}'))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem("Yes" if hit else "No"))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{acc:03d}'))

    def cell_clicked(self, row, column):
        item = self.frameTable.item(row, 1)
        if item is None:
            return
        try:
            self.cycle.setValue(int(item.text(), base=10))
        except ValueError:
            pass

    def crit_table(self):
        seed = int(self.rng.text(), 16) if self.rng.text() else 0
        crit_filter, min_dmg, chance = self.crit.checkState(), self.min_dmg.value(), self.chance.value()
        table = self.frameTable
        table.horizontalHeaderItem(3).setText('Crit')
        table.horizontalHeaderItem(4).setText('Damage')
        offset = 3  # 2 frames are skipped
        for i, base in enumerate(battle_seeds(seed, limit=self.limit.value())):
            rng = rand(base, offset)
            crit, dmg = crit_dmg_calc(rng, chance)  # TODO: Add chance
            if crit_filter == 0 and crit or crit_filter == 2 and not crit:
                continue
            elif dmg < min_dmg:
                continue
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{base:08X}'))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{2*i+self.cycle.value()}'))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{i}'))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem("Yes" if crit else "No"))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{dmg:03d}'))

    def quick_table(self):
        seed = int(self.rng.text(), 16) if self.rng.text() else 0
        quick_filter = self.quick_claw.checkState()
        table = self.frameTable
        table.horizontalHeaderItem(3).setText('Quick')
        table.horizontalHeaderItem(4).setText('Value')
        offset = 0
        for i, base in enumerate(battle_seeds(seed, limit=self.limit.value())):
            rng = rand(base, offset)
            value = next(rng)
            quick = value < 0x3333
            if quick_filter == 0 and quick or quick_filter == 2 and not quick:
                continue
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{base:08X}'))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{2*i+self.cycle.value()}'))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{i}'))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem("Yes" if quick else "No"))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{value:04X}'))

    def wild_table(self):
        seed = int(self.rng.text(), 16) if self.rng.text() else 0
        diff = self.diff.checkState() != 0
        bike = self.bike.checkState() != 0
        if self.slots.text():
            slots = {int(s.strip()) for s in self.slots.text().split(',')}
        else:
            slots = None
        table = self.frameTable
        table.horizontalHeaderItem(3).setText('Slot')
        table.horizontalHeaderItem(4).setText('PID')
        for i, base, slot, pid in wild_mons(seed, rate=self.rate.value(), diff=diff, bike=bike, slots=slots):
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{base:08X}'))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{i+self.cycle.value()}'))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{i}'))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{slot}'))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{pid:08X}'))

    def load_raw(self):
        buffer = bytearray.fromhex(self.raw.text())
        self.mon = BoxMon.from_buffer(buffer)
        self.encrypted = True
        self.show_mon()

    def open_mon(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        tup = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open pokemon', options=options,
                                                    directory=self.last_mon_dir,
                                                    filter='Decrypted pokemon (*.pkm *.pk3);;Binary file (*)')
        path, filetype = tup
        if not path:
            return
        self.last_mon_dir = os.path.dirname(path)
        with open(path, 'rb') as f:
            buffer = f.read(80)
        if len(buffer) != 80:  # TODO: Show alert
            return
        buffer = bytearray(buffer[:80])
        if '*.pk3' in filetype:  # Convert PKHeX .pk3
            self.mon = BoxMon.from_pk3(buffer)
        else:
            self.mon = BoxMon.from_buffer(buffer)
        # Test if mon is already decrypted
        self.encrypted = not (self.mon.checksum == self.mon.calc_checksum())  # If equal, mon is already decrypted
        self.show_mon()

    def save_mon(self):  # Save pokemon to file
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        tup = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, 'Save pokemon', options=options,
                                                    directory=self.last_mon_dir,
                                                    filter='PKHeX pokemon (*.pk3);;Encrypted pokemon (*.bin)')
        path, filetype = tup
        if not path:
            return
        self.last_mon_dir = os.path.dirname(path)
        base, ext = os.path.splitext(path)
        if not ext:  # Pick ext from filetype
            if '*.pk3' in filetype:
                path = base + '.pk3'
            else:
                path = base + '.bin'
        if '*.pk3' in filetype:
            # TODO: Process for PKHeX
            self.decrypt()
            buffer = self.mon.to_pk3()
        else:
            self.encrypt()
            buffer = bytes(self.mon)
        print(path)
        with open(path, 'wb') as f:
            f.write(buffer)

    def encrypt(self):
        if self.encrypted:
            return
        self.mon.encrypt()
        self.encrypted = True

    def decrypt(self):
        if not self.encrypted:
            return
        self.mon.decrypt()
        self.encrypted = False

    def substruct(self, n):  # Safe substructure access
        return self.mon.sub(n)

    def show_mon(self):
        mon = self.mon
        self.encrypt()  # Encrypt before displaying mon
        b = bytes(self.mon)
        h = ''.join('%02X' % x for x in b)
        self.raw.setText(h)
        self.pid.setText(f'{mon.personality:08X}')
        self.otId.setText(f'{mon.otId:08X}')
        self.nickname.setText(decode_str(mon.nickname))
        self.otName.setText(decode_str(mon.otName))
        self.language.setValue(mon.language)
        self.isBadEgg.setCheckState(mon.isBadEgg)
        self.isEgg.setCheckState(mon.isEgg)
        self.hasSpecies.setCheckState(mon.hasSpecies)
        self.checksum.setValue(mon.checksum)
        self.check_legal()
        self.decrypt()
        for i, pos in enumerate(perms[mon.personality % 24]):
            title = ['Growth', 'Attacks', 'EVs/Condition', 'Misc.'][i]
            self.tabWidget_2.setTabText(i, f'{title} [{pos}]')
        # Growth
        growth = self.substruct(0).type0
        for name in ('experience', 'friendship', 'heldItem', 'ppBonuses', 'species'):
            if name == 'experience':
                getattr(self, name).setText(str(getattr(growth, name)))
            else:
                getattr(self, name).setValue(getattr(growth, name))
        # Attacks
        attacks = self.substruct(1).type1
        for i, name in enumerate(('move0', 'move1', 'move2', 'move3')):
            getattr(self, name).setValue(attacks.moves[i])
        for i, name in enumerate(('pp0', 'pp1', 'pp2', 'pp3')):
            getattr(self, name).setValue(attacks.pp[i])
        # EVs & Condition
        evs = self.substruct(2).type2
        for name in SUB2_FIELDS:
            getattr(self, name).setValue(getattr(evs, name))
        # Miscellaneous
        misc = self.substruct(3).type3
        for name in ('pokerus', 'metLocation', 'metLevel', 'metGame', 'otGender',
                     'hpIV', 'attackIV', 'defenseIV', 'spAttackIV', 'spDefenseIV', 'speedIV'):
            getattr(self, name).setValue(getattr(misc, name))
        self.isEgg_3.setCheckState(misc.isEgg)

    def update_raw(self, name, *args):  # Updating any field updates the raw value
        field = getattr(self, name)
        # Get the value to set
        try:
            base = 16 if name in ('checksum', 'otId') else 10
            value = int(field.text(), base)
        except:
            try:
                value = field.value()
            except:
                value = field.checkState()
        self.decrypt()  # Decrypt before modifying fields
        if name in MON_FIELDS:
            setattr(self.mon, name, value)
        elif name in SUB0_FIELDS:  # Growth
            growth = self.substruct(0).type0
            setattr(growth, name, value)
        elif name in SUB1_FIELDS:  # Attacks
            attacks = self.substruct(1).type1
            index = int(name[-1])
            if 'move' in name:
                attacks.moves[index] = value
            else: # pp
                attacks.pp[index] = value
        elif name in SUB2_FIELDS:  # EVS/Condition
            evs = self.substruct(2).type2
            setattr(evs, name, value)
        elif name in SUB3_FIELDS:  # Misc
            misc = self.substruct(3).type3
            if name == 'isEgg_3':
                name = 'isEgg'
            setattr(misc, name, value)
        self.check_legal()
        self.encrypt()  # Encrypt before displaying
        h = ''.join('%02X' % x for x in bytes(self.mon))
        self.raw.setText(h)
        print(f'{name} Raw updated!')

    def update_hex_box(self, field, *args):  # Add hex prefix to spin boxes
        attr = getattr(self, field)
        value = attr.value()
        attr.setPrefix(f'(0x{value:X}) ')

    def update_pid(self):
        self.encrypt()  # Encrypt with old PID before changing
        pid = int(self.pid.text(), 16)
        self.mon.personality = pid
        self.show_mon()

    def check_legal(self):  # Display whether actual and calculated checksums match
        checksum = self.checksum.value()
        self.decrypt()  # Decrypt before calculating
        self.checksum.setPrefix('' if checksum == self.mon.calc_checksum() else '! ')

    def corrupt_id(self, name, *args):  # Corrupt PID/TID
        value = int(getattr(self, name).text(), 16)
        value ^= 0x40000000
        self.encrypt()  # Encrypt with old PID/TID
        if name == 'pid':
            self.mon.personality = value
        else:
            self.mon.otId = value
        self.show_mon()

    def make_legal(self):  # Force legality
        self.decrypt()  # Must decrypt before checksum calc
        self.checksum.setValue(self.mon.calc_checksum())
        self.update_raw('checksum')


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GuiWindow()
    ui.setupUi(MainWindow)
    ui.frameTable.clipboard = app.clipboard()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
