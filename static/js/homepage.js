



function toggleText(evt) {
  var id = 'poem_' + this.id;
  $("#" + id).toggle();
}

function highlightText(evt) {
  var id = this.id;
  var subj = "div[subjects*='"+ id +"']";
  $(subj).toggleClass("highlight");
}


$('.headline').on('click', toggleText)
$('li').on('click', highlightText)
$('.poembody').mark($('div[term]').attr('id'))
