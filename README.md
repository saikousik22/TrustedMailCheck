# TrustedMailCheck

TrustedMailCheck is a Python-based secure mail verification system that uses **digital signatures** to ensure message authenticity and integrity. The goal is to detect any tampering of email attachments (like PDF files) and allow the receiver to automatically remove such messages if they're found to be invalid.

This project provides a **digital proof mechanism** for secure communication by combining cryptographic hashing with RSA encryption.

---

## 🔨 Project Working

### ✉️ Sender Side:

1. The user uploads a PDF file they want to send.
2. The SHA-256 hash of this PDF file is generated.
3. The sender's RSA **private key** is used to encrypt this hash, forming the **digital signature** and Make Sure to send the **Public Key** Before sending the mail to Receiver.
4. The email is then sent to the receiver with:

   * The PDF attachment
   * The generated digital signature

### 📥 Receiver Side:

1. The receiver runs the verification program which:

   * Connects to the Gmail inbox using IMAP
   * Fetches **unseen** messages
2. For each message:

   * It extracts the PDF, digital signature, and public key
   * Generates SHA-256 hash of the received PDF
   * Decrypts the digital signature using the **sender's public key** to get the original hash
   * Compares both hashes:

     * If same: **Valid message**
     * If different: **Tampered**
3. If tampered:

   * The receiver is prompted: "Mail is invalid. Do you want to delete it?"
   * If they accept, the message is **automatically moved to Trash**

---

## 👤 Inputs Required

### ✉️ Sender (via `sender/index.html`):

* Sender Email ID
* Receiver Email ID
* App Password
* PDF file to send

### 📥 Receiver (via `receiver/index.html`):

* Receiver Email ID
* App Password

---

## 🔐 Setting up App Password

To use Gmail SMTP/IMAP with third-party apps:

1. Enable 2-Step Verification for your Gmail account.
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Select **Mail** and your device type.
4. Click **Generate**, and copy the 16-digit password.
5. Use this app password instead of your actual Gmail password in the forms.

---

## ✨ Features

* Ensures data integrity using **SHA-256 hashing**
* Verifies sender identity using **RSA digital signatures**
* Automatically detects and handles tampered emails
* Uses system notifications and GUI prompts
* Automatically moves tampered messages to Trash upon confirmation
* Organized code with `sender/` and `receiver/` folders

---

## 📄 Tech Stack

* **Python 3.x**
* **RSA (PyCryptodome)**
* **SHA-256 Hashing**
* **Flask** (for web interface)
* **IMAPClient, pyzmail36** (for Gmail inbox access)
* **Plyer** (for cross-platform notifications)
* **Tkinter** (for GUI prompts)
* **HTML/CSS** (for sender/receiver interfaces)

---

## 📦 Clone & Run in Your System

### Step 1: Clone the repository

```bash
git clone https://github.com/saikousik22/TrustedMailCheck.git
cd TrustedMailCheck
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run Sender Side

```bash
cd sender
python app.py
```

Sender-side server will start. Then open `Sender_Index.html` in your browser and use the sender form.

### Step 4: Run Receiver Side

```bash
cd receiver
python app.py
```

Receiver-side server will start. Then open `Receiver_Index.html` in your browser and use the receiver form.

---

## 📽️ Demo

Note: The demo video is large and may not preview on GitHub.
📥 Click the link below to download the raw file and view it on your device.

https://github.com/saikousik22/TrustedMailCheck/blob/main/demo.mp4



## 📍 Contributions

Contributions are welcome! Please:

* Fork the repo
* Create a branch
* Make your changes
* Submit a Pull Request

---

## 💬 License

This project is licensed under the [MIT License](LICENSE).

---

## 🛠️ Contact

**Author**: Padarthi Sai Kousik

* GitHub: [@saikousik22](https://github.com/saikousik22)
* Email: [psaikousik@gmail.com](mailto:psaikousik@gmail.com)
