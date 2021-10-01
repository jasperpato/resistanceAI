from flask import Flask, render_template, request, redirect, url_for
from baseline import BaselineAgent

app = Flask("Resistance")
agent = BaselineAgent()

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        if not request.form.get("players") or not request.form.get("number"):
            return render_template("index.html")
        number_of_players = int(request.form["players"])
        player_number = int(request.form["number"])
        spy_list = []
        for i in range(10):
            if request.form.get(str(i)):
                if i >= number_of_players:
                    return render_template("index.html")
                spy_list.append(i)
        if len(spy_list) == 0 or (len(spy_list) == agent.spy_count[number_of_players]
        and request.form.get(str(player_number))):
            agent.new_game(number_of_players, player_number, spy_list)
            return redirect("/propose")
    return render_template("index.html")

@app.route("/propose", methods=["GET", "POST"])
def propose():
    if request.method == "POST":
        if not request.form.get("leader"):
            return render_template("propose.html", round=agent.rounds_completed()+1)
        leader = int(request.form["leader"])
        if leader == agent.player_number:
            agent.propose_mission(agent.mission_sizes[agent.number_of_players],
            agent.fails_required[agent.number_of_players][agent.round()])
            return redirect("/proposition")
        else:
            pass
    return render_template("propose.html", round=agent.round())

@app.route("/proposition", methods=["GET"])
def proposition():
    return render_template("proposition.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)