from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import imapclient
import pyzmail
import tkinter as tk
from tkinter import messagebox
from plyer import notification

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DOWNLOAD_DIR = "downloads"
PUBLIC_KEY_FILE = "public_key.pem"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def notify_user(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def ask_delete_confirmation():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    result = messagebox.askyesno("Delete Confirmation", "Document is tampered! Do you want to move the email to Trash?")
    root.destroy()
    return result

def download_and_verify_email(email_address, app_password, imap_server='imap.gmail.com'):
    client = imapclient.IMAPClient(imap_server, ssl=True)
    client.login(email_address, app_password)
    client.select_folder('INBOX')

    messages = client.search(['UNSEEN'])

    for msgid in messages:
        raw_message = client.fetch(msgid, ['RFC822'])
        message = pyzmail.PyzMessage.factory(raw_message[msgid][b'RFC822'])

        attachments = []
        for part in message.mailparts:
            if part.filename:
                filepath = os.path.join(DOWNLOAD_DIR, part.filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload())
                attachments.append(filepath)
                print(f"Downloaded: {filepath}")

        pdf_files = [f for f in attachments if f.lower().endswith('.pdf')]
        sig_files = [f for f in attachments if f.lower().endswith('.sig')]

        if pdf_files and sig_files:
            with open(pdf_files[0], 'rb') as f:
                data = f.read()
            with open(sig_files[0], 'rb') as f:
                signature = f.read()
            with open(PUBLIC_KEY_FILE, 'rb') as f:
                public_key = RSA.import_key(f.read())

            h = SHA256.new(data)
            try:
                pkcs1_15.new(public_key).verify(h, signature)
                notify_user("Verification Successful", f"{os.path.basename(pdf_files[0])} is genuine!")
                print(f"[INFO] Document '{pdf_files[0]}' is VALID")
            except (ValueError, TypeError):
                notify_user("Verification Failed", f"{os.path.basename(pdf_files[0])} is tampered!")
                print(f"[WARNING] Document '{pdf_files[0]}' is INVALID")

                if ask_delete_confirmation():
                    client.move(msgid, '[Gmail]/Trash')
                    print("Email moved to Trash.")

    client.logout()

@app.route('/verify-emails', methods=['POST'])
def verify_emails_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email')
    app_password = data.get('app_password')

    if not email or not app_password:
        return jsonify({"error": "Email and app password are required"}), 400

    try:
        download_and_verify_email(email, app_password)
        return jsonify({"message": "Email verification process completed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
