window.addEventListener('load', function () {
  $('#id-alerta').hide();

})

function refreshPage(){
	window.location.reload();
}

function hide_alert() {
    setTimeout(function () {
		$('#id-alerta').hide();
    }, 3000);
}

function show_alert(text){
	$('#id-alerta').text(text);
	$('#id-alerta').show();
}

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
				show_alert('Upload completed successfully');
				hide_alert()
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
				document.getElementById('upload-cloud-btn').disabled = false;
				show_alert('Download completed successfully');
				hide_alert();
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


$(function(){
	$('#delete-cloud-btn').click(function(){
		console.log('Doing some cool stuff!')
		gameName = document.getElementById('game-title').textContent;
		gameName = gameName.replace('Title: ', '');
		console.log(gameName);
		$.ajax({
			url: '/delete_cloud',
			data: {'gameName': gameName},
			type: 'GET',
			success: function(response){
				console.log(response);
				document.getElementById('delete-cloud-btn').disabled = false;
				refreshPage();
				show_alert('Deleted savedata from Cloud');
				hide_alert();
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

