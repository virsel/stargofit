

// exercises kind selection
$('.image-btn').click(function () {
  console.log('image click');
  $eOverlay = $($(this).children()[2]);
  console.log($eOverlay);
  var eSelect_all_checkbox = $('#select_all_kinds');
  var lChecked_images = $('.tempting-azure-gradient');
  var iChecked_images = lChecked_images.length;
  var bIs_checked = $eOverlay.hasClass('tempting-azure-gradient');
  if (bIs_checked && iChecked_images > 1) {
    $(this).children()[0].checked = false;
    $eOverlay.removeClass('tempting-azure-gradient');
    if (eSelect_all_checkbox.is(":checked"))
      eSelect_all_checkbox.prop('checked', false);
  }
  else if (!bIs_checked) {
    // if kind is not selected...
    $(this).children()[0].checked = true;
    $eOverlay.addClass('tempting-azure-gradient');
    if (iChecked_images == 2)
      eSelect_all_checkbox.prop('checked', true);
  }
});

// fast selection buttons
$('#select_all_kinds').change(function () {
  console.log($(this));
  var lChecked_images = $('.tempting-azure-gradient');
  if (!$(this).is(":checked")) {
    // if kind is not selected...
    // reset settings

    var iChecked_images = lChecked_images.length;

    if (iChecked_images > 1) {
      lChecked_images.each(function (index) {
        if ($(this).attr('id') != 'endurance') {
          $(this).removeClass('tempting-azure-gradient');
          var sKind = $(this).attr('id');
          $('#' + sKind + '_input').prop('checked', false);
        }
      });
      var eEndurance_mask = $('#endurance_mask');
      if (!eEndurance_mask.hasClass('tempting-azure-gradient')) {
        eEndurance_mask.addClass('tempting-azure-gradient');
        var sKind = $(lChecked_images[0]).attr('id');
        $('#endurance_input').prop('checked', true);
      }
    }
  }
  else {
    console.log('select all muscle kinds');
    $('.image-btn .mask').each(function (index) {
      console.log('mask to select');

      if (!$(this).hasClass('tempting-azure-gradient')) {
        $(this).addClass('tempting-azure-gradient');
        var sKind = $(this).attr('id').split('_')[0];
        $('#' + sKind + '_input').prop('checked', true);
      }
    });
  }
});

// ###end### exercises kind selection



/* Dropdown Menu*/
$('.dropdown').click(function () {
  $(this)
    .attr('tabindex', 1)
    .focus();
  $(this).toggleClass('dropdown-fr-active');
  $(this)
    .find('.dropdown-menu')
    .slideToggle(300);
});

$('.dropdown').focusout(function () {
  $(this).removeClass('dropdown-fr-active');
  $(this)
    .find('.dropdown-menu')
    .slideUp(300);
});

$('.dropdown .dropdown-menu li').click(function () {
  if (
    $(this)
      .attr('class')
      .includes('drdwn-fr-el-active')
  ) {
  } else {
    var eOld_selected_el = $('.drdwn-fr-el-active');
    if (eOld_selected_el) eOld_selected_el.removeClass('drdwn-fr-el-active');

    $(this).toggleClass('drdwn-fr-el-active');
    document.getElementById('dropdown-fr-label').innerHTML = $(this).html();
    document.getElementById('frequenz-value').value = $(this).attr('data-id');
  }
});
/* ###end### Dropdown Menu*/

/* open/close exercise exclusion */
$('#exclude_equipment').click(function () {

  $Equ_table = $('#equ-excl-table');

  if ($Equ_table.hasClass('active')) {
    $Equ_table.removeClass('active');
    // unselect equipment
    fToggleEquKind(eAll_kind_button, false);
    fToggleAll(false);
    bAll_selected = false;
    // ###end### unselect equipment
  } else {
    $Equ_table.addClass('active');
  }
});
/* ###end### open/close exercise exclusion */

