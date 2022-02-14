/**
 * The below listener handles timeline event to load covid statistics for different time-periods.
 */
let dateSelector = document.getElementById("date-selector");
let loadingContainer = document.querySelector(".loading-container");
dateSelector.addEventListener("change", function() {
    loadingContainer.style.display = "block";
    fetch(`/statistics/${dateSelector.value}`)
        .then(res => res.json())
        .then(res => {
            renderStatistics(res.total_cases, res.country_statistics);
            loadMap();
            loadingContainer.style.display = "none";
        }).catch(err => {
            alert("Something went wrong");
            loadingContainer.style.display = "none";
        })
});