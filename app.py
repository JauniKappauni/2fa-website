from flask import Flask, render_template, request
import qrcode
import pyotp
from io import BytesIO
import base64

app = Flask(__name__)

secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)
otp_url = totp.provisioning_uri(name="test", issuer_name="test")

qr = qrcode.make(otp_url)
buffer = BytesIO()
qr.save(buffer, format="PNG")
qr_base64 = base64.b64encode(buffer.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def function1():
    status = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if totp.verify(user_input):
            status = "✅"
        else:
            status = "❌"
    return render_template("index.html", status=status, qr_base64=qr_base64)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=20001, debug=True)