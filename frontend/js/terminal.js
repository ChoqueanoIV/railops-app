const token = sessionStorage.getItem("access_token");
const sairButton = document.getElementById("sair");

if (!token) {
    window.location.replace("./index.html");
}

sairButton.addEventListener("click", function () {
    sessionStorage.removeItem("access_token");
    window.location.replace("./index.html");
});
