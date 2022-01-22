let statisticsContainer = document.querySelector(".statistics-container");
let searchInput = document.getElementById("input");
searchInput.addEventListener('input', filter_autoComplete);

list_country();
function list_country() {
    // statistics.sort((a, b) => parseFloat(a.statistics[0].confirmed) - parseFloat(b.statistics[0].confirmed));
    statistics.forEach(data => {
        add_country(data);
    });
}

function filter_autoComplete({target}) {
    statisticsContainer.innerHTML = ``;

    let data = target.value;
    if (data.length) {
        let filteredValues = autoComplete(data);
        filteredValues.forEach(value => {
            add_country(value);
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

function add_country(data) {
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
    confirmedCount.innerText = data.statistics[0].confirmed;

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
    deathsCount.innerText = data.statistics[0].deaths;

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
    recoveredCount.innerText = data.statistics[0].recovered;

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