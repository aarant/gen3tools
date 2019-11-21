SECTIONS {
    . = 0x0203d000;
    .text :
    ALIGN(4) {
        temp.o(.text);
    }
}