// exercise exclusion for equipment selection

// set var
var iIndoor_count = 0;
var iOutdoor_count = 0;
var iLight_count = 0;
var bIndoor_all_selected = false;
var bOutdoor_all_selected = false;
var bLight_all_selected = false;
var bAll_selected = false;

var eAll_kind_button = document.getElementById('equ-kind-all');
var eLight_button = document.getElementById('equ-kind-light');
var eIndoor_button = document.getElementById('equ-kind-ind');
var eOutdoor_button = document.getElementById('equ-kind-out');
// ###end### set var

// set Button start functions
eAll_kind_button.onclick = function () {
  var bSelect = !bAll_selected;
  fToggleEquKind(eAll_kind_button, bSelect);
  fToggleAll(bSelect);
  bAll_selected = !bAll_selected;
};
eLight_button.onclick = function () {
  var bSelect = !bLight_all_selected;
  fToggleEquKind(eLight_button, bSelect);
  fToggleKindEquElements('light', bSelect);
  if (bSelect) iLight_count = iLight;
  else iLight_count = 0;
  fSetAllBtnByClickOnElement(
    bIndoor_all_selected,
    bOutdoor_all_selected,
    bSelect
  );
  bLight_all_selected = !bLight_all_selected;
};
eIndoor_button.onclick = function () {
  var bSelect = !bIndoor_all_selected;
  fToggleEquKind(eIndoor_button, bSelect);
  fToggleKindEquElements('indoor', bSelect);
  if (bSelect) iIndoor_count = iIndoor;
  else iIndoor_count = 0;
  fSetAllBtnByClickOnElement(
    bLight_all_selected,
    bOutdoor_all_selected,
    bSelect
  );
  bIndoor_all_selected = !bIndoor_all_selected;
};
eOutdoor_button.onclick = function () {
  var bSelect = !bOutdoor_all_selected;
  fToggleEquKind(eOutdoor_button, bSelect);
  fToggleKindEquElements('outdoor', bSelect);
  if (bSelect) iOutdoor_count = iOutdoor;
  else iOutdoor_count = 0;
  fSetAllBtnByClickOnElement(
    bLight_all_selected,
    bIndoor_all_selected,
    bSelect
  );
  bOutdoor_all_selected = !bOutdoor_all_selected;
};
// ###end### set Button start functions

// select / unselect all equipments and buttons
function fToggleAll(bSelect) {
  if ((!bLight_all_selected && bSelect) || (!bSelect && bLight_all_selected)) {
    fToggleEquKind(eLight_button, bSelect);
    fToggleKindEquElements('light', bSelect);
    if (bSelect) iLight_count = iLight;
    else iLight_count = 0;
    bLight_all_selected = !bLight_all_selected;
  }
  if (
    (!bIndoor_all_selected && bSelect) ||
    (!bSelect && bIndoor_all_selected)
  ) {
    fToggleEquKind(eIndoor_button, bSelect);
    fToggleKindEquElements('indoor', bSelect);
    if (bSelect) iIndoor_count = iIndoor;
    else iIndoor_count = 0;
    bIndoor_all_selected = !bIndoor_all_selected;
  }
  if (
    (!bOutdoor_all_selected && bSelect) ||
    (!bSelect && bOutdoor_all_selected)
  ) {
    fToggleEquKind(eOutdoor_button, bSelect);
    fToggleKindEquElements('outdoor', bSelect);
    if (bSelect) iOutdoor_count = iOutdoor;
    else iOutdoor_count = 0;
    bOutdoor_all_selected = !bOutdoor_all_selected;
  }
}
// ###end### select / unselect all equipments and buttons

function fToggleEquKind(eBtn, bSelect) {
  Util.toggleClass(eBtn, 'selected', bSelect);
}

