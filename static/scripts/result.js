// This file handles the user changing the variety on the result screen.

const varietySelect = document.getElementById("varietySelect");
const pokemonImage = document.getElementById("pokemonImage");
const pokemonType = document.getElementById("pokemonType");

varietySelect.addEventListener("change", async function () {
  const index = varietySelect.value;
  const variety = varietyList[index];
  pokemonImage.src = variety.image;
  pokemonImage.alt = variety.name;
  pokemonType.innerHTML = "";
  const types = variety.type;
  types.forEach((type) => {
    let nextType = document.createElement("img");
    nextType.src = "/static/typeIcons/" + type + ".png";
    nextType.alt = type;
    nextType.className = "typeIconMain";
    pokemonType.appendChild(nextType);
  });
  const weaknesses = variety.weaknesses;
  Object.keys(weaknesses).forEach((category) => {
    updateVariety(category, weaknesses[category]);
  });
});

const updateVariety = (category, types) => {
  category.className = "typeContainer";
  const div = document.getElementById(category);
  div.innerHTML = "";
  div.className = "typeContainer";
  types.forEach((type) => {
    let nextType = document.createElement("img");
    nextType.src = "/static/typeIcons/" + type + ".png";
    nextType.alt = type;
    nextType.className = "typeIcon";
    div.appendChild(nextType);
  });
  if (types.length === 0) {
    let na = document.createElement("div");
    na.id = "NA";
    na.innerHTML = "N/A";
    div.appendChild(na);
  }
};
