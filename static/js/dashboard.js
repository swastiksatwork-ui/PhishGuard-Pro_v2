async function loadDashboard() {

    try {

        const response = await fetch("/reports/analysis_report.json");

        const data = await response.json();

        console.log("Dashboard JSON Loaded");

        console.log(data);

        document.getElementById("overall-score").innerText =
        data.gauge.overall_score;

        document.getElementById("objective-score").innerText =
        data.gauge.objective_score;

        document.getElementById("subjective-score").innerText =
        data.gauge.subjective_score;

        document.getElementById("confidence-score").innerText =
        data.gauge.confidence + "%";

        document.getElementById("risk-level").innerText =
        data.gauge.risk_level;

    }

    catch(error){

        console.error(error);

    }

}

loadDashboard();