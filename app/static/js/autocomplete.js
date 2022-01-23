let statisticsContainer = document.querySelector(".statistics-container");
let searchInput = document.getElementById("input");
searchInput.addEventListener('input', filter_autoComplete);

let headerTotalConfirmed = document.getElementById("header-total-confirmed");
let totalConfirmed = document.getElementById("total-confirmed");
let totalDeaths = document.getElementById("total-deaths");
let totalRecovered = document.getElementById("total-recovered");

list_country();
function list_country() {
    statistics.sort((a, b) => a.statistics[0].confirmed === b.statistics[0].confirmed ? 0 : a.statistics[0].confirmed < b.statistics[0].confirmed || -1);

    let totalConfirmedCase = 0;
    let totalDeathsCase = 0;
    let totalRecoveredCase = 0;
    statistics.forEach(data => {
        totalConfirmedCase +=data.statistics[0].confirmed;
        totalDeathsCase +=data.statistics[0].deaths;
        totalRecoveredCase +=data.statistics[0].recovered;
        addCountry(data);
    });
    headerTotalConfirmed.innerText = totalConfirmedCase.toLocaleString();
    totalConfirmed.innerText = totalConfirmedCase.toLocaleString();
    totalDeaths.innerText = totalDeathsCase.toLocaleString();
    totalRecovered.innerText = totalRecoveredCase.toLocaleString();
}

function filter_autoComplete({target}) {
    statisticsContainer.innerHTML = ``;

    let data = target.value;
    if (data.length) {
        let filteredValues = autoComplete(data);
        filteredValues.forEach(value => {
            addCountry(value);
        });
    } else {
        list_country();
    }
}

function autoComplete(value) {
    return statistics.filter(data =>
        data.name.toLowerCase().includes(value.toLowerCase())
    )
}

function addCountry(data) {
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
    confirmedCount.innerText = data.statistics[0].confirmed.toLocaleString();

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
    deathsCount.innerText = data.statistics[0].deaths.toLocaleString();

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
    recoveredCount.innerText = data.statistics[0].recovered.toLocaleString();

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