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

    let activeItem = null;

    function setActiveMenuItem() {
        const currentPath = window.location.pathname;

        sidebarItems.forEach(element => {
            const link = element.querySelector('a');
            if (link && link.getAttribute('href') === currentPath) {
                element.setAttribute('id', 'active');
                activeItem = element;
            } else {
                element.removeAttribute('id');
            }
        });
    }

    setActiveMenuItem(); // 페이지 로드 시 실행

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

function applyCalendarView() {
    const path = window.location.pathname;
    if (path === '/calendar') {
        document.querySelector('.container').classList.add('calendar-view');
    }
}
document.addEventListener('DOMContentLoaded', applyCalendarView);
