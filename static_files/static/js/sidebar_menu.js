
function SetSidebarLinkActive(sId) {
  console.log('switch active class from sidebar with id: ' + sId);
  $('#sidebar-treeview .active').removeClass('active');
  $('#sidebar-treeview #' + sId).parent().addClass('active');
}