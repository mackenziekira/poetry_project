

function renderTable(data) {
    $('tbody').append('<tr id=' + counter + '>');
    $.each(data, function(key, value) {
        $('#' + counter).append('<td>' + value.count + ': ' + value.word + '</td>');
});
    $('tbody').append('</tr>');
    counter++;
    
}

function fetchInfo(e) {
    var id = this.value;
    console.log(id)
    var url = '/subject_info/' + id + '.json';
    $.get(url, renderTable);
}

$('#subjects').on('change', fetchInfo);
var counter = 0;
