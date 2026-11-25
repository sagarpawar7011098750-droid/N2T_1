// Box.asm for K = 63
// Start row = 63 -> Start address = 16384 + 32*63 = 18400
// Height = 20 rows, Width = (63 mod 4) + 1 = 4 words (64 pixels)

(MAIN_LOOP)
    @KBD
    D=M
    @SET_BLACK
    D;JNE           // If any key is pressed (KBD != 0), draw black

    @color
    M=0             // Otherwise set color = 0 (white)
    @DRAW_INIT
    0;JMP

(SET_BLACK)
    @color
    M=-1            // Set color = -1 (16 black pixels)

(DRAW_INIT)
    @18400          // SCREEN (16384) + 32 * 63
    D=A
    @rowAddr
    M=D             // rowAddr points to the start of the current row

    @20
    D=A
    @rowsLeft
    M=D             // Counter for 20 rows

(ROW_LOOP)
    @rowsLeft
    D=M
    @MAIN_LOOP
    D;JEQ           // If rowsLeft == 0, return to keyboard check

    // Fill 4 consecutive words (64 pixels) starting at rowAddr
    @rowAddr
    D=M
    @currWord
    M=D

    @4
    D=A
    @colsLeft
    M=D             // Counter for 4 words per row

(COL_LOOP)
    @colsLeft
    D=M
    @NEXT_ROW
    D;JEQ           // Done with the 4 words in this row

    @color
    D=M             // Load color (-1 or 0)
    @currWord
    A=M             // Dereference pointer to screen RAM
    M=D             // Write 16 pixels

    @currWord
    M=M+1           // Move 1 word (16 pixels) right
    @colsLeft
    M=M-1           // Decrement column counter
    @COL_LOOP
    0;JMP

(NEXT_ROW)
    @32
    D=A
    @rowAddr
    M=D+M           // Move down 1 row (+32 words in Hack screen memory)
    @rowsLeft
    M=M-1           // Decrement row counter
    @ROW_LOOP
    0;JMP