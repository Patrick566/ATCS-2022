// Line Animation (written by me)
function line() {
    var navbar = document.getElementsByClassName("navbar")[0];
    navbar.style.visibility = "hidden";
    var carousel = document.getElementsByClassName("carousel")[0];
    carousel.style.visibility = "hidden";
    var aboutMe = document.getElementById("about-me");
    aboutMe.style.visibility = "hidden";
    var title = document.getElementById("title");
    title.style.visibility = "hidden";
    var line = document.getElementById("line");
    line.style.height = "0vh"
    makeLine(0);
}
function makeLine(length) {
    var line = document.getElementById("line");
    if (length != 50) {
        line.style.height = length.toString() + "vh";
        length++;
        setTimeout(makeLine, 10, length);
    }
    else {
        line.style.visibility = "hidden";
        var navbar = document.getElementsByClassName("navbar")[0];
        navbar.style.visibility = "visible";
        var carousel = document.getElementsByClassName("carousel")[0];
        carousel.style.visibility = "visible";
        var aboutMe = document.getElementById("about-me");
        aboutMe.style.visibility = "visible";
        var title = document.getElementById("title");
        title.style.visibility = "visible";
        return;
    }
}