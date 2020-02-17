function fGetPlanDetail(eSidebarContent, sNew_state, sDay) {
    if ($('#main_content').hasClass('all_training_plans')) {
        var settings = {
            'url': '/de/fitness/' + sNew_state,
            "method": "POST",
            'traditional': true,
            "data": { 'day': sDay }
        }
        $.ajax(settings).done(function (data) {
            console.log(data);
            eSidebarContent.empty();
            eSidebarContent.append(data);
            $('#main_content').attr('class', 'main_content training_plan_detail');
            history.pushState(null, null, '/de/fitness/' + sNew_state);
        });
    }
    else {
        location.href = '/de/fitness/plan/' + sNew_state;
    }
}


function fGetAllPlansContent() {
    var settings = {
        'url': '/de/fitness/all_training_plans/',
        "method": "POST",
        'traditional': true,
        "data": {}
    }
    $.ajax(settings).done(function (data) {
        console.log(data);
        eSidebarContent.empty();
        eSidebarContent.append(data);
        $('#main_content').attr('class', 'main_content all_training_plans');
        fSetOptionMenu();
    });
}

