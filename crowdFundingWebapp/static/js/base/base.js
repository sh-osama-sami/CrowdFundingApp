document.addEventListener('DOMContentLoaded', function() {
    fetch("/Projects/all_categories").then((response) => response.json()).then((data) => {

        const dropdownMenu = document.querySelector(".dropdown-menu");
        data.forEach((category) => {
            dropdownMenu.innerHTML += `<a class="dropdown-item" href="/Projects/category/${category.id}">${category.name}</a>`;
        });
    }).catch((error) => {
        console.log('Error fetching categories:', error);
    });
});