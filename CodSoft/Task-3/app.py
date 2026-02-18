from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_title = request.form.get("task")
        if task_title:
            tasks.append({"title": task_title, "done": False})
        return redirect(url_for("index"))

    return render_template("index.html", tasks=tasks)

@app.route("/complete/<int:task_id>")
def complete(task_id):
    tasks[task_id]["done"] = True
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks.pop(task_id)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        updated_task = request.form.get("task")
        tasks[task_id]["title"] = updated_task
        return redirect(url_for("index"))

    return render_template("edit.html", task=tasks[task_id], task_id=task_id)

if __name__ == "__main__":
    app.run(debug=True)
