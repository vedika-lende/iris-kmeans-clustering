
document.addEventListener("DOMContentLoaded", () => {
    const themeButton = document.getElementById("theme-toggle");
    const sidebar = document.getElementById("sidebar");
    const menuButton = document.getElementById("menu-toggle");
    const predictionForm = document.querySelector(".prediction-form");
    const predictButton = document.getElementById("predict-btn");

    // Theme toggle
    const savedTheme = localStorage.getItem("iris-theme");

    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
    }

    function updateThemeButton() {
        if (themeButton) {
            themeButton.textContent =
                document.body.classList.contains("light-theme") ? "☾" : "☼";
        }
    }

    updateThemeButton();

    themeButton?.addEventListener("click", () => {
        document.body.classList.toggle("light-theme");

        const theme = document.body.classList.contains("light-theme")
            ? "light"
            : "dark";

        localStorage.setItem("iris-theme", theme);
        updateThemeButton();
    });

    // Mobile navigation
    menuButton?.addEventListener("click", () => {
        sidebar?.classList.toggle("open");
    });

    document.addEventListener("click", (event) => {
        if (
            sidebar &&
            menuButton &&
            !sidebar.contains(event.target) &&
            !menuButton.contains(event.target)
        ) {
            sidebar.classList.remove("open");
        }
    });

    // Prevent duplicate submissions and show loading feedback
    predictionForm?.addEventListener("submit", (event) => {
        if (!predictionForm.checkValidity()) {
            return;
        }

        if (predictButton?.disabled) {
            event.preventDefault();
            return;
        }

        if (predictButton) {
            predictButton.disabled = true;
            predictButton.textContent = "Analyzing measurements...";
        }
    });
});
