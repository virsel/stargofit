


// save standard path class Names
document.querySelectorAll('.muscle').forEach(function (path) {
    Util.fSetExpandedStandardClassName(path, '');
});
// ###end### save standard path class Names


// set header input selection
function fSetMainLabel(sMuscle_name, bNew) {
    var eHelpElement = document.getElementById(sMuscle_name + '-i');
    var sMain_group = eHelpElement.className.split(' ')[1].replace('-input', '');

    // select if all sub inputs are selected
    if (bNew) {
        var leSub_input = document.querySelectorAll(".muscles-input." + sMain_group + "-input");
        var bSelect_header_input = true;
        leSub_input.forEach(function (sub_input) {
            if (!sub_input.checked)
                bSelect_header_input = false
        });
        if (bSelect_header_input) {
            var leHeader_input = document.querySelectorAll(".muscles-input-heading." + sMain_group + "-input");
            leHeader_input.forEach(function (header_input) {
                header_input.checked = true;
            });
            Util.toggleClass(document.getElementById(sMain_group), 'selected-muscle-group', true);
        }
    }
    // ###end### select if all sub inputs are selected


    // unselect if one sub input is not selected
    else {
        var leHeader_input = document.querySelectorAll(".muscles-input-heading." + sMain_group + "-input");
        leHeader_input.forEach(function (header_input) {
            header_input.checked = false;
        });
        var eMain_group = document.getElementById(sMain_group);
        Util.toggleClass(eMain_group, 'selected-muscle-group', false);
    }
    // ###end### unselect if one sub input is not selected
}
// ###end### set header input selection


// change visibility of muscle groups
function fChangeMuscleGroupVisibility(sMuscle_name, bIs_new, bMuscle_group_clicked, sMuscle_group) {

    console.log(sMuscle_name);
    console.log(bIs_new);
    console.log(bMuscle_group_clicked);
    console.log(sMuscle_group);
    // for clicked muscle main group
    if (bMuscle_group_clicked) {

        // ###end### check if selected muscle group is first new
        var seSelected_muscle_shapes = document.querySelectorAll('g .selected');
        var iSelected_shapes_count = seSelected_muscle_shapes.length;
        var bIs_first_new = false;
        if (iSelected_shapes_count == 0)
            bIs_first_new = true;


        // unselect muscle group
        if (bIs_new == false) {
            var iM_shapes = document.querySelectorAll('.' + sMuscle_group + '-shape').length;
            // unselect Muscle group + light blue shape color
            if (iM_shapes == iSelected_shapes_count) {
                fSelectMuscles(1, null, sMuscle_group)
            }
            // ###end### unselect Muscle group + light blue shape color

            else {
                fSelectMuscles(2, null, sMuscle_group)
            }

            return;
        }

        // ###end### unselect muscle group


        else {

            // first selected muscle group
            if (bIs_first_new && bIs_new) {
                fSelectMuscles(3, null, sMuscle_group);
            }
            // ###end### first selected muscle group


            // only one new selected muscle group
            else if (bIs_new) {
                fSelectMuscles(4, null, sMuscle_group);
            }
            // ###end### only one new selected muscle group


            // one less muscle group
            else {
                fSelectMuscles(2, null, sMuscle_group);
            }
            return; // end function
            // ###end### one less muscle group
        }
    }

    // ###end### for clicked muscle main group


    // for clicked muscle sub group
    else {
        var iSelected_muscles_count = document.querySelectorAll('g .selected').length;
        if (!bIs_new) {
            if (iSelected_muscles_count == 1) { // all muscle groups must be visible
                fSelectMuscles(5, sMuscle_name, null);
            }
            else {
                fSelectMuscles(6, sMuscle_name, null);
            }
            return;
        }
        else {
            // first selected muscle group
            if (iSelected_muscles_count == 0 && bIs_new) {
                fSelectMuscles(7, sMuscle_name, null);
                return; // end function
            }
            // ###end### first selected muscle group


            // only one new selected muscle group           
            else {
                fSelectMuscles(8, sMuscle_name, null);
            }
            // ###end### only one new selected muscle group
        }
    }
    // ###end### for clicked muscle sub group
}
// ###end### change visibility of muscle groups


