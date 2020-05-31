-- HUD for Pokemon Emerald (J)
final_inp = 400000 -- final input frame

function readEnemy(n)
  local addr = 0x0243E8 + 100*n
  local s = string.format("foe%d.bin", n)
  gui.text(0, 14*14, s)
  local out = assert(io.open(s, "wb"))
  for i=0,79 do
    local b = memory.readbyte(addr + i, "EWRAM")
    out:write(string.char(b))
  end
  out:close()
end

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
    -- addr = memory.read_u32_le(0x007918, "IWRAM")
    -- gui.text(0, 14*2, string.format("Addr: %08X", addr))
    -- battler = memory.readbyte(0x023d08)
    -- buffer = 0x02022D08+0x200*battler
    -- battleMons = 0x02023d28+0x58*battler
    -- move = memory.read_u16_le(0x023E8E, "EWRAM")
    -- gui.text(0, 14*3, string.format("%08x %08x %04x", buffer, battleMons, move))
  else -- overworld display
    foePID = memory.read_u32_le(0x0243E8, "EWRAM")
    gui.text(0, 28, string.format("Foe: %08X", foePID))
    tile = memory.readbyte(0x037233, "EWRAM")
    gui.text(0, 14*3, string.format("Tile: %d", tile))
    gTrainerId = memory.read_u16_le(0x020000, "EWRAM")
    gSaveBlock2 = bit.band(memory.read_u32_le(0x5AF0, "IWRAM"), 0xFFFFFF)
    otId = memory.read_u32_le(gSaveBlock2+0xA, "EWRAM")
    gui.text(0, 14*4, string.format("ID: %04X %08X", gTrainerId, otId))
    mudkipPID = memory.read_u32_le(0x024190, "EWRAM")
    gui.text(0, 14*5, string.format("Mudkip: %08X", mudkipPID))
    gSaveBlock1 = bit.band(memory.read_u32_le(0x5aec, "IWRAM"), 0xFFFFFF)
    steps = memory.readbyte(gSaveBlock1+0x2F9C+0x1b0, "EWRAM")
    gui.text(0, 14*6, string.format("Steps: %02X", steps))
    -- addr = memory.read_u32_le(0x007918, "IWRAM")
    -- gui.text(0, 14*4, string.format("Addr: %08X", addr))
  end
end
for i=0,5 do readEnemy(i) end
event.onframeend(showState)
