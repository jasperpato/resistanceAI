from flask import Flask, render_template

app = Flask("Resistance")
turn = 0

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/turn", methods=["get", "post"])
def turn():
    return render_template("turn.html")

app.run(host="0.0.0.0", debug=True)