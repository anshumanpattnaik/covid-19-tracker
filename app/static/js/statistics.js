let statisticsContainer = document.querySelector(".statistics-container");
let searchInput = document.getElementById("input");
let headerTotalConfirmed = document.getElementById("header-total-confirmed");
let totalConfirmed = document.getElementById("total-confirmed");
let totalDeaths = document.getElementById("total-deaths");
let totalRecovered = document.getElementById("total-recovered");

renderStatistics();

/**
 * This function renders all countries statistics
 */
function renderStatistics() {

    // Sorting statistics from higher confirmed cases to lower confirmed cases
    if(statistics[0].statistics.edges.length >= 1) {
        statistics.sort((a, b) => a.statistics.edges[0].node.confirmed === b.statistics.edges[0].node.confirmed ? 0 : a.statistics.edges[0].node.confirmed < b.statistics.edges[0].node.confirmed || -1);
    }

    statistics.forEach(data => {
        if(data.statistics.edges.length >= 1) {
            addCountryStatistics(data);
        }
    });
    headerTotalConfirmed.innerText = totalCases.totalConfirmed.toLocaleString();
    totalConfirmed.innerText = totalCases.totalConfirmed.toLocaleString();
    totalDeaths.innerText = totalCases.totalDeaths.toLocaleString();
    totalRecovered.innerText = totalCases.totalRecovered.toLocaleString();
}

searchInput.addEventListener('input', function (e) {
    // clear list
    statisticsContainer.innerHTML = ``;

    let data = e.target.value;
    if (data.length) {
        let filteredValues = filterStatistics(data);
        filteredValues.forEach(value => addCountryStatistics(value));
    } else {
        renderStatistics();
    }
});

/**
 * This function filters covid statistics by country name.
 * @param name is country name
 * @returns filtered statistics list.
 */
function filterStatistics(name) {
    return statistics.filter(data =>
        data.name.toLowerCase().includes(name.toLowerCase())
    )
}

/**
 * This function adds list of countries with the statistics to the parent container.
 * @param data contains country list with the covid statistics
 */
function addCountryStatistics(data) {
    let countryListContainer = document.createElement("div");
    countryListContainer.setAttribute("class", "country-list-container");

    let country = document.createElement("div");
    country.setAttribute("class", "country");

    let flag = document.createElement("img");
    flag.setAttribute("class", "flag");
    flag.src = data.flag;
    flag.loading = "lazy";

    let countryName = document.createElement("span");
    countryName.innerText = data.name;

    country.append(flag);
    country.append(countryName);

    // Confirmed Statistics
    let confirmedStatistics = document.createElement("div");
    confirmedStatistics.setAttribute("class", "statistics");

    let confirmedCount = document.createElement("span");
    confirmedCount.setAttribute("class", "count");
    confirmedCount.innerText = data.statistics.edges[0].node.confirmed.toLocaleString();

    let confirmedLabel = document.createElement("span");
    confirmedLabel.setAttribute("class", "label");
    confirmedLabel.innerText = "CONFIRMED";

    confirmedStatistics.append(confirmedCount);
    confirmedStatistics.append(confirmedLabel);

    // Deaths Statistics
    let deathsStatistics = document.createElement("div");
    deathsStatistics.setAttribute("class", "statistics");

    let deathsCount = document.createElement("span");
    deathsCount.setAttribute("class", "count");
    deathsCount.innerText = data.statistics.edges[0].node.deaths.toLocaleString();

    let deathsLabel = document.createElement("span");
    deathsLabel.setAttribute("class", "label");
    deathsLabel.innerText = "DEATHS";

    deathsStatistics.append(deathsCount);
    deathsStatistics.append(deathsLabel);

    // Recovered Statistics
    let recoveredStatistics = document.createElement("div");
    recoveredStatistics.setAttribute("class", "statistics");

    let recoveredCount = document.createElement("span");
    recoveredCount.setAttribute("class", "count");
    recoveredCount.innerText = data.statistics.edges[0].node.recovered.toLocaleString();

    let recoveredLabel = document.createElement("span");
    recoveredLabel.setAttribute("class", "label");
    recoveredLabel.innerText = "RECOVERED";

    recoveredStatistics.append(recoveredCount);
    recoveredStatistics.append(recoveredLabel);

    countryListContainer.append(country);
    countryListContainer.append(confirmedStatistics);
    countryListContainer.append(deathsStatistics);
    countryListContainer.append(recoveredStatistics);

    statisticsContainer.append(countryListContainer);
}