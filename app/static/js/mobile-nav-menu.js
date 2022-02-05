let menu = [
    {
        "label": "Home",
        "icon": "home"
    },
    {
        "label": "Map",
        "icon": "map"
    },
    {
        "label": "About",
        "icon": "info"
    }
]

let countryContainer = document.querySelector('.country-container');
let mapContainer = document.querySelector("#map");
let mobileNavContainer = document.querySelector('.mobile-nav-container');

function resetMenuSelection() {
    // reset the selection
    document.querySelectorAll(".menu-label").forEach(item => item.style.color = "#5f6673");
    document.querySelectorAll(".menu-label").forEach(item => item.style.fontWeight = "normal");
    document.querySelectorAll(".material-icons").forEach(item => item.style.color = "#5f6673");
}

for(let i=0; i<menu.length; i++) {
    let menuContainer = document.createElement("div");
    menuContainer.setAttribute("class", "menu");
    menuContainer.setAttribute("id", "menu-"+menu[i].label);

    let menuIcon = document.createElement("span");
    menuIcon.setAttribute("class", "material-icons");
    menuIcon.setAttribute("id", "menu-icon-"+menu[i].label);
    menuIcon.innerHTML = menu[i].icon;

    let menuLabel = document.createElement("span");
    menuLabel.setAttribute("class", "menu-label");
    menuLabel.setAttribute("id", "menu-label-"+menu[i].label);
    menuLabel.innerHTML = menu[i].label;

    menuContainer.append(menuIcon);
    menuContainer.append(menuLabel);
    mobileNavContainer.append(menuContainer);

    document.querySelector("#menu-label-"+menu[0].label).style.color = "#407ba7";
    document.querySelector("#menu-label-"+menu[0].label).style.fontWeight = "bold";
    document.querySelector("#menu-icon-"+menu[0].label).style.color = "#FFF";

    menuContainer.addEventListener("click", function () {
        // reset the selection
        resetMenuSelection();

        // changing style selection
        document.querySelector("#menu-label-"+menu[i].label).style.color = "#407ba7";
        document.querySelector("#menu-label-"+menu[i].label).style.fontWeight = "bold";
        document.querySelector("#menu-icon-"+menu[i].label).style.color = "#FFF";

        if(menu[i].label === "Home") {
            countryContainer.style.display = "flex";
            mapContainer.style.display = "none";
        }
        if(menu[i].label === "Map") {
            countryContainer.style.display = "none";
            mapContainer.style.display = "block";
        }
        if(menu[i].label === "About") {
            alert("About");
            // countryContainer.style.display = "none";
            // map.style.display = "none";
        }
    });
}