const homeSearch = document.getElementById("homeSearch");
const suggestionsDiv = document.getElementById("suggestions");
const submitButton = document.getElementById("submitButton");

homeSearch.addEventListener("input", async function () {
  const query = this.value;
  if (query.length > 0) {
    const response = await fetch(`/autocomplete?query=${query}`);
    const suggestions = await response.json();
    displaySuggestions(suggestions);
  } else {
    document.getElementById("suggestions").innerHTML = "";
  }
});

function displaySuggestions(suggestions) {
  suggestionsDiv.innerHTML = "";
  suggestions.forEach((pair) => {
    let name = pair[0];
    let image = pair[1];
    const div = document.createElement("div");
    div.innerText = name + " ";
    div.classList.add("suggestion");
    suggestionsDiv.appendChild(div);
    const img = document.createElement("img");
    img.src = image;
    img.alt = name;
    img.width = 100;
    img.length = 100;
    div.appendChild(img);
    div.addEventListener("click", () => {
      homeSearch.value = name;
      suggestionsDiv.innerHTML = "";
      submitButton.click();
    });
  });
}
