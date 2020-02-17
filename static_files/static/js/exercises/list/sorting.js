// sorting button

// variables
var eSorting_selected = document.getElementById('sorting-selected');
var eSorting = document.getElementById('sorting-button');
var sSorting = '';
var eSort_descending = document.getElementById('absteigend');
var eSort_ascending = document.getElementById('aufsteigend');
var eSort_asc_bg = document.getElementById('asc-bg');
var eSort_desc_bg = document.getElementById('desc-bg');
var eSort_circle = document.getElementById('sorting-circle');
// ###end###  variables

// open menu event
eSorting.addEventListener('click', function () {
    eSorting.setAttribute('style', 'height: 0px;');
    eSorting_selected.setAttribute('style', 'height: auto;');
});
// ###end### open menu event


// close-icon event
document.getElementById('close-button').addEventListener('click', function () {
    eSorting_selected.setAttribute('style', 'height: 0px;');
    eSorting.setAttribute('style', 'height: auto;');
});
// ###end### close-icon event


// sorting ascending
Array.from(eSort_ascending.children).forEach(function (element) {
    element.addEventListener('click', function (button) {
        console.log('sortieren-aufsteigend');
        if (sSorting == 'up') {
            sSorting = '';
            Util.toggleClass(eSort_asc_bg, 'sorting-selected', false);
            Util.toggleClass(eSort_circle, 'sorting-circle-in-use', false); 
        }
        else {
            if (sSorting == 'down')
                Util.toggleClass(eSort_desc_bg, 'sorting-selected', false);

            sSorting = 'up';
            Util.toggleClass(eSort_asc_bg, 'sorting-selected', true);

            Util.toggleClass(eSort_circle, 'sorting-circle-in-use', true); // mark sort circle as used
        }
        fGetExercisesPerConditions()
    });
});
// ###end### sorting ascending


// sorting descending
Array.from(eSort_descending.children).forEach(function (element) {
    element.addEventListener('click', function (button) {
        console.log('sortieren-aubsteigend');
        if (sSorting == 'down') {
            sSorting = '';
            Util.toggleClass(eSort_desc_bg, 'sorting-selected', false);
            Util.toggleClass(eSort_circle, 'sorting-circle-in-use', false); 
        }
        else {
            if (sSorting == 'up')
                Util.toggleClass(eSort_asc_bg, 'sorting-selected', false);

            sSorting = 'down';
            Util.toggleClass(eSort_desc_bg, 'sorting-selected', true);
            Util.toggleClass(eSort_circle, 'sorting-circle-in-use', true); // mark sort circle as used
        }
        fGetExercisesPerConditions();
    });
});
// ###end### sorting descending
// ###end### sorting button

