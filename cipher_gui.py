"""Cipher Graphical User Interface Module"""

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from cipher import decrypt, encrypt

Form, _ = uic.loadUiType("cipher.ui")


class CipherWindow(QMainWindow, Form):
    """Cipher program GUI window"""
    def __init__(self):
        """Window init method"""
        super().__init__()
        self.setupUi(self)

        # Set fields for more flexible cipher mode change
        self.encrypt_func = encrypt
        self.decrypt_func = decrypt

        # Add signals to buttons
        self.encryptButton.clicked.connect(self.encrypt_signal)
        self.decryptButton.clicked.connect(self.decrypt_signal)

        # Add signals to radio buttons
        self.basicRadio.toggled.connect(self.change_mode)
        self.enhancedRadio.toggled.connect(self.change_mode)

        self.show()

    def change_mode(self):
        """Change encryption mode"""
        if self.basicRadio.isChecked():
            self.encrypt_func = encrypt
        elif self.enhancedRadio.isChecked():
            self.encrypt_func = lambda *args: encrypt(*args, transform=True)

    def encrypt_signal(self):
        """Encryption GUI logic"""
        # Get text from input text field
        text = self.inputEdit.toPlainText()

        # Check text input
        if len(text) == 0:
            self.statusbar.showMessage('Empty input')
            return

        # Encrypt
        key, ciphertext = self.encrypt_func(text)

        # Show result in key and output text fields
        self.keyEdit.setPlainText(key)
        self.outputEdit.setPlainText(ciphertext)

        # Set status
        self.statusBar().showMessage(f'Encryption successful!')

    def decrypt_signal(self):
        """Decryption GUI logic"""
        # Get text and key from input and key text fields
        text = self.inputEdit.toPlainText()
        key = self.keyEdit.toPlainText()

        # Check text and key input
        if len(text) == 0:
            self.statusbar.showMessage('Empty input')
            return
        if len(key) == 0:
            self.statusbar.showMessage('Empty key')
            return

        # Decryption
        # Plaintext can contain decrypted message or error message
        status, plaintext = self.decrypt_func(text, key)

        # Set status and show result
        if status:
            self.outputEdit.setPlainText(plaintext)
            self.statusBar().showMessage(f'Decryption successful!')
        else:
            self.statusBar().showMessage(f'Failed to decrypt: {plaintext}')


def main():
    """GUI startup function"""
    app = QApplication(sys.argv)
    window = CipherWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
