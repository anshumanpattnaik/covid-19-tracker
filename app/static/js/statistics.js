let statisticsContainer = document.querySelector(".statistics-container");
let nrfContainer = document.querySelector(".nrf-container");
let searchInput = document.getElementById("input");
let headerTotalConfirmed = document.getElementById("header-total-confirmed");
let totalConfirmed = document.getElementById("total-confirmed");
let totalDeaths = document.getElementById("total-deaths");
let totalRecovered = document.getElementById("total-recovered");

let geoJSON = {}
renderStatistics(totalCases, statistics);

/**
 * This function renders all countries statistics
 */
function renderStatistics(totalCases, statistics) {
    statisticsContainer.innerHTML = ``;

    if(totalCases !== undefined && statistics !== undefined) {
        // Sorting statistics from higher confirmed cases to lower confirmed cases
        if(statistics[0].statistics.edges.length >= 1) {
            statistics.sort((a, b) => (a.statistics.edges.length >= 1 && b.statistics.edges.length >= 1) &&
                (a.statistics.edges[0].node.confirmed === b.statistics.edges[0].node.confirmed ? 0 :
                    a.statistics.edges[0].node.confirmed < b.statistics.edges[0].node.confirmed || -1));
        }
        let featuresData = []
        statistics.forEach(data => {
            if(data.statistics.edges.length >= 1) {
                featuresData.push({
                    type: "Feature",
                    geometry: {
                        type: "Point",
                        coordinates: data.coordinates
                    },
                    properties: {
                        popup_view: renderPopupView(data.name, data.flag, data.statistics.edges[0].node.confirmed,
                                                    data.statistics.edges[0].node.deaths),
                        confirmed: data.statistics.edges[0].node.confirmed,
                        deaths: data.statistics.edges[0].node.deaths,
                        recovered: data.statistics.edges[0].node.recovered
                    }
                });
                addCountryStatistics(data);
            }
        });
        geoJSON = {
            type: "FeatureCollection",
            features: featuresData
        }
        headerTotalConfirmed.innerText = totalCases.totalConfirmed.toLocaleString();
        totalConfirmed.innerText = totalCases.totalConfirmed.toLocaleString();
        totalDeaths.innerText = totalCases.totalDeaths.toLocaleString();
        totalRecovered.innerText = totalCases.totalRecovered.toLocaleString();
        if(totalCases.totalRecovered >= 1) {
            totalRecovered.innerText = totalCases.totalRecovered.toLocaleString();
        } else {
            totalRecovered.innerText = "N/A";
        }
    }
}

searchInput.addEventListener('input', function (e) {
    // clear list
    statisticsContainer.style.display = "block";
    statisticsContainer.innerHTML = ``;

    let data = e.target.value;
    if (data.length >= 1) {
        let filteredValues = filterStatistics(data);
        if(filteredValues.length === 0) {
            statisticsContainer.style.display = "none";
            nrfContainer.style.display = "flex";
        } else {
            nrfContainer.style.display = "none";
        }
        filteredValues.forEach(value => {
            if(value.statistics.edges.length >= 1) {
                addCountryStatistics(value);
            }
        });
    } else {
        renderStatistics(totalCases, statistics);
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
 * This function returns custom popup view HTML design that renders over the map.
 * @param name is country name
 * @param flag is country flag
 * @param confirmed is confirmed cases
 * @param deaths is deaths cases
 * @returns HTML popup view
 */
function renderPopupView(name, flag, confirmed, deaths) {
    return `<div class="map-popup-container">
               <div class="flag-container">
                   <img src=${flag} />
               </div>
               <div>
                  <div class="map-country-container">
                     <strong class="country">${name}</strong>
                  </div>
                  <div class="map-container-divider"></div>
                     <div class="map-statistics-container">
                        <div class="statistics">
                           <span class="cases">${confirmed.toLocaleString()}</span>
                           <strong class="label">Confirmed</strong>
                        </div>
                        <div class="statistics">
                           <span class="cases">${deaths.toLocaleString()}</span>
                            <strong class="label">Deaths</strong>
                        </div>
                     </div>
                  </div>
               </div>`
}

/**
 * This function adds list of countries with the statistics to the parent container.
 * @param data contains country list with the covid statistics
 */
function addCountryStatistics(data) {
    let countryListContainer = document.createElement("div");
    countryListContainer.setAttribute("class", "country-list-container");
    countryListContainer.setAttribute("id", "country-"+data.code);

    let country = document.createElement("div");
    country.setAttribute("class", "country");

    let flag = document.createElement("img");
    flag.setAttribute("class", "flag");
    flag.src = data.flag;

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
    if(data.statistics.edges[0].node.recovered >= 1){
        recoveredCount.innerText = data.statistics.edges[0].node.recovered.toLocaleString();
    } else {
        recoveredCount.innerText = "N/A";
    }

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

    countryListContainer.addEventListener('click', function (e) {
        let selectedValue = "country-"+data.code;
        let countryItem = document.querySelectorAll(".country-list-container");
        let DESELECTED_COLOR = '#1d1d1d';
        let SELECTED_COLOR = '#003f6d';
        let HOVER_COLOR = '#343a40';

        countryItem.forEach(item => {
            item.style.backgroundColor = DESELECTED_COLOR;
            item.addEventListener("mouseover", function() {
                item.style.backgroundColor = HOVER_COLOR;
            });
            item.addEventListener("mouseout", function() {
                item.style.backgroundColor = DESELECTED_COLOR;
            });
        });
        let selector = document.querySelector("#country-"+data.code);
        selector.style.backgroundColor = SELECTED_COLOR;
        if(selector.getAttribute('id') === selectedValue) {
            selector.addEventListener("mouseover", function() {
                selector.style.backgroundColor = SELECTED_COLOR;
            });
            selector.addEventListener("mouseout", function() {
                selector.style.backgroundColor = SELECTED_COLOR;
            });
        }

        // fly to coordinate
        flyToCoordinate(data);
    });
}
