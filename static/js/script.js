document.addEventListener('DOMContentLoaded', function() {
    const menuOpen = document.getElementById('menu-open');
    const menuClose = document.getElementById('menu-close');
    const sideBar = document.querySelector('.container .left-section');
    const sidebarItems = document.querySelectorAll('.container .left-section .sidebar .item');

    if (menuOpen) {
        menuOpen.addEventListener('click', () => {
            sideBar.style.top = '0';
        });
    }

    if (menuClose) {
        menuClose.addEventListener('click', () => {
            sideBar.style.top = '-60vh';
        });
    }

    let activeItem = sidebarItems[0];

    sidebarItems.forEach(element => {
        element.addEventListener('click', () => {
            if (activeItem) {
                activeItem.removeAttribute('id');
            }

            element.setAttribute('id', 'active');
            activeItem = element;
        });
    });
});
