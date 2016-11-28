

function renderTable(data) {
    $.each(data, function(key, value) {
        $('#' + counter).append('<td>' + value.count + ': ' + value.word + '</td>');
});
    counter++;
    
}

function fetchInfo(e) {
    var id = this.value;
    var subject = $('#subjects :selected').text();
    $('tbody').append('<tr id=' + counter + '><td><b>' + subject + '</b></td></tr>');
    var url = '/subject_info/' + id + '.json';
    $.get(url, renderTable);
}

$('#subjects').on('change', fetchInfo);
var counter = 0;
