function fSetUrlHistory(page) {
  history.pushState(null, null, page);
}

console.log('hallo Welt 3');

// carousel controlers, left + right
function fAddBtnClicked(btn) {
  console.log('fAddBtnClicked begin');

  var unit_number = iTraining_units_count == 0 ? 'begin' : iTraining_units_count;

  iTraining_units_count++;
  var sNew_id = String(Object.keys(dAll_training_unit_data).length);
  dAll_training_unit_data[sNew_id] = [String(iTraining_units_count), 0, 0, false, {}];
  fGetPageData(unit_number, iTraining_units_count, sNew_id);

  fGetNewNumberCircle(iTraining_units_count, sNew_id);


  if (unit_number == 'begin') {
    $('#schedule-form').css('display', 'block');
    $('.e-timeline-week .e-tbar-btn').trigger('click');
  }


  sCurrant_training_unit_id = sNew_id;
  fAddTrainingToSchedule(iTraining_units_count, sNew_id);
  iCurrant_step++;
}


function fNextBtnClicked(btn) {
  console.log('fNextBtnClicked begin');
  fCheckAndSetStepSuccess();
  var unit_next_number = $(btn).data('next');
  fSetCurrentStateData(unit_next_number);
  iCurrant_step++;
}
// #end carousel controlers, left + right


function fSetCurrentStateData(sNew_step) {
  console.log('fSetCurrentStateData begin ' + sNew_step)
  sCurrant_training_unit_id = $('#content-' + sNew_step + ' .training_unit').data('unit_id');
}


// #end exercise search dialog
var data_titles;
// click on add exercise button





function fAddWarmExClicked(eAdd_btn) {
  sTraining_part = 'warm';
  fBaseCreateExercisesSearchDialog();
  eLabel_btn = $("#warm_label_" + sCurrant_training_unit_id);
  fOpenOrCloseExTable(true, eLabel_btn, sCurrant_training_unit_id);
}
function fAddCoolExClicked(eAdd_btn) {
  sTraining_part = 'cool';
  fBaseCreateExercisesSearchDialog();
  eLabel_btn = $("#cool_label_" + sCurrant_training_unit_id);
  fOpenOrCloseExTable(true, eLabel_btn, sCurrant_training_unit_id);
}
function fAddTrainExClicked(eAdd_btn) {
  sTraining_part = 'train';
  fBaseCreateExercisesSearchDialog();
  eLabel_btn = $("#train_label_" + sCurrant_training_unit_id);

  fOpenOrCloseExTable(true, eLabel_btn, sCurrant_training_unit_id);
}






// request for page
function fGetPageData(unit_number, next_unit_number, sNew_id) {

  var eForm = $('#training_plan-create-' + sCurrant_training_unit_id);
  var settings = {
    url: '',
    method: 'POST',
    traditional: true,
    data: eForm.serialize() + '&unit_number=' + next_unit_number + '&unit_id=' + sNew_id
  };

  $.ajax(settings).done(function (data) {
    console.log('training plan get next page fct begin');
    console.log(unit_number);
    $('#content-' + unit_number).addClass('has-next');
    eNext_content = $('#content-next');

    $('#steps-content').append($(eNext_content.clone()));
    eNext_content.attr('id', 'content-' + next_unit_number);
    eNext_content.append(data);
    fAppendNewTableSet(sNew_id); // warm, train and cool table
    var sEnd_content_number = String(parseInt(next_unit_number) + 2);
    $('#circle-end').attr('data-slide-to', sEnd_content_number);
  });
}
// ###end### request for second page


// append new number circle
function fGetNewNumberCircle(sNumber, sNew_id) {
  var settings = {
    url: 'new_circle/',
    method: 'GET',
    traditional: true,
    data: { number: sNumber, unit_id: sNew_id }
  };

  $.ajax(settings).done(function (data) {
    var eNext_circle = $('.circle-wrapper.next')[0];
    $(eNext_circle).clone().insertBefore($('#circle-end-wrapper'));
    $(eNext_circle).append(data);
    $(eNext_circle).attr('class', 'circle-wrapper');
    console.log(sNumber);
    $('.carousel').carousel(parseInt(sNumber))
  });
}
// #end append new number circle


