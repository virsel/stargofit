var bFr_numb_is_one = true;
var bFr_label_is_sing = true;

// plus minus buttons
jQuery(document).ready(function () {
    // value increment
    $('[data-quantity="plus"]').click(function (e) {
        e.preventDefault();
        fieldName = $(this).attr('data-field');
        if (fieldName == 'frequenz_number') {
            bFr_numb_is_one = false;
            if (bFr_numb_is_one != bFr_label_is_sing)
                fSetFrequenzLabel(bFr_numb_is_one);
        }
       
        var currentVal = parseInt($('input[name=' + fieldName + ']').val());     
        if (!isNaN(currentVal) && currentVal < 364) {          
            $('input[name=' + fieldName + ']').val(currentVal + 1);
        } else {
            $('input[name=' + fieldName + ']').val(365);
        }
    });
    // ###end### value increment


   // value decrement
    $('[data-quantity="minus"]').click(function (e) {
        e.preventDefault();
        fieldName = $(this).attr('data-field');
        var currentVal = parseInt($('input[name=' + fieldName + ']').val());
        if (!isNaN(currentVal) && currentVal > 1) {
            var iNew_val = currentVal - 1;
          
            $('input[name=' + fieldName + ']').val(iNew_val);
            if (fieldName == 'frequenz_number') {
                bFr_numb_is_one = iNew_val == 1;
                if (bFr_numb_is_one != bFr_label_is_sing)
                    fSetFrequenzLabel(bFr_numb_is_one);
            }

        } else {
            $('input[name=' + fieldName + ']').val(1);
            if (fieldName == 'frequenz_number') {
                bFr_numb_is_one = true;
                if (bFr_numb_is_one != bFr_label_is_sing)
                    fSetFrequenzLabel(bFr_numb_is_one);
            }
        }
    });
 // value decrement

// ###end### plus minus buttons


    var eUnti_count = $('#unit-count');
    var eFrequenz_count = $('#frequenz-count');
// input event
    eUnti_count.on('input', function (e) {
        console.log('focused');
        var iUnit_count = parseInt(this.value);
        if (iUnit_count > 365) {
            this.value = 365;
        }
        else if (iUnit_count < 1) {
            this.value = 1;
        }
    });

    eFrequenz_count.on('input', function (e) {
        console.log('focused');
        var iUnit_count = parseInt(this.value);
        if (iUnit_count > 365) {
            this.value = 365;
        }
        else if (iUnit_count < 1)
            this.value = 1;
        bFr_numb_is_one = (this.value == 1);
        if (bFr_numb_is_one != bFr_label_is_sing)
            fSetFrequenzLabel(bFr_numb_is_one);
    });
// ###end### input event


// set Frequenz Label corresponding to count
    function fSetFrequenzLabel(bFr_numb_is_one) {
        if (bFr_numb_is_one) {
            document.querySelectorAll('.fr-lab-sing').forEach(function (eSing_label) {
                Util.toggleClass(eSing_label, 'fr-lab-sing-active', true);
            });
            document.querySelectorAll('.fr-lab-pl').forEach(function (eSing_label) {
                Util.toggleClass(eSing_label, 'fr-lab-pl-active', false);
            });
            bFr_label_is_sing = true;
        }
        else {
            document.querySelectorAll('.fr-lab-sing').forEach(function (eSing_label) {
                Util.toggleClass(eSing_label, 'fr-lab-sing-active', false);
            });
            document.querySelectorAll('.fr-lab-pl').forEach(function (eSing_label) {
                Util.toggleClass(eSing_label, 'fr-lab-pl-active', true);
            });
            bFr_label_is_sing = false;
        }
    }
// ###end### set Frequenz Label corresponding to count

});

