
// exercises search dialog scripts
var leExerciseBoxes;
function fSetExercisesSearchDialog() {
    console.log('hallo start of exercise search dialog');
    eEff_output = document.getElementById('exercises_dlg_eff_output');
    eEff_slider = document.getElementById('exercises_dlg_range_eff');
    liEff_values = [1, 5];
    eDiff_output = document.getElementById('exercises_dlg_diff_output');
    eDiff_slider = document.getElementById('exercises_dlg_range_diff');
    liDiff_values = [1, 5];
    leExerciseBoxes = $('#exercise_search_el .exercise');
    iExerciseBoxes_count = leExerciseBoxes.length;
    bFilter_is_more = false;
    iEff_diff = 4;
    iDiff_diff = 4;
    bIsFirstAreaSelection = true;
    bIsFirstKindSelection = true;
    iSearch_index = -1;
    iExercise_id = -1;
    eExercise_list = $('#exercise_search_el');





    // area selection
    checkList = new ej.dropdowns.MultiSelect({
        placeholder: "{% trans 'Körperbereich' %}",
        mode: 'CheckBox',
        showDropDownIcon: true,
        allowFiltering: false,
        popupHeight: '350px',
        popupWidth: '200px',
    });
    checkList.appendTo('#area-selection');
    fSetAreaSelectionEvents();
    // #end area selection


    // kind selection
    kind_selection = new ej.dropdowns.MultiSelect({
        placeholder: "{% trans 'Übungsart' %}",
        mode: 'CheckBox',
        showDropDownIcon: true,
        allowFiltering: false,
        popupHeight: '350px',
        popupWidth: '250px',
    });
    kind_selection.appendTo('#kind-selection');
    fSetKindSelectionEvents();
    // #end area selection


    fSetRangeSliders(); // set range sliders
    console.log('set exercise search dialog function end');
    fSetExerciseSearchAutoComplete();
}



function fSetExerciseSearchAutoComplete() {
    console.log('autocomplete function start');
    var sSearch_string = ''
    var eExercise_search_input = $('#exercise_dlg_search_input');

    eExercise_search_input.mdbAutocomplete({
        data: lsExercises_titles
    });
    var eExercise_search_btn = document.getElementById('exercises_dlg_search_btn')

    // set search selection event
    eExercise_search_btn.addEventListener('click', function (e) {
        e.preventDefault();
        console.log('start search input change event function');
        console.log(eExercise_search_input);


        console.log(sSearch_string);

        iSearch_index = lsExercises_titles.indexOf(sSearch_string);

        if (iSearch_index >= 0) { // one specific   
            fSetFoundedExerciseBox(iSearch_index);
            console.log(iSearch_index);
        }
        else {
            var counter = 0;
            lsExercises_titles.forEach(function (title) {
                console.log(title);
                var iTitle_list_index = title.toLowerCase().indexOf(sSearch_string.toLowerCase());
                if (iTitle_list_index >= 0)
                    fSetFoundedExerciseBox(counter);
                counter++;
            });
        }
        ClearSearchInput();
    });


    eExercise_search_input.keyup(function (event) {

        console.log('key pressed');
        if (event.keyCode === 13) {
            event.preventDefault();
            eExercise_search_btn.click();
        }
        else {
            sSearch_string = eExercise_search_input.val();
        }
    });

}
// #end set Search input field


function ClearSearchInput() {
    $('#autocomplete-clear').click();
}


function fSetFoundedExerciseBox(iIndex) {
    console.log('set founded exercise id...');

    iExercise_id = lsExercises_ids[iIndex];
    console.log(iExercise_id);
    var eExercise_box = $('#search-exercise-id_' + String(iExercise_id));
    if (eExercise_box.css('display') == 'none')
        eExercise_box.css('display', 'block');
    eExercise_box.addClass("searched-exercise");
    setTimeout(function () { eExercise_box.removeClass("searched-exercise"); }, 4000);
    $('#exercise_search_el').prepend(eExercise_box);
}
// #end set search selection event





