$(function(){
	$('#upload-cloud-btn').click(function(){
		console.log('Doing some cool stuff!')
		gameName = document.getElementById('game-title').textContent;
		gameName = gameName.replace('Title: ', '');
		console.log(gameName);
		$.ajax({
			url: '/upload_cloud',
			data: {'gameName': gameName},
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

$(function(){
	$('#download-cloud-btn').click(function(){
		console.log('Doing some cool stuff!')
		gameName = document.getElementById('game-title').textContent;
		gameName = gameName.replace('Title: ', '');
		console.log(gameName);
		$.ajax({
			url: '/download_cloud',
			data: {'gameName': gameName},
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

