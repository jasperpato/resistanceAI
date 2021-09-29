from flask import Flask, render_template, request, redirect
from first_agent import FirstAgent

app = Flask("Resistance")
agent = FirstAgent()
turn = 0

@app.route("/", methods=["GET", "POST"])
def main():
    if(request.method == "POST"):
        number_of_players = request.form["players"]
        

    return render_template("index.html")

@app.route("/propose", methods=["GET", "POST"])
def turn():
    return render_template("propose.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)