function fSetAreaSelectionEvents() {
    console.log('exercises search area selection set events start');
    checkList.addEventListener('select', function (i) {
        console.log('exercises search area selection select event start');
        sArea = i.itemData.value;
        if (bIsFirstFiltering) {
            bIsFirstFiltering = false;
            bIsFirstAreaSelection = false;
            lsSelected_areas.push(sArea);
            fFilterCorrespondingToUserAction(7, sArea);
        }
        else if (bIsFirstAreaSelection) {
            lsSelected_areas.push(sArea);
            fFilterCorrespondingToUserAction(8, sArea);
            bIsFirstAreaSelection = false;
        }
        else {
            lsSelected_areas.push(sArea);
            fFilterCorrespondingToUserAction(9, sArea);
        }
    });


    checkList.addEventListener('removed', function (i) {
        sArea = i.itemData.value;

        if (lsSelected_areas.length > 1) {
            var index = lsSelected_areas.indexOf(sArea);
            if (index > -1) {
                lsSelected_areas.splice(index, 1);
            }
            fFilterCorrespondingToUserAction(10, sArea);
        }
        else {
            lsSelected_areas = []
            fFilterCorrespondingToUserAction(11);
            bIsFirstAreaSelection = true;
        }
    });
    // #end Set Area Filter functions
}


// set training kind selection events
function fSetKindSelectionEvents() {
    console.log('exercises search kind selection set events start');
    kind_selection.addEventListener('select', function (i) {
        console.log('exercises search kind selection select event start');
        sKind = i.itemData.value;
        if (bIsFirstFiltering) {
            bIsFirstFiltering = false;
            bIsFirstKindSelection = false;
            lsSelected_kinds.push(sKind);
            fFilterCorrespondingToUserAction(2, sKind);
        }
        else if (bIsFirstKindSelection) {
            lsSelected_kinds.push(sKind);
            fFilterCorrespondingToUserAction(12, sKind);
            bIsFirstKindSelection = false;
        }
        else {
            lsSelected_kinds.push(sKind);
            fFilterCorrespondingToUserAction(5, sKind);
        }
    });


    kind_selection.addEventListener('removed', function (i) {
        sKind = i.itemData.value;

        if (lsSelected_kinds.length > 1) {
            var index = lsSelected_kinds.indexOf(sKind);
            if (index > -1) {
                lsSelected_kinds.splice(index, 1);
            }
            fFilterCorrespondingToUserAction(6, sKind);
        }
        else {
            lsSelected_kinds = []
            fFilterCorrespondingToUserAction(13);
            bIsFirstKindSelection = true;
        }
    });
}
// #end set training kind selection events



// create sliders
function fSetRangeSliders() {
    console.log('start slider set event function');
    noUiSlider.create(eEff_slider, {
        start: [1, 5], // Handle start position
        step: 1,
        connect: [false, true, false],
        range: { // Slider can select '0' to '100'
            'min': 1,
            'max': 5
        },
    });
    console.log('start slider set event function before setting second slider');
    noUiSlider.create(eDiff_slider, {
        start: [1, 5], // Handle start position
        step: 1,
        connect: [false, true, false],
        range: { // Slider can select '0' to '100'
            'min': 1,
            'max': 5
        },
    });
    console.log('start slider set event function after setting second slider');


    // append event listeners to sliders
    eEff_slider.noUiSlider.on('update', function (values) {
        console.log('eff slider update event start');
        if (values[0] == values[1])
            eEff_output.innerText = values[0];
        else
            eEff_output.innerText = values[0] + ' - ' + values[1];
    });
    eEff_slider.noUiSlider.on('end', function (values) {
        liEff_values = values;
        var iNew_diff = values[1] - values[0];
        bFilter_is_more = iEff_diff < iNew_diff;
        iEff_diff = iNew_diff;
        console.log('hallo end 1');
        fFiltering('eff', liEff_values);
    });


    eDiff_slider.noUiSlider.on('update', function (values) {
        if (values[0] == values[1])
            eDiff_output.innerText = values[0];
        else
            eDiff_output.innerText = values[0] + ' - ' + values[1];
    });
    eDiff_slider.noUiSlider.on('end', function (values) {
        liDiff_values = values;
        console.log(liDiff_values);
        var iNew_diff = values[1] - values[0];
        bFilter_is_more = iDiff_diff < iNew_diff;
        iDiff_diff = iNew_diff;
        console.log('hallo end 2');
        fFiltering('diff', values);
    });
    // #end append event listeners to sliders
}
// #end create sliders


