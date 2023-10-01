    document.addEventListener("DOMContentLoaded", function() {
    const searchIcon = document.getElementById("search-icon");
    const searchForm = document.getElementById("search-form");

    if (searchIcon && searchForm) {
        searchIcon.addEventListener("click", function() {
            searchForm.submit();
        });
    }
});