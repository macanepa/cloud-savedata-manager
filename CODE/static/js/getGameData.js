$(function(){
	$('.game-li').click(function(){
		var li_id = $(this).attr('id');
		console.log(li_id);
		var gameName = document.getElementById(li_id).getAttribute("value");
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
				size = response['kb_filesize'];
				timestamp = response['timestamp'];
				gameName = response['game_name'];
				description = response['description'];

				document.getElementById('game-title').textContent = "Title: " + gameName;
				document.getElementById('path').textContent = "Location: " + path;
				document.getElementById('game-size').textContent = "Size: " + size + " Kb";
				document.getElementById('game-timestamp').textContent = "Timestamp: " + timestamp;
				document.getElementById('gameId').textContent = "id: " + id;
				document.getElementById('description').textContent = "Description: " + description;

				document.getElementById('ddownload-cloud-btn').disabled = false;
				document.getElementById('ddelete-cloud-btn').disabled = false;
				if (response['is_local']){
					console.log('is local: True');
					document.getElementById('uupload-cloud-btn').disabled = false;
				}
				else{
					console.log('disable the upload button')
					document.getElementById('uupload-cloud-btn').disabled = true;
				}

			},
			error: function(error){
				console.log(error);
			}
		});
	});

	$('#path').click(function(){
		var path = $(this).text();
		console.log(path);
		path = path.replace('Location:', '');
		console.log(path)
		if(path == ''){
			return
		}
		path = path;
		console.log('wiweño');
		console.log(path);
		$.ajax({
			url: '/open_location',
			data: {'path': path},
			type: 'GET',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});