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
    pokemonType.appendChild(nextType);
  });
  const weaknesses = variety.weaknesses;
  Object.keys(weaknesses).forEach((category) => {
    updateVariety(category, weaknesses[category]);
  });
});

const updateVariety = (category, types) => {
  category.className = "typeContainer"
  const div = document.getElementById(category);
  div.innerHTML = "";
  types.forEach((type) => {
    let nextType = document.createElement("img");
    nextType.src = "/static/typeIcons/" + type + ".png";
    nextType.alt = type;
    nextType.className = "typeContainer";
    div.appendChild(nextType);
  });
};
