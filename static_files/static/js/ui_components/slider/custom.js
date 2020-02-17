function fSliderDoubleRange(sRange,sOutput,iStart,iEnd,iStep=1)
{
var eOutput = document.getElementById(sOutput);
var eSlider = document.getElementById(sRange); 

        noUiSlider.create(eSlider, {
        start: [ iStart, iEnd ], // Handle start position
        step: iStep,
        connect: [false, true,false],
        range: { // Slider can select '0' to '100'
            'min': iStart,
            'max': iEnd          
            },
    });
    

    // When the slider value changes, update the input and span
    eSlider.noUiSlider.on('update', function (values) {
        if (values[0] == values[1])
            eOutput.innerText = values[0]; 
        else
            eOutput.innerText = values[0] + ' - ' + values[1]; 
    });
    
return eSlider;
}