// set variables
var eEff_output = document.getElementById('eff_output');
var eEff_slider = document.getElementById('range_eff');
var eDiff_output = document.getElementById('diff_output');
var eDiff_slider = document.getElementById('range_diff');
var liDiff_values = [1, 5];
var liEff_values = [1, 5];
var bWith_equ = true;
var bWithout_equ = true;
var iEquipment = 3;
// #end set variables

// create sliders
noUiSlider.create(eEff_slider, {
  start: [1, 5], // Handle start position
  step: 1,
  connect: [false, true, false],
  range: {
    // Slider can select '0' to '100'
    min: 1,
    max: 5
  }
});
noUiSlider.create(eDiff_slider, {
  start: [1, 5], // Handle start position
  step: 1,
  connect: [false, true, false],
  range: {
    // Slider can select '0' to '100'
    min: 1,
    max: 5
  }
});

// append event listeners to sliders
eEff_slider.noUiSlider.on('update', function (values) {
  if (values[0] == values[1]) eEff_output.innerText = values[0];
  else eEff_output.innerText = values[0] + ' - ' + values[1];
});
eEff_slider.noUiSlider.on('end', function (values) {
  liEff_values = [parseInt(values[0]), parseInt(values[1])];
  var iNew_diff = values[1] - values[0];
  if (iNew_diff > 3) liEff_values = [];

  fGetExercisesPerConditions();
});

eDiff_slider.noUiSlider.on('update', function (values) {
  if (values[0] == values[1]) eDiff_output.innerText = values[0];
  else eDiff_output.innerText = values[0] + ' - ' + values[1];
});
eDiff_slider.noUiSlider.on('end', function (values) {
  liDiff_values = [parseInt(values[0]), parseInt(values[1])];
  console.log(liDiff_values);
  var iNew_diff = values[1] - values[0];
  if (iNew_diff > 3) liDiff_values = [];

  fGetExercisesPerConditions();
});
// #end append event listeners to sliders
// #end create sliders
var bEqu_filter_is_enabled = false;
document
  .getElementById('equipment-switcher')
  .addEventListener('change', function (eSwitcher) {
    if (!bEqu_filter_is_enabled) {
      document.querySelectorAll('.equ-radio').forEach(function (eRadio) {
        eRadio.checked = false;
        eRadio.disabled = false;
      });
      bEqu_filter_is_enabled = !bEqu_filter_is_enabled;
    } else {
      document.querySelectorAll('.equ-radio').forEach(function (eRadio) {
        eRadio.checked = false;
        eRadio.disabled = true;
      });
      bEqu_filter_is_enabled = !bEqu_filter_is_enabled;
    }
  });

// set equipment checkboxes
// 3: all
// 2: without equ
// 1: with equ
$('#with_equ').on('click', function (e) {
  if ($(this).attr('checked', 'false')) {
    console.log('equipment');
    iEquipment = 1;
    fGetExercisesPerConditions();
  }
  else {
    console.log('no equipment');
    iEquipment = 3;
    fGetExercisesPerConditions();
  }
});

$('#equipment-switcher').on('click', function (e) {
  console.log('equipment switcher');
  console.log($(this).is(':checked'));
  if (!$(this).is(':checked')) {
    console.log('no equipment');
    iEquipment = 3;
    fGetExercisesPerConditions();
  }
});


$('#without_equ').on('click', function (e) {
  if ($(this).attr('checked', 'false')) {
    iEquipment = 2;
    fGetExercisesPerConditions();
  }
});
// #end set equipment checkboxes
