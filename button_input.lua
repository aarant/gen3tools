instrs = {0x1D}

function encode(b)
  pad = joypad.get()
  for i, _ in pairs(pad) do
    pad[i] = "False"
  end
  if bit.band(b, 0x80) == 0 then pad["Down"] = "True" end
  if bit.band(b, 0x40) == 0 then pad["Up"] = "True" end
  if bit.band(b, 0x20) == 0 then pad["Left"] = "True" end
  if bit.band(b, 0x10) == 0 then pad["Right"] = "True" end
  if bit.band(b, 0x08) == 0 then pad["Start"] = "True" end
  if bit.band(b, 0x04) == 0 then pad["Select"] = "True" end
  if bit.band(b, 0x02) == 0 then pad["B"] = "True" end
  if bit.band(b, 0x01) == 0 then pad["A"] = "True" end
  joypad.set(pad)
  emu.frameadvance()
end

tastudio.setrecording(true)
for _, ins in ipairs(instrs) do
  b0 = ins
  encode(b0)
  b1 = bit.rshift(ins, 8)
  encode(b1)
  b2 = bit.rshift(ins, 16)
  encode(b2)
  b3 = bit.rshift(ins, 24)
  encode(b3)
end
tastudio.setrecording(false)
