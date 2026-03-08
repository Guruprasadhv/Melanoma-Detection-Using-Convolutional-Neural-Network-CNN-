addEventListener("load", function () {
    setTimeout(hideURLbar, 0);
}, false);

function hideURLbar() {
    window.scrollTo(0, 1);
}

function login() {
    var uname = document.getElementById("uname").value;
    var pwd = document.getElementById("pwd").value;

    if (uname == "admin" && pwd == "admin") {
        alert("Login Success!");

        // Retrieve the index URL from the data attribute on the body or a specific element
        var indexUrl = document.body.getAttribute('data-index-url');
        if (indexUrl) {
            window.location = indexUrl;
        } else {
            // Fallback if attribute is missing
            console.error("Index URL not found in data attribute");
        }
        return false;
    } else {
        alert("Invalid Credentials!")
    }
}
