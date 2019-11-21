import sys

from base_gui import Ui_MainWindow
from pokemon import perms, BoxMon, Substruct0, Substruct1, Substruct2, Substruct3
from seed import seed_at, cycles_to, r_nature, seeds, rand, battle_seeds, acc_calc, crit_dmg_calc, wild_mons

from PyQt5 import QtCore, QtGui, QtWidgets

MON_FIELDS = tuple(tup[0] for tup in BoxMon._fields_ if tup[0] not in ('markings', 'unknown', 'unused', 'secure'))
SUB0_FIELDS = tuple(tup[0] for tup in Substruct0._fields_)
SUB1_FIELDS = ('move0', 'move1', 'move2', 'move3', 'pp0', 'pp1', 'pp2', 'pp3')
SUB2_FIELDS = tuple(tup[0] for tup in Substruct2._fields_)
SUB3_FIELDS = tuple(tup[0] for tup in Substruct3._fields_ if tup[0] not in ('unk', 'isEgg')) + ('isEgg_3',)
IV_FIELDS = ('hpIV', 'attackIV', 'defenseIV', 'spAttackIV', 'spDefenseIV', 'speedIV')

raw_re = QtCore.QRegExp(r'[A-Fa-f0-9]{160}')


class GuiWindow(Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.old_cycle = 0
        self.encrypted = True
        self.mon = BoxMon()

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
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
        # Setup pokemon fields
        self.raw.setValidator(QtGui.QRegExpValidator(raw_re, self.raw))

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
            slots = {int(s) for s in self.slots.text().split(',')}
        else:
            slots = None
        table = self.frameTable
        table.horizontalHeaderItem(3).setText('Slot')
        table.horizontalHeaderItem(4).setText('PID')
        for i, base, pid in wild_mons(seed, rate=self.rate.value(), diff=diff, bike=bike, slots=slots):
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{base:08X}'))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{i+self.cycle.value()}'))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{i}'))
            # TODO: Add Slot
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{pid:08X}'))


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GuiWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
