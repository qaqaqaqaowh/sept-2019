from braintree import BraintreeGateway, Configuration, Environment
import os
from flask import Flask, render_template, request, redirect

gateway = BraintreeGateway(Configuration(
        Environment.Sandbox,
        merchant_id=os.getenv("ID"),
        public_key=os.getenv("KEY"),
        private_key=os.getenv("SECRET")
    ))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", token=gateway.client_token.generate())

@app.route("/pay", methods=["POST"])
def pay():
    gateway.transaction.sale({
        "amount": "100.00",
        "payment_method_nonce": request.form['nonce'],
        "options": {
            "submit_for_settlement": True
        }
    })
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
