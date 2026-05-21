// ======================================================
// API ENDPOINT
// ======================================================

const DASHBOARD_API =
    "/api/dashboard";

// ======================================================
// LOAD DASHBOARD
// ======================================================

async function loadDashboard() {

    try {

        console.log(
            "📊 Loading dashboard..."
        );

        const response =
            await fetch(
                DASHBOARD_API
            );

        const data =
            await response.json();

        // ==============================================
        // VALIDATION
        // ==============================================

        if (!data.success) {

            console.error(
                "Dashboard fetch failed"
            );

            return;
        }

        // ==============================================
        // ANALYTICS
        // ==============================================

        const analytics =
            data.analytics;

        // ==============================================
        // POPULATE METRICS
        // ==============================================

        populateMetrics(
            analytics
        );

        // ==============================================
        // RENDER CHARTS
        // ==============================================

        renderEmotionChart(
            analytics.emotion_distribution
        );

        renderConfidenceChart(
            analytics.timeline
        );

        // ==============================================
        // RECENT ACTIVITY
        // ==============================================

        renderRecentActivity(
            analytics.recent_activity
        );

    } catch (error) {

        console.error(
            "Dashboard Error:",
            error
        );
    }
}

// ======================================================
// POPULATE METRICS
// ======================================================

function populateMetrics(
    analytics
) {

    document.getElementById(
        "total-messages"
    ).textContent =
        analytics.total_messages;

    document.getElementById(
        "dominant-emotion"
    ).textContent =
        capitalize(
            analytics.dominant_emotion
        );

    document.getElementById(
        "avg-confidence"
    ).textContent =
        analytics.avg_confidence;

    document.getElementById(
        "emotional-diversity"
    ).textContent =
        analytics.emotional_diversity;
}

// ======================================================
// EMOTION DISTRIBUTION CHART
// ======================================================

function renderEmotionChart(
    emotionData
) {

    const ctx =
        document.getElementById(
            "emotionChart"
        );

    new Chart(ctx, {

        type: "doughnut",

        data: {

            labels:
                Object.keys(
                    emotionData
                ),

            datasets: [{

                data:
                    Object.values(
                        emotionData
                    ),

                backgroundColor: [

                    "#4A90E2",
                    "#5CB85C",
                    "#EF4444",
                    "#F59E0B",
                    "#8B5CF6",
                    "#14B8A6",
                    "#94A3B8"
                ],

                borderWidth: 0
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"
                }
            }
        }
    });
}

// ======================================================
// CONFIDENCE TREND CHART
// ======================================================

function renderConfidenceChart(
    timeline
) {

    const ctx =
        document.getElementById(
            "confidenceChart"
        );

    const labels =
        timeline.map((_, index) =>

            `#${index + 1}`
        );

    const confidenceValues =
        timeline.map(item =>

            item.confidence
        );

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{

                label:
                    "Confidence",

                data:
                    confidenceValues,

                borderColor:
                    "#4A90E2",

                backgroundColor:
                    "rgba(74,144,226,0.15)",

                tension: 0.4,

                fill: true
            }]
        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 1
                }
            }
        }
    });
}

// ======================================================
// RECENT ACTIVITY
// ======================================================

function renderRecentActivity(
    activity
) {

    const container =
        document.getElementById(
            "recent-activity"
        );

    // ==============================================
    // EMPTY STATE
    // ==============================================

    if (!activity.length) {

        container.innerHTML = `

            <div class="empty-state">

                No recent activity found.

            </div>
        `;

        return;
    }

    // ==============================================
    // BUILD HTML
    // ==============================================

    let html = "";

    activity.forEach(item => {

        html += `

            <div class="activity-item">

                <div class="activity-emotion">

                    ${capitalize(item.emotion)}

                </div>

                <div class="activity-confidence">

                    Confidence:
                    ${Number(
                        item.confidence
                    ).toFixed(2)}

                </div>

                <div class="activity-date">

                    ${formatDate(
                        item.created_at
                    )}

                </div>

            </div>
        `;
    });

    container.innerHTML =
        html;
}

// ======================================================
// FORMAT DATE
// ======================================================

function formatDate(dateString) {

    const date =
        new Date(dateString);

    return date.toLocaleString();
}

// ======================================================
// CAPITALIZE
// ======================================================

function capitalize(text) {

    if (!text) {

        return "";
    }

    return (
        text.charAt(0)
        .toUpperCase()
        +
        text.slice(1)
    );
}

// ======================================================
// INITIALIZE
// ======================================================

loadDashboard();