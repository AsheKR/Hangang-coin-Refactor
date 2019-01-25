$(function() {
    $('#send_coin_name').click(function() {
        uri = $('input[type=radio]:checked').val()
        location.href = 'coin/'+uri+'/'
    })
})