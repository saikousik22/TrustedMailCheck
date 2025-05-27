from flask import Flask, request, jsonify
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# ----------- RSA key generation -----------
def generate_keys():
    if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
        print("RSA keys not found. Generating new keys...")
        key = RSA.generate(2048)
        with open("private_key.pem", "wb") as f:
            f.write(key.export_key())
        with open("public_key.pem", "wb") as f:
            f.write(key.publickey().export_key())
        print("Keys generated: private_key.pem and public_key.pem")
    else:
        print("RSA keys already exist. Skipping generation.")

# ----------- PDF signing -----------
def sign_pdf(pdf_path, private_key_path, signature_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    h = SHA256.new(data)
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    signature = pkcs1_15.new(private_key).sign(h)
    with open(signature_path, 'wb') as f:
        f.write(signature)
    print(f"PDF signed and signature saved to {signature_path}")

# ----------- Send email with attachments -----------
def send_email_with_attachments(sender_email, app_password, receiver_email, subject, body, attachments):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)

    for file_path in attachments:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)
    print("Email sent successfully!")

# ----------- Flask route -----------
@app.route('/send-signed-pdf', methods=['POST'])
def send_signed_pdf():
    try:
        # Get form data
        sender_email = request.form['sender_email']
        sender_password = request.form['sender_password']
        receiver_email = request.form['receiver_email']
        pdf_file = request.files['pdf_file']

        # Save uploaded PDF
        pdf_path = "uploaded.pdf"
        pdf_file.save(pdf_path)

        # Generate keys, sign PDF, send email
        generate_keys()
        private_key_file = "private_key.pem"
        signature_file = "document.sig"

        sign_pdf(pdf_path, private_key_file, signature_file)

        send_email_with_attachments(
            sender_email=sender_email,
            app_password=sender_password,
            receiver_email=receiver_email,
            subject="Signed PDF Document",
            body="Please find the digitally signed PDF and signature attached.",
            attachments=[pdf_path, signature_file]
        )

        # Cleanup temporary files
        os.remove(pdf_path)
        os.remove(signature_file)

        return jsonify({"status": "success", "message": "Email sent successfully!"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
