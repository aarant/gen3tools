-- Input a binary file as buttons, one byte per frame

buttons = {"Down", "Up", "Left", "Right", "Start", "Select", "B", "A", "L", "R"}

function encode(b)
  pad = joypad.get()
  pad = {}
  pad["L"] = true
  if bit.band(b, 0x80) == 0 then pad["Down"] = true end
  if bit.band(b, 0x40) == 0 then pad["Up"] = true end
  if bit.band(b, 0x20) == 0 then pad["Left"] = true end
  if bit.band(b, 0x10) == 0 then pad["Right"] = true end
  if bit.band(b, 0x08) == 0 then pad["Start"] = true end
  if bit.band(b, 0x04) == 0 then pad["Select"] = true end
  if bit.band(b, 0x02) == 0 then pad["B"] = true end
  if bit.band(b, 0x01) == 0 then pad["A"] = true end
  joypad.set(pad)
  -- setinput(pad)
  emu.frameadvance()
end

function setinput(input)
    --joypad.set(input)
    local inputString = "|    0,    0,    0,  100,"

    if input["Up"] == true then inputString = inputString .. "U" else inputString = inputString .. "." end
    if input["Down"] == true then inputString = inputString .. "D" else inputString = inputString .. "." end
    if input["Left"] == true then inputString = inputString .. "L" else inputString = inputString .. "." end
    if input["Right"] == true then inputString = inputString .. "R" else inputString = inputString .. "." end
    if input["Start"] == true then inputString = inputString .. "S" else inputString = inputString .. "." end
    if input["Select"] == true then inputString = inputString .. "s" else inputString = inputString .. "." end
    if input["B"] == true then inputString = inputString .. "B" else inputString = inputString .. "." end
    if input["A"] == true then inputString = inputString .. "A" else inputString = inputString .. "." end
    if input["L"] == true then inputString = inputString .. "L" else inputString = inputString .. "." end
    if input["R"] == true then inputString = inputString .. "R" else inputString = inputString .. "." end
    inputString = inputString .. "...|"
    joypad.setfrommnemonicstr(inputString)
end

tastudio.setrecording(true)
f = assert(io.open("input.bin", "rb"))
data = f:read("*all")
for b in string.gmatch(data, ".") do encode(string.byte(b)) end
tastudio.setrecording(false)
