$('div#datepicker').datepicker({
    title: 'Календарь событий',
    inline: true,
    format: "dd-mm",
    maxViewMode: 1,
    todayBtn: "linked",
    language: "ru",
    daysOfWeekHighlighted: "0,6",
    todayHighlight: true
});
// previous format: "yyyy-mm-dd",
var path = window.location.pathname;

if (path.toLowerCase().indexOf('events/categories') !== -1) {
//  var re = /\d{4}-\d{2}-\d{2}/; <!-- previous format -->
    var re = /\d{2}-\d{2}/;
    var matches_array = path.match(re);
    var current_date = matches_array[0];
//    console.log(current_date);
    $('div#datepicker').datepicker('update', current_date);
    $('#my_hidden_input').val(current_date);

}
$('#datepicker').on('changeDate', function () {
    var date = $('#datepicker').datepicker('getFormattedDate');
//    console.log(date);
    window.location.href = '/events/categories/' + date + '/';
});