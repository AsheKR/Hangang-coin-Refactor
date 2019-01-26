$(function() {
    $('#send_coin_name').click(function() {
        uri = $('input[type=radio][name=coin]:checked').val()
        window.location.href = '/coin/'+uri+'/'
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
                console.log(data);
            }
        })
    },

    set_interval: function() {
        globalVar.setFiveSc(setInterval(this.call_ajax, 10000))
    },

    change_html: function(json_data) {
        $('#today_master_value span').text(json_data['today_master_value'])
        $('#latest_value span').text(json_data['latest_value'])
        $('#percent').text(json_data['percent'])
    }
}