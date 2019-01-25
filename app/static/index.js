$(function() {
    $('#send_coin_name').click(function() {
        uri = $('input[type=radio]:checked').val()
        window.location.href = '/coin/'+uri+'/'
    })
})