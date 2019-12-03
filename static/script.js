var size_init = 4;

$(document).ready(function() {
  for (var i = 1; i < size_init + 1; i++) {
    var name_input = $('<input type="text"><br/>');
    name_input.attr("name", "member");
    name_input.attr("placeholder", "Enter member " + i + "'s name");
    $("#group-entry").append(name_input);

    var email_input = $('<input type="text"><br/><br/>');
    email_input.attr("name", "email");
    email_input.attr("placeholder", "Enter member " + i + "'s email");
    $("#group-entry").append(email_input);
    // $("input").addClass("member");
  }

  $("#add-more").click(function() {
    size_init++;
    var name_input = $('<input type="text"><br/>');
    name_input.attr("name", "member" + size_init);
    name_input.attr("placeholder", "Enter member " + size_init + "'s name");
    $("#group-entry").append(name_input);

    var email_input = $('<input type="text"><br/><br/>');
    email_input.attr("name", "member" + size_init);
    email_input.attr("placeholder", "Enter member " + size_init + "'s name");
    $("#group-entry").append(email_input);
    //$("input").addClass("member");
  });
});
