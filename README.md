# IS Lab #1
### Cipher program
Cipher program that encrypts and decrypts text using magic squares. 

Magic Squares are built using **Siamese method** (odd order) and **Generic Pattern** (doubly even order).

In addition, during encryption, Magic Squares can be randomly transformed with:
- 90° counter- and clockwise rotation
- Exchange of rows i and (n + 1 - i), columns i and (n + 1 - i) for (1 <= i <= n)
- Exchange of rows i and j, (n + 1 - i) and (n + 1 - j) for (i < j < (n + 1) / 2)
- Exchange of columns i and j, (n + 1 - i) and (n + 1 - j) for (i < j < (n + 1) / 2)

Information about Magic Squares was taken from the [Wikipedia Page](https://en.wikipedia.org/wiki/Magic_square).

Used third-party libraries: 
- PyQt5
- Numpy