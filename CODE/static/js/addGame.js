function refreshPage(){
		    window.location.reload();
		}

$(function(){
	$("#new-game-form").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = '/addGame';

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               console.log(data);
               refreshPage();
           }
         });
	});
});