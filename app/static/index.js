$(function() {

    $('#select-coin-button').click(function() {
        $('#select_coin').css('display', 'block')
    })

    $('#send_coin_name').click(function() {
        uri = $('input[type=radio][name=coin]:checked').val()
        window.location.href = '/coin/'+uri+'/'
    })

    $('#send_coin_exit').click(function() {
        $('#select_coin').css('display', 'none')
    })

    ChangeHTML.init()
})

var globalVar = (function() {
    var _fiveSc = 0,
        _now_coin = '';

    var setNowCoin = function(now_coin) {
        _now_coin = now_coin
    }

    var getNowCoin = function() {
        return _now_coin
    }

    var setFiveSc = function(fiveSc) {
        _fiveSc = fiveSc;
    }

    var getFiveSc = function() {
        return _fiveSc;
    }

    return {
        setFiveSc: setFiveSc,
        getFiveSc: getFiveSc,
        setNowCoin: setNowCoin,
        getNowCoin: getNowCoin
    }
}())

var ChangeHTML = {
    init: function() {
        globalVar.now_coin = $('input[type=radio][name=coin]:checked').val()
        this.call_ajax()
        this.set_interval()
    },

    call_ajax: function() {
        url = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api/coin/' + globalVar.now_coin;

        $.ajax({
            type: "GET",
            url: url,
            success: function(data) {
                ChangeHTML.change_html(data);
            }
        })
    },

    set_interval: function() {
        globalVar.setFiveSc(setInterval(this.call_ajax, 10000))
    },

    change_html: function(json_data) {

        $('#today_master_value span').text(json_data['today_master_value'])
        $('#latest_value span').text(json_data['latest_value'])
        $('#section1').css('background-image', 'url("'+json_data['image']+'")')
        $('#percent span').text(json_data['percent'])

        $('#percent .fas').removeClass('fa-sort-down')
        $('#percent .fas').removeClass('fa-sort-up')

        if (json_data['today_master_value'] > json_data['latest_value']) {
            $('#latest_value').css('color', 'red')
            $('#percent').css('color', 'red')
            $('#percent .fas').addClass('fa-sort-down')
        } else {
            $('#latest_value').css('color', 'green')
            $('#percent').css('color', 'green')
            $('#percent .fas').addClass('fa-sort-up')
        }
    }
}