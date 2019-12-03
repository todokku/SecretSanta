var size_init = 4;

$(document).ready(function() {
  for (var i = 1; i < size_init+1; i++) {
    var name_input = $('<input type="text">');

    name_input.attr("name", "member" + i);
    name_input.attr("placeholder", "Enter member " + i + "\'s name");

    $("#group-entry").append(name_input);         
  }

  $("#add-more").click(function() {

    size_init++;
    var name_input = $('<input type="text">');
    name_input.attr("name", "member" + size_init);
    name_input.attr("placeholder", "Enter member " + size_init + "\'s name");
    $("#group-entry").append(name_input)
  
  })
  // $("input").after("<br><br>")
})