// filtering
function fFiltering(sOption, liValues = []) {
    if (bIsFirstFiltering) {
        if (sOption == 'eff' || sOption == 'diff')
            fFilterCorrespondingToUserAction(1, sOption, liValues)
        else
            fFilterCorrespondingToUserAction(2)
        bIsFirstFiltering = false;
    }
    else if (sOption == 'eff' || sOption == 'diff') {
        if (bFilter_is_more)
            fFilterCorrespondingToUserAction(3, sOption, liValues)
        else
            fFilterCorrespondingToUserAction(4, sOption, liValues)
    }
}


// 1: first filtering diff or eff
// 2: first filtering kind
// 3: more diff or eff
// 4: less diff or eff
// 5: more kind
// 6: less kind
// 7: first filtering area
// 8: first area selection
// 9: more area
// 10: less area
// 11: no area selection
// 12: first kind selection
// 13: no kind selection
function fFilterCorrespondingToUserAction(iNumber, sOption = '', liValues = []) {
    switch (iNumber) {
        case 1:
            console.log('1');
            leExerciseBoxes.filter(function (index) {
                var bShow = $(this).data(sOption) >= liValues[0] && $(this).data(sOption) <= liValues[1];
                return !bShow;
            }).css('display', 'none');
            break;
        case 2:
            console.log('2 xc' + sOption);
            leExerciseBoxes.filter(function (index) {
                var bHide = $(this).data('kind') != sOption;
                return bHide;
            }).css('display', 'none');
            break;

        case 3:
            console.log('3');
            var leHiddenExercises = leExerciseBoxes.filter(':hidden');
            var iHiddenExercises = leHiddenExercises.length;
            var iCounter = 0;
            leHiddenExercises.filter(function (index) {
                var bShow = $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_areas.length > 0)
                    bShow = bShow && lsSelected_areas.includes($(this).data('area'));
                if (lsSelected_kinds.length > 0)
                    bShow = bShow && lsSelected_kinds.includes($(this).data('kind'));
                if (bShow)
                    iCounter++;
                return bShow;
            }).css('display', 'block');
            if (iCounter == iHiddenExercises)
                bIsFirstFiltering = true;
            break;
        case 4:
            console.log('4');
            leExerciseBoxes.filter(':visible').filter(function (index) {
                var bShow = $(this).data(sOption) >= liValues[0] && $(this).data(sOption) <= liValues[1];
                return !bShow;
            }).css('display', 'none');
            break;
        case 5:
            console.log('5' + sOption);
            var leHiddenExercises = leExerciseBoxes.filter(':hidden');
            var iHiddenExercises = leHiddenExercises.length;
            var iCounter = 0;
            leHiddenExercises.filter(function (index) {
                var bShow = $(this).data('kind') == sOption;
                bShow = bShow && $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_areas.length > 0)
                    bShow = bShow && lsSelected_areas.includes($(this).data('area'));
                if (bShow)
                    iCounter++;
                return bShow;
            }).css('display', 'block');
            if (iCounter == iHiddenExercises)
                bIsFirstFiltering = true;
            break;
        case 6:
            console.log('6' + sOption);
            leExerciseBoxes.filter(':visible').filter(function (index) {

                var bHide = $(this).data('kind') == sOption;
                return bHide;
            }).css('display', 'none');
            break;
        case 7:
            console.log('7' + sOption);
            leExerciseBoxes.filter(function (index) {
                var bHide = $(this).data('area') != sOption;
                return bHide;
            }).css('display', 'none');
            break;
        case 8:
            console.log('8' + sOption);
            var leVisisbleExercises = leExerciseBoxes.filter(':visible');
            leVisisbleExercises.filter(function (index) {
                var bShow = $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && ($(this).data('area') == sOption);
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_kinds.length > 0)
                    bShow = bShow && lsSelected_kinds.includes($(this).data('kind'));
                console.log($(this).data('area') + '  ' + bShow);
                return !bShow;
            }).css('display', 'none');
            break;
        case 9:
            console.log('9' + sOption);
            var leHiddenExercises = leExerciseBoxes.filter(':hidden');
            var iHiddenExercises = leHiddenExercises.length;
            var iCounter = 0;
            leHiddenExercises.filter(function (index) {
                var bShow = $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && ($(this).data('area') == sOption);
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_kinds.length > 0)
                    bShow = bShow && lsSelected_kinds.includes($(this).data('kind'));
                if (bShow)
                    iCounter++;
                return bShow;
            }).css('display', 'block');
            if (iCounter == iHiddenExercises)
                bIsFirstFiltering = true;
            break;

        case 10:
            console.log('10' + sOption);
            var leVisisbleExercises = leExerciseBoxes.filter(':visible');
            leVisisbleExercises.filter(function (index) {
                var bHide = ($(this).data('area') == sOption);

                return bHide;
            }).css('display', 'none');
            break;
        case 11:
            console.log('11' + sOption);
            var leHiddenExercises = leExerciseBoxes.filter(':hidden');
            var iHiddenExercises = leHiddenExercises.length;
            var iCounter = 0;
            leHiddenExercises.filter(function (index) {
                var bShow = $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_kinds.length > 0)
                    bShow = bShow && lsSelected_kinds.includes($(this).data('kind'));
                console.log($(this).data('area') + '  ' + bShow)
                if (bShow)
                    iCounter++;
                return bShow;
            }).css('display', 'block');
            if (iCounter == iHiddenExercises)
                bIsFirstFiltering = true;
            break;
        case 12:
            console.log('12' + sOption);
            var leVisisbleExercises = leExerciseBoxes.filter(':visible');
            leVisisbleExercises.filter(function (index) {
                var bShow = $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && ($(this).data('kind') == sOption);
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_areas.length > 0)
                    bShow = bShow && lsSelected_areas.includes($(this).data('area'));
                console.log($(this).data('area') + '  ' + bShow);
                return !bShow;
            }).css('display', 'none');
            break;
        case 13:
            console.log('13' + sOption);
            var leHiddenExercises = leExerciseBoxes.filter(':hidden');
            var iHiddenExercises = leHiddenExercises.length;
            var iCounter = 0;
            leHiddenExercises.filter(function (index) {
                var bShow = $(this).data('diff') >= liDiff_values[0] && $(this).data('diff') <= liDiff_values[1]; // eff + diff filter
                bShow = bShow && $(this).data('eff') >= liEff_values[0] && $(this).data('eff') <= liEff_values[1];
                if (lsSelected_areas.length > 0)
                    bShow = bShow && lsSelected_areas.includes($(this).data('area'));
                console.log($(this).data('area') + '  ' + bShow)
                if (bShow)
                    iCounter++;
                return bShow;
            }).css('display', 'block');
            if (iCounter == iHiddenExercises)
                bIsFirstFiltering = true;
            break;
        default:
            // Anweisungen werden ausgeführt,
            // falls keine der case-Klauseln mit expression übereinstimmt
            break;
    }
    // set Result label
    console.log('before setting results count');
    var iResults = leExerciseBoxes.filter(':visible').length;
    var eResult_el = document.getElementById('exercises_dlg_search_result_count');
    eResult_el.innerText = iResults;
    // #end set Resutl label
}