// select all muscle group shapes
document.querySelectorAll(".main_shape").forEach(function (group) {
    // muscle group shapes hoover effect
    group.addEventListener('mouseover', function (el) {
        let sMuscle_group = group.id;
        let leLabels = document.querySelectorAll("." + sMuscle_group + '-input')
        if (leLabels) {
            leLabels.forEach(function (label) {
                if (label.classList)
                    label.classList.add("hover")
                else
                    label.className += ' ' + "hover"
            });
        }
    })


    group.addEventListener('mouseout', function (el) {
        let sMuscle_group = group.id;
        let leLabels = document.querySelectorAll("." + sMuscle_group + '-input')
        if (leLabels) {
            leLabels.forEach(function (label) {
                if (label.classList)
                    label.classList.remove("hover")
                else
                    label.className = label.className.replace("hover", '');
            });
        }
    })
    // ###end### muscle group shapes hoover effect


    // click on muscle group shape
    group.addEventListener('click', function (el) {

        let sMuscle_group = group.id;
        // switch label selection
        let leInputs = document.querySelectorAll('.' + sMuscle_group + '-input');
        var bIs_checked = leInputs[0].checked;

        // ###end### handle one only element and check if selected
        if (bIs_checked) {
            fChangeMuscleGroupVisibility(null, false, true, sMuscle_group);
        }
        else {
            fChangeMuscleGroupVisibility(null, true, true, sMuscle_group);
        }
    })
    // ###end### click on muscle group shape
})
// ###end### select all muscle group shapes


// click on muscle group label
document.querySelectorAll(".muscle-groups label").forEach(function (group) {


    // muscle group label hoover effect
    group.addEventListener('mouseover', function (el) {
        // set variables
        let lsMuscle_label_class = group.getAttribute('class').split('-');
        let sMuscle_name = lsMuscle_label_class[1];
        let sMuscle_group_name = '';
        let bMuscle_group_clicked = false;
        if (lsMuscle_label_class[0] == 'heading') { // check if muscle group heading was clicked
            bMuscle_group_clicked = true;

            sMuscle_group_name = sMuscle_name;
        }

        let eInput = document.getElementById(sMuscle_name + '-i')
        // ###end### set variables
        if (eInput.checked) {
            // do something 
        }
        else {
            if (bMuscle_group_clicked) {
                let leMuscle_shapes = document.querySelectorAll('.' + sMuscle_group_name + '-shape');
                leMuscle_shapes.forEach(function (shape) {
                    // switch muscle group shape selection
                    Util.toggleClass(shape, 'muscle-label-hover', true);
                    // ###end### switch muscle group shape selection
                });
            }
            else {
                let eMuscle_shape = document.getElementById(sMuscle_name + '-shape');

                // switch muscle group shape selection
                Util.toggleClass(eMuscle_shape, 'muscle-label-hover', true);
                // ###end### switch muscle group shape selection
            }
        }
    });





    group.addEventListener('mouseout', function (el) {
        // set variables
        let lsMuscle_label_class = group.getAttribute('class').split('-');
        let sMuscle_name = lsMuscle_label_class[1];
        let sMuscle_group_name = '';
        let bMuscle_group_clicked = false;
        if (lsMuscle_label_class[0] == 'heading') { // check if muscle group heading was clicked
            bMuscle_group_clicked = true;

            sMuscle_group_name = sMuscle_name;
        }
        if (bMuscle_group_clicked) {
            let leMuscle_shapes = document.querySelectorAll('.' + sMuscle_group_name + '-shape');
            leMuscle_shapes.forEach(function (shape) {
                // switch muscle group shape selection
                Util.toggleClass(shape, 'muscle-label-hover', false);
                // ###end### switch muscle group shape selection
            });
        }
        else {
            let eMuscle_shape = document.getElementById(sMuscle_name + '-shape');

            // switch muscle group shape selection
            Util.toggleClass(eMuscle_shape, 'muscle-label-hover', false);
            // ###end### switch muscle group shape selection
        }
    })
    // ###end### muscle group label hoover effect


    group.addEventListener('click', function () {

        // set variables
        let lsMuscle_label_class = group.getAttribute('class').split('-');
        let sMuscle_name = lsMuscle_label_class[1];
        let sMuscle_group_name = '';
        let bMuscle_group_clicked = false;
        if (lsMuscle_label_class[0] == 'heading') { // check if muscle group heading was clicked
            bMuscle_group_clicked = true;
            sMuscle_group_name = sMuscle_name;
        }
        let eInput = document.getElementById(sMuscle_name + '-i');
        // ###end### set variables


        if (eInput.checked) {
            if (bMuscle_group_clicked) {
                fChangeMuscleGroupVisibility(null, false, bMuscle_group_clicked, sMuscle_group_name);
            }
            else {
                fChangeMuscleGroupVisibility(sMuscle_name, false, false, null);
            }
        }
        else {
            if (bMuscle_group_clicked) {
                fChangeMuscleGroupVisibility(null, true, bMuscle_group_clicked, sMuscle_group_name);
            }
            else {
                fChangeMuscleGroupVisibility(sMuscle_name, true, false, null);
            }
        }
    })
})
// ###end### click on muscle group label


