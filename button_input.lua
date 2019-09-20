instrs = {0x21004806,0x48066001,0x70012101,0xf0004805,0x4805f803,0x48054686,0x00004700,0x03002360,0x030027a0,0x0805ecb1,0x080004b3,0x081377a5}
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
