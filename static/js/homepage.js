



function toggleText(evt) {
  var id = 'poem_' + this.id;
  $("#" + id).toggle();
}

function highlightText(evt) {
  var id = this.id;
  var subj = "div[subjects*='"+ id +"']";
  $(subj).toggleClass("highlight");
}

function checkNoSpace(evt) {
  var textEntered = this.value;
  if (textEntered.indexOf(' ') > -1) {
    $('#error').html('Search word must be one word.');
  }
  else {
    $('#error').html('');
  }
}


$('.headline').on('click', toggleText)
$('li').on('click', highlightText)
$('.poembody').mark($('div[term]').attr('id'))
$('input').on('keyup', checkNoSpace);

