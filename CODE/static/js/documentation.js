window.onload = function() {
  $(function(){
		$.ajax({
					url: '/check_credentials',
					data: {},
					type: 'GET',
					success: function(response){
						console.log(response);

					},
					error: function(error){
						console.log(error);
					}
				});
});
};

function refreshPage(){
		    window.location.reload();
		}

$(function(){
	$("#redirect-index").click(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
	window.location.href = "/";
	});
});




