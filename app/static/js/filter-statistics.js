/**
 * The below listener handles timeline event to load covid statistics for different time-periods.
 */
let dateSelector = document.getElementById("date-selector");
dateSelector.addEventListener("change", function() {
    let query = JSON.stringify(graphqlQuery);
    let date = query.match(/\d{2}([\/.-])\d{2}\1\d{4}/g);
    query = query.replaceAll(date[0], dateSelector.value);
    fetch('/graphql', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: query
    }).then(res => res.json())
        .then(res => {
            renderStatistics(res.data.totalCases.edges[0].node, res.data.countryStatistics);
            loadMap();
        }).catch(err => {
            console.log(err)
        })
});