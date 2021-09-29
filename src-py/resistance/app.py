from flask import Flask, render_template, request, redirect, url_for
from first_agent.first_agent import FirstAgent

app = Flask("Resistance")
agent = FirstAgent()
turn = 0

@app.route("/", methods=["GET", "POST"])
def main():
    if(request.method == "POST"):
        if not request.form.get["players"] or not request.form.get["number"]:
            return render_template("index.html")
        number_of_players = request.form["players"]
        player_number = request.form["number"]
        spy_list = []
        for i in range(10):
            if request.form.get[str(i)]:
                if request.form.get[str(i)] >= number_of_players:
                    return render_template("index.html")
                spy_list.append(i)
        if len(spy_list) == 0:
            return redirect("propose.html")
        if len(spy_list) == agent.spy_count[number_of_players] and request.form.get[str(player_number)]:
            return redirect("propose.html")
    return render_template("index.html")

@app.route("/propose", methods=["GET", "POST"])
def propose():
    return render_template("propose.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)