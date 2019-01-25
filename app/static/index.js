$(function() {
    $('#send_coin_name').click(function() {
        uri = $('input[type=radio][name=coin]:checked').val()
        window.location.href = '/coin/'+uri+'/'
    })
})