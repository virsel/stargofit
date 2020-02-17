
eMobileNavTrigger = $('#nav-trigger');
eSidebarNav = $('#sidebar-left');

//on mobile, open sidebar when clicking on menu icon
eMobileNavTrigger.on('click', function (event) {
    event.preventDefault();
    console.log('navbar clicked');
    $(this).toggleClass('visible');
    eSidebarNav.toggleClass('visible');
});

// close custom menu on click on close icon
function ClickOnCloseIcon(eBtn) {
    $(eBtn).parent().parent().removeClass('visible');
}