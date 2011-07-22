/* Author: Chris Barna */
var pad = function (number, length) {
    var str = number.toString();
    while (str.length < length) {
        str = '0' + str;
    }
    return str;
};

var renderBarchart = function (fromDate, toDate) {
    $.ajax({
        url: '/api/tickets/both/' + fromDate.getFullYear() + '-' + pad(fromDate.getMonth() + 1, 2) + '-' + pad(fromDate.getDate(), 2) + '/' + toDate.getFullYear() + '-' + pad(toDate.getMonth() + 1, 2) + '-' + pad(toDate.getDate(), 2) + '/',
        dataType: 'json',
        success: function (data) {
            barchart.render(fromDate.getTime(), toDate.getTime(), data);
        }
    });
};

$(function () {

    $("#from, #to").datepicker({
        changeMonth: true,
        onSelect: function () {
            $("#chart").html('');
            renderBarchart($('#from').datepicker('getDate'), $('#to').datepicker('getDate'));
        }
    });
    $('#to').datepicker('setDate', new Date());
    $('#from').datepicker('setDate', -28);

    renderBarchart($("#from").datepicker('getDate'), $("#to").datepicker('getDate'));

});

