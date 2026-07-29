from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO
from scanner.detector import analyze_url
import shared
import time
from utils.terminal_stream import init_terminal_stream


app = Flask(__name__)

socketio = SocketIO(
    app,
    async_mode="threading"
)

init_terminal_stream(socketio)

# ===========================
# Worker Function
# ===========================

def run_pipeline(url):

    print("🚀 Scan Started")

    print("Testing stdout...")
    print("Loading WHOIS...")
    print("Launching Playwright...")

    shared.submitted_url = url

    try:

        import importlib
        import utils.features

        print("✅ Scan Finished")

        # Tell the client the pipeline is done so it can move on to the
        # threat_score page. scanner_pipeline.html needs a small listener
        # for this (see note below) since it isn't one of the files I have.
        socketio.emit("pipeline_complete", {"redirect": "/threat_score"})

    except Exception as e:

        import traceback

        print("❌ Pipeline Error")

        traceback.print_exc()

        socketio.emit("pipeline_complete", {"redirect": "/threat_score"})

# ===========================
# Routes
# ===========================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        url = request.form["url"]
        print("URL RECEIVED:", url)

        socketio.start_background_task(
            run_pipeline,
            url
        )

        return render_template("scanner_pipeline.html")

    return render_template("project_module_1.html")
    

@app.route("/reports/analysis_report.json")
def analysis_report():

    return send_from_directory(

        "reports",

        "analysis_report.json"

    )

@app.route("/threat_score")
def threat():

    return render_template("threat_score.html")

@app.route("/reports/threat_score.json")
def threat_score():

    return send_from_directory(

        "reports",

        "threat_score.json"

    )
    

@app.route("/theatrics")
def theatrics():

    return render_template("theatrics.html")

@app.route("/reports/threat_chart.json")
def threat_chart():

    return send_from_directory(

        "reports",

        "threat_chart.json"

    )

@app.route("/reports/sus_features.json")
def sus_features():
    return send_from_directory(
        "reports",
        "sus_features.json"
    )
    
@app.route("/suspicious")
def suspicious():
    return render_template("suspicious.html")    

@app.route("/reports/command_center.json")
def command_center_json():
    return send_from_directory(
        "reports",
        "command_center.json"
    )

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

from flask import send_from_directory

@app.route("/reports/images/<path:filename>")
def report_images(filename):
    return send_from_directory("reports/images", filename)

@app.route("/reports/master_report.txt")
def master_report():
    return send_from_directory(
        "reports",
        "master_report.txt"
    )

@app.route("/reports/primary_verdict.txt")
def primary_verdict():
    return send_from_directory(
        "reports",
        "primary_verdict.txt"
    )

@app.route("/reports/runtime_verdict.txt")
def runtime_verdict():
    return send_from_directory(
        "reports",
        "runtime_verdict.txt"
    )

@app.route("/reports")
def reports_page():
    return render_template("reports.html")

@app.route("/investigation")
def investigation():
    return render_template("investigationHub.html")

@app.route("/storage/runtime_dump.txt")
def download_runtime_dump():
    return send_from_directory(
        "storage",
        "runtime_dump.txt",
        as_attachment=True
    )

@app.route("/storage/screenshot_dump.txt")
def download_screenshot_dump():
    return send_from_directory(
        "storage",
        "screenshot_dump.txt",
        as_attachment=True
    )

@app.route("/storage/dataset_dump.txt")
def download_dataset_dump():
    return send_from_directory(
        "storage",
        "dataset_dump.txt",
        as_attachment=True
    )

if __name__ == "__main__":
    socketio.run(app, debug=False)

