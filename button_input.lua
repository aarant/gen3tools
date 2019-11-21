-- Input a binary file as buttons, one byte per frame

function encode(b)
  pad = joypad.get()
  for i, _ in pairs(pad) do
    pad[i] = "False"
  end
  pad["L"] = "True"
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
f = assert(io.open("input.bin", "rb"))
data = f:read("*all")
for b in string.gmatch(data, ".") do encode(string.byte(b)) end
tastudio.setrecording(false)
