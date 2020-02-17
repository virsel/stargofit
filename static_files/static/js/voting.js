
// like button
function like(event, url, like) {
    event.preventDefault();
    var pk = like.data('id');
    var action = like.data('action');

    // ajax request
    // send data
    $.post(url,
        {
            pk: pk,
            action: action,
        },
        // ###end### send data

        // get data + work with
        function (json) {
            if (json['status'] == 'ok') {

                // draw circle
                var id = 'circle-' + pk;
                var circle = document.getElementById(id);
                set_vote_circle(circle, json.percentage)
                // ###end### draw circle

                //$('span.dislike').text(json.dislike_count);
                //$('span.like').text(json.like_count);

                // for horizontal voting
                //var percentage = String(json.percentage + '%');
                //$('div.progress-bar').css('width',percentage);
            }
        }
        // ###end### get data + work with
    );
    // ###end### ajax request
}
// ###end### like button


// dislike button
function dislike(event, url, dislike) {
    event.preventDefault();
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    // ajax request
    // send data
    $.post(url,
        {
            pk: pk,
        },
        // ###end### send data

        // get data + work with
        function (json) {
            if (json['status'] == 'ok') {

                // draw circle
                var id = 'circle-' + pk;
                var circle = document.getElementById(id);
                set_vote_circle(circle, json.percentage)
                // ###end### draw circle

                //$('span.dislike').text(json.dislike_count);
                //$('span.like').text(json.like_count);

                // for horizontal voting
                //var percentage = String(json.percentage + '%');
                //$('div.progress-bar').css('width',percentage);
            }
        }
        // ###end### get data + work with
    );
    // ###end### ajax request
}
// ###end### dislike button

// draw all first rating circles...
var leVoting_circles = document.querySelectorAll('.user_voting_bar');
leVoting_circles.forEach(function (circle) {
    var percentage = parseInt(circle.dataset.percentage);

    set_vote_circle(circle, percentage);
});
// ###end### draw all first rating circles...

function set_vote_circle(circle, percentage) {
    $('.star_user_voting').attr('data-pct', percentage); // set circle percent content


    // change percent to circle conditions
    var r = circle.getAttribute('r');
    var c = Math.PI * (r * 2);
    var percentage = ((100 - percentage) / 100) * c;
    // ###end### change percent to circle conditions


    var $circle = $(circle);
    $circle.css({ strokeDashoffset: percentage });

}