function fToggleEquEl(eEl, eInp, bSel) {
  if (bSel) {
    Util.toggleClass(eEl, 'active', true);
    eInp.checked = true;
  } else {
    Util.toggleClass(eEl, 'active', false);
    eInp.checked = false;
  }
}

function fToggleKindEquElements(kind, bSelect) {
  if (bSelect) {
    document
      .querySelectorAll('.equ-table.' + kind + ' .btn')
      .forEach(function (eEl) {
        fToggleEquEl(eEl, eEl.children[0], bSelect);
      });
  } else {
    document
      .querySelectorAll('.equ-table.' + kind + ' .btn.active')
      .forEach(function (eEl) {
        fToggleEquEl(eEl, eEl.children[0], bSelect);
      });
  }
}

// set All btn by click on elements
function fSetAllBtnByClickOnElement(bFst_other_btn, bScnd_other_btn, bSelect) {
  if (bSelect && (bFst_other_btn && bScnd_other_btn)) {
    fToggleEquKind(eAll_kind_button, bSelect);
    bAll_selected = true;
  } else if (!bSelect && (bFst_other_btn && bScnd_other_btn)) {
    fToggleEquKind(eAll_kind_button, bSelect);
    bAll_selected = false;
  }
}
// ###end### set All btn by click on one element

$('.indoor .equ-exl-btn').click(function (e) {
  e.preventDefault();
  var eInput = $(this).children()[0];
  var bSelect = !eInput.checked;

  fToggleEquEl(this, eInput, bSelect);
  if (bSelect) {
    ++iIndoor_count;
    if (iIndoor_count == iIndoor) {
      fToggleEquKind(eIndoor_button, bSelect);
      bIndoor_all_selected = true;
      fSetAllBtnByClickOnElement(
        bOutdoor_all_selected,
        bLight_all_selected,
        bSelect
      );
    }
  } else {
    --iIndoor_count;
    if (bIndoor_all_selected) {
      fToggleEquKind(eIndoor_button, bSelect);
      bIndoor_all_selected = false;
      fSetAllBtnByClickOnElement(
        bOutdoor_all_selected,
        bLight_all_selected,
        bSelect
      );
    }
  }
});

$('.outdoor .equ-exl-btn').click(function (e) {
  e.preventDefault();
  var eInput = this.children[0];
  var bSelect = !eInput.checked;

  fToggleEquEl(this, eInput, bSelect);
  if (bSelect) {
    ++iOutdoor_count;
    if (iOutdoor_count == iOutdoor) {
      fToggleEquKind(eOutdoor_button, bSelect);
      bOutdoor_all_selected = true;
      fSetAllBtnByClickOnElement(
        bLight_all_selected,
        bIndoor_all_selected,
        bSelect
      );
    }
  } else {
    --iOutdoor_count;
    if (bOutdoor_all_selected) {
      fToggleEquKind(eOutdoor_button, bSelect);
      bOutdoor_all_selected = false;
      fSetAllBtnByClickOnElement(
        bLight_all_selected,
        bIndoor_all_selected,
        bSelect
      );
    }
  }
});

$('.light .equ-exl-btn').click(function (e) {
  e.preventDefault();
  var eInput = this.children[0];
  var bSelect = !eInput.checked;
  fToggleEquEl(this, eInput, bSelect);
  if (bSelect) {
    ++iLight_count;
    if (iLight_count == iLight) {
      fToggleEquKind(eLight_button, bSelect);
      bLight_all_selected = true;
      fSetAllBtnByClickOnElement(
        bOutdoor_all_selected,
        bIndoor_all_selected,
        bSelect
      );
    }
  } else {
    --iLight_count;
    if (bLight_all_selected) {
      fToggleEquKind(eLight_button, bSelect);
      bLight_all_selected = false;
      fSetAllBtnByClickOnElement(
        bOutdoor_all_selected,
        bIndoor_all_selected,
        bSelect
      );
    }
  }
});
// ###end### exercise exclusion for equipment selection



