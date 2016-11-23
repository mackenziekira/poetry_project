

function renderTable(data) {
    console.log(data);
    
    $.each(data, function(k, v) {
        $('#' + counter).append('<tr class=' + counter + '></tr>');
        $.each(v, function(i, j) {
            $('tr.' + counter + ':last').append('<td>' + j + '</td>');
        });
});
    counter++;
    
}

function fetchInfo(e) {
    var author = $('#authors :selected').text();
    $('#tables').append('<table class="table table-striped"><thead><tr><th>' + author + '</th></tr></thead><tbody id=' + counter + '></tbody></table>');
    var id = this.value;
    var url = '/author_lda/' + id + '.json';
    $.get(url, renderTable);
}

$('#authors').on('change', fetchInfo);
var counter = 0;

