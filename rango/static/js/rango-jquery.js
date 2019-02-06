$(document).ready( function() {

    $("#about-btn").click( function(event) {
        msgstr = $("#msg").html()
        msgstr = msgstr + "o"
        $("#msg").html(msgstr)
    });
    $("p").hover( function() {
            $("#about-btn").css('color', 'red');
            $("p").css('color', 'green');
    },
    function() {
            $("#about-btn").css('color', 'blue');
            $('p').css('color', 'yellow');
    });
});