// Select all button
$('#select_all_btn').on('click', function (eButton) {

    eButton.preventDefault();

    console.log(eButton);

    if ($(this).hasClass('clickable')) {
        document.querySelectorAll(".muscle").forEach(function (path) {
            Util.fSetExpandedStandardClassName(path, 'path-start'); // fill all shapes with light blue 
        });


        $(this).removeClass('clickable'); // make 'Select all' button not clickable


        // set corresponding muscle group unselected
        document.querySelectorAll('.selected-muscle-group').forEach(function (group) {
            Util.toggleClass(group, 'selected-muscle-group', false);
        });
        // ###end### set corresponding muscle group unselected

        document.querySelectorAll('.muscles-input').forEach(function (input) {
            input.checked = false;
        });
        document.querySelectorAll('.muscles-input-heading').forEach(function (input) {
            input.checked = false;
        });

        field = 'all'; // for django request
        names = [];
        fGetExercisesPerConditions();
    }
});
// ###end### Select all button


// selection function
// 1 : unselect Muscle group + light blue shape color
// 2 : unselect Muscle group
// 3 : select first muscle group + grey shape color
// 4 : select muscle group
// 5 : unselect muscle shape + light blue shape color
// 6 : unselect muscle shape 
// 7 : select first muscle shape + grey shape color
// 8 : select muscle shape
function fSelectMuscles(int, sMuscle_shape, sMuscle_group) {
    console.log(int);
    switch (int) {
        case 1:
            // change input element selection
            document.querySelectorAll("." + sMuscle_group + "-input").forEach(function (input) {
                input.checked = false;
                fSetRequestListValues(input, true);
            });


            // set light blue muscle shape
            document.querySelectorAll('.muscle').forEach(function (path) {
                Util.fSetExpandedStandardClassName(path, 'path-start');
            });
            // ###end### set light blue muscle shape


            $('#select_all_btn').removeClass('clickable'); // make 'Select all' button clickable

            Util.toggleClass(document.getElementById(sMuscle_group), 'selected-muscle-group', false);

            field = 'all';
            names = [];
            fGetExercisesPerConditions();
            break;

        case 2:
            // change input element selection
            document.querySelectorAll("." + sMuscle_group + "-input").forEach(function (input) {
                input.checked = false;
                fSetRequestListValues(input, true); // true for erase
            });
            // set unselected grey muscle shape
            document.querySelectorAll('.' + sMuscle_group + '-shape').forEach(function (path) {
                Util.fSetExpandedStandardClassName(path, 'path-unselected');
            });
            // ###end### set light blue muscle shape

            Util.toggleClass(document.getElementById(sMuscle_group), 'selected-muscle-group', false);

            field = 'muscle';
            fGetExercisesPerConditions();
            break;

        case 3:
            // change input element selection
            document.querySelectorAll("." + sMuscle_group + "-input").forEach(function (input) {
                input.checked = true;
                fSetRequestListValues(input, false); // false for push
            });


            $('#select_all_btn').addClass('clickable'); // make 'Select all' button clickable

            console.log('3');

            // set unselected grey muscle shape and selected muscle shape
            document.querySelectorAll('.muscle').forEach(function (path) {
                if ((path.getAttribute('class').split(' ')[1].replace('-shape', '')) == sMuscle_group) {
                    Util.fSetExpandedStandardClassName(path, '');
                    Util.toggleClass(path, 'selected', true);
                }
                else {
                    Util.fSetExpandedStandardClassName(path, 'path-unselected');
                    console.log('3 unselected');
                }
            });
            // ###end### set unselected grey muscle shape and selected muscle shape

            Util.toggleClass(document.getElementById(sMuscle_group), 'selected-muscle-group', true);

            // set ajax database request
            field = 'muscle';
            fGetExercisesPerConditions();
            // ###end### set ajax database request
            break;

        case 4:
            // change input element selection
            document.querySelectorAll("." + sMuscle_group + "-input").forEach(function (input) {
                input.checked = true;
                fSetRequestListValues(input, false); // false for push
            });
            // set selected muscle shape
            document.querySelectorAll('.' + sMuscle_group + '-shape').forEach(function (path) {
                Util.fSetExpandedStandardClassName(path, '');
                Util.toggleClass(path, 'selected', true);
            });
            // ###end### set selected muscle shape

            Util.toggleClass(document.getElementById(sMuscle_group), 'selected-muscle-group', true);

            // set ajax database request
            field = 'muscle';
            fGetExercisesPerConditions();
            // ###end### set ajax database request


            break;


        case 5:

            document.querySelectorAll(".muscle").forEach(function (path) {
                Util.fSetExpandedStandardClassName(path, 'path-start'); // fill all shapes with light blue 
            });

            var eInput = document.getElementById(sMuscle_shape + '-i'); // unselect input
            eInput.checked = false;

            fSetRequestListValues(eInput, true); // false for push, 

            $('#select_all_btn').removeClass('clickable'); // make 'Select all' button clickable

            // set corresponding muscle group unselected
            var sMain_group = eInput.className.split(' ')[1].replace('-input', '');
            Util.toggleClass(document.getElementById(sMain_group), 'selected-muscle-group', false);
            // ###end### set corresponding muscle group unselected

            field = 'all';
            names = [];
            fGetExercisesPerConditions();

            break;


        case 6:

            var eInput = document.getElementById(sMuscle_shape + '-i'); // unselect input
            eInput.checked = false;


            fSetMainLabel(sMuscle_shape, false); // false for one less muscle shape

            Util.fSetExpandedStandardClassName(document.getElementById(sMuscle_shape + '-shape'), 'path-unselected'); // unselect shape

            // set ajax database request
            field = 'muscle';
            fSetRequestListValues(eInput, true); // false for one less, 
            fGetExercisesPerConditions();
            // ###end### set ajax database request


            break;

        case 7:
            var eInput = document.getElementById(sMuscle_shape + '-i'); // unselect input
            eInput.checked = true;





            Util.toggleClass(document.getElementById('select_all_btn'), 'clickable', true); // make 'Select all' button clickable


            // set unselected grey muscle shape and selected muscle shape
            let paths = document.querySelectorAll('.muscle');
            paths.forEach(function (path) {
                Util.fSetExpandedStandardClassName(path, 'path-unselected');
            });
            // ###end### set unselected grey muscle shape and selected muscle shape

            Util.fSetExpandedStandardClassName(document.getElementById(sMuscle_shape + '-shape'), 'selected'); // select clicked muscle shape

            // get exercises per muscle group
            field = 'muscle';
            fSetRequestListValues(eInput, false); // false for push, 
            fGetExercisesPerConditions();
            // ###end### get exercises per muscle group
            break;


        case 8:
            var eInput = document.getElementById(sMuscle_shape + '-i'); // unselect input
            eInput.checked = true;



            Util.fSetExpandedStandardClassName(document.getElementById(sMuscle_shape + '-shape'), 'selected'); // select clicked muscle shape

            fSetMainLabel(sMuscle_shape, true); // true for new muscle shape

            // get exercises per muscle group
            field = 'muscle';
            fSetRequestListValues(eInput, false); // false for push, 
            fGetExercisesPerConditions();
            // ###end### get exercises per muscle group
            break;
        default:
            res.innerHTML = 'N�sse';
    }
}


function fSetRequestListValues(eDomElement, bErase) {
    var bMain_group = eDomElement.className.split(' ')[0] == 'muscles-input-heading';

    if (!bMain_group) {
        if (bErase) {
            // erase each sub muscle from main muscle group
            sName = eDomElement.id.replace('-i', '');
            var index = names.indexOf(sName);
            console.log(names + ' ' + names.indexOf(sName) + ' ' + sName);
            if (index > -1) {
                names.splice(index, 1);
            }
            // ### end ### erase each sub muscle from main muscle group
        }
        else {
            sName = eDomElement.id.replace('-i', '');
            if (names.indexOf(sName) == -1)
                names.push(sName); // apend all muscle sub groups
        }
    }
}
