$(function(){
	$('li').click(function(){
		var gameName = $(this).text();
		console.log('wiweño')
		console.log(gameName)
		$.ajax({
			url: '/games',
			data: {'gameName': gameName},
			type: 'GET',
			success: function(response){
				console.log(response);
				id = response['id'];
				path = response['path'];
				gameName = response['game_name'];
				document.getElementById('game-title').textContent = "Title: " + gameName;
				document.getElementById('path').textContent = "Location: " + path;
				document.getElementById('gameId').textContent = "id: " + id;
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});