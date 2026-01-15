function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');
    const pageTitle = document.querySelector('.page-title');

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const viewName = this.dataset.view;

            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');

            views.forEach(view => view.classList.remove('active'));
            const targetView = document.getElementById(`view-${viewName}`);
            if (targetView) {
                targetView.classList.add('active');
            }

            if (pageTitle) {
                const label = this.querySelector('.label');
                if (label) {
                    pageTitle.textContent = label.textContent;
                }
            }
        });
    });
}

export { initNavigation };
