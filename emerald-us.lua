-- HUD for Pokemon Emerald (J)
final_inp = 6000000 -- final input frame

function showState()
  gui.cleartext()
  frame = emu.framecount()
  if frame >= final_inp then frame = final_inp end
  seconds = frame / 59.73
  minutes = seconds / 60
  seconds = seconds % 60
  hours = minutes / 60
  minutes = minutes % 60
  gui.text(0, 0, string.format("%06d %02d:%02d:%02d", frame, hours, minutes, seconds))
  if frame >= final_inp then return end
  rng = memory.read_u32_le(0x05D80, "IWRAM")
  cycles = memory.read_u32_le(0x0249c0, "EWRAM")
  gui.text(0, 14, string.format("%06d %08X", cycles, rng))
  inBattle = memory.readbyte(0x002799, "IWRAM")
  inBattle = 0
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
    addr = memory.read_u32_le(0x007914, "IWRAM")
    gui.text(0, 14*2, string.format("Addr: %08X", addr))
  else -- overworld display
    foePID = memory.read_u32_le(0x024744, "EWRAM")
    gui.text(0, 28, string.format("Foe: %08X", foePID))
    tile = memory.readbyte(0x037593, "EWRAM")
    gui.text(0, 14*3, string.format("Tile: %d", tile))
    turn = memory.read_u16_le(0x024330, "EWRAM")
    if turn < 0x3333 then -- quick claw activates
      gui.text(0, 14*6, string.format("Turn: %04X", turn), 0xff5ad684)
    else
      gui.text(0, 14*6, string.format("Turn: %04X", turn))
    end
    -- mudkipPID = memory.read_u32_le(0x0244ec, "EWRAM")
    -- gui.text(0, 14*4, string.format("Mudkip: %08X", mudkipPID))
    -- addr = memory.read_u32_le(0x007914, "IWRAM")
    -- gui.text(0, 14*4, string.format("Addr: %08X", addr))
  end
end
event.onframeend(showState)
