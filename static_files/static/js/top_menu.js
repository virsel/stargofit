// add event listeners to top menu
(function() {
  // set varibles
  var threeDNav = document.getElementsByClassName('js-cd-3d-nav');
  if (threeDNav.length > 0) {
    var header = document.getElementsByClassName('cd-header')[0],
      main = document.getElementsByClassName('sub_content')[0],
      navTrigger = document.getElementsByClassName('cd-header__nav-trigger')[0],
      ToggleElement = document.getElementsByClassName('toggle-element')[0];
    var marker = document.getElementsByClassName('cd-3d-nav__marker')[0];
    var threeDNav = document.getElementsByClassName('js-cd-3d-nav');
    var navItems = threeDNav[0].getElementsByTagName('li');
    var selectedItem = threeDNav[0].getElementsByClassName(
      'cd-3d-nav__item--selected'
    )[0];
    var training_kind_name = String(
      selectedItem.firstElementChild.className
    ).replace('_selector', '');
    marker.style.width = window
      .getComputedStyle(navItems[2])
      .getPropertyValue('width');
    // ###end### set varibles

    // update top menu position onload
    function updateSelectedNav(type) {
      // update the marker position
      var iItemIndex = Array.prototype.indexOf.call(navItems, selectedItem);
      updateMarkerWidth();
      var leftPosition;
      if (iItemIndex == 1) {
        leftPosition = 70;
      } else {
        leftPosition = (iItemIndex - 1) * parseInt(marker.style.width) + 70;
      }
      removeClassPrefix(marker);
      Util.addClass(marker, 'cd-3d-nav__marker--col-' + training_kind_name);
      marker.style.left = leftPosition + 'px';

      if (type == 'close') {
        marker.addEventListener('transitionend', function cb() {
          marker.removeEventListener('transitionend', cb);
        });
      }
    }

    function updateMarkerWidth() {
      // update the marker width
      marker.style.width = window
        .getComputedStyle(navItems[2])
        .getPropertyValue('width');
    }

    function removeClassPrefix(el) {
      el.className = el.className.split(' ')[0].trim();
    }
    // ###end### update top menu position

    // open/close top menu
    function toggle3dBlock(
      addOrRemove,
      header,
      ToggleElement,
      threeDNav,
      main
    ) {
      if (typeof addOrRemove === 'undefined') addOrRemove = true;

      Util.toggleClass(header, 'cd-header--is-translated', addOrRemove);
      Util.toggleClass(
        ToggleElement,
        'toggle-element--is-translated',
        addOrRemove
      );
      Util.toggleClass(threeDNav[0], 'cd-3d-nav--is-visible', addOrRemove);
      Util.toggleClass(main, 'sub_content--is-translated', addOrRemove);
      main.addEventListener('transitionend', function cb() {
        //fix marker position when opening the menu (after a window resize)
        addOrRemove && updateSelectedNav();
        main.removeEventListener('transitionend', cb);
      });
      $('#sub_top_menu_toggle').toggleClass('open');
    }
    // ###end### open/close top menu

    // click event listener for toggle menu
    navTrigger.addEventListener('click', function(event) {
      console.log('nav trigge#r');
      // open/close navigation
      event.preventDefault();
      toggle3dBlock(
        !Util.hasClass(header, 'cd-header--is-translated'),
        header,
        ToggleElement,
        threeDNav,
        main
      );
    });
    // ###end### click event listener for toggle menu

    // click event listener for menu section
    threeDNav[0].addEventListener('click', function(event) {
      console.log('top menu click');
      event.preventDefault();
      selectedItem = event.target.closest('.cd-3d-nav__item');
      if (
        Util.hasClass(selectedItem, 'cd-3d-nav__item--selected') ||
        selectedItem.className == 'cd-3d-nav__placeholder'
      )
        return;
      training_kind_name = String(
        selectedItem.firstElementChild.className
      ).replace('_selector', '');
      history.pushState(null, null, training_kind_name);
      fChangeContent();
    });
    // ###end### click event listener for menu section

    // change Website Content
    function fChangeContent() {
      Util.removeClass(
        threeDNav[0].getElementsByClassName('cd-3d-nav__item--selected')[0],
        'cd-3d-nav__item--selected'
      );
      Util.addClass(selectedItem, 'cd-3d-nav__item--selected');
      updateSelectedNav(); // set section position

      fSendAndGetData(training_kind_name); // ajax request
    }
    // ###end### change Website Content

    // back/forward click event
    $(window).on('popstate', function() {
      training_kind_name = location.pathname.split('/').pop();
      console.log(training_kind_name);
      if (training_kind_name != '') {
        sButtonClassName = training_kind_name + '_selector';
        eButton = document.getElementsByClassName(sButtonClassName)[0];
        selectedItem = eButton.parentElement;
      } else {
        training_kind_name = 'endurance';
        sButtonClassName = training_kind_name + '_selector';
        eButton = document.getElementsByClassName(sButtonClassName)[0];
        selectedItem = eButton.parentElement;
      }
      updateSelectedNav(); // set section position
      fChangeContent();
    });
    // ###end### back/forward click event

    // resize event listener for window
    window.addEventListener('resize', function() {
      // reset marker position on resize
      window.requestAnimationFrame(updateSelectedNav);
    });
    // ###end### resize event listener for window
  }
})();
// ###end### add event listeners to top menu
