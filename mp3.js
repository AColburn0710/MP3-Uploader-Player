function listMP3Files() {
	try{
		console.log('hello world')
	fetch('/list_files')
		.then(response => response.json())
		.then(data => {
			console.log("Received Data:", data);
			const mp3FileList = document.getElementById('mp3-file-list');
			mp3FileList.innerHTML = '';
			
			data.files.forEach(filename => {
				const listItem = document.createElement('li');
				listItem.innerHTML=filename;
				var functionString = 'playFile(\'' + filename + '\')';
				listItem.setAttribute("onclick", functionString);
				listItem.setAttribute("class", 'fileButton');
				mp3FileList.appendChild(listItem);
			});
		})
		
	}catch(error){
		console.error('Error fetching MP3 file list:', error);
		}
	
	
	document.getElementById('mp3-upload-form').addEventListener('submit', function (event) {
		event.preventDefault();
		
		const formData = new FormData(this);
		
		fetch('/upload', {
			method: 'POST',
			body: formData
		})
		.then(response => {
			if (response.ok) {
				alert('MP3 file uploaded successfully.');
				listMP3Files();
			} else {
				alert('Error uploading MP3 file.');
			}
		})
		.catch(error => console.error('Error uploading MP3 file:', error));
	})
	
};

function playFile(filename)
{
	fetch('/play/'+filename)
};
