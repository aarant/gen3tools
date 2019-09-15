function showState()
  gui.cleartext()
  frame = emu.framecount()
  if frame >= 231382 then frame = 231382 end
  seconds = frame / 59.73
  minutes = seconds / 60
  seconds = seconds % 60
  hours = minutes / 60
  minutes = minutes % 60
  gui.text(0, 0, string.format("%06d %02d:%02d:%02d", frame, hours, minutes, seconds))
  if frame >= 231382 then return end
  rng = memory.read_u32_le(0x005ae0, "IWRAM")
  cycles = memory.read_u32_le(0x024664, "EWRAM")
  gui.text(0, 14, string.format("%06d %08X", cycles, rng))
  inBattle = memory.readbyte(0x002799, "IWRAM")
  if (inBattle == 2) then -- battle display
    hp = memory.read_u16_le(0x023DA8, "EWRAM")
    if hp ~= 0 then gui.text(0, 14*4+4, string.format("%d", hp), 0xff5ad684) end
    turn = memory.read_u16_le(0x023FD4, "EWRAM")
    if turn < 0x3333 then -- quick claw activates
      gui.text(0, 14*6, string.format("Turn: %04X", turn), 0xff5ad684)
    else
      gui.text(0, 14*6, string.format("Turn: %04X", turn))
    end
    dmg = memory.read_s16_le(0x023E94, "EWRAM")
    crit = memory.readbyte(0x023EB5, "EWRAM")
    if (crit > 1) then -- show as crit
      gui.text(0, 14*7, string.format("Dmg: %03d !", dmg), 0xff5ad684)
    else -- show normally
      gui.text(0, 14*7, string.format("Dmg: %03d", dmg))
    end
    flags = memory.readbyte(0x023F20, "EWRAM")
    if flags ~= 1 then -- Hit
      gui.text(0, 14*8, "Hit")
    else -- Miss
      gui.text(0, 14*8, "Miss", 0xffde6b5a)
    end
  else -- overworld display
    foePID = memory.read_u32_le(0x0243E8, "EWRAM")
    gui.text(0, 28, string.format("Foe: %08X", foePID))
    tile = memory.readbyte(0x037233, "EWRAM")
    gui.text(0, 14*3, string.format("Tile: %d", tile))
    instr = memory.read_u32_le(0x007cec, "IWRAM")
    gui.text(0, 14*4, string.format("Ins: %08X", instr))
  end
end
event.onframeend(showState)
