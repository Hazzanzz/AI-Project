document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('sketch-upload');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a sketch.');
        return;
    }

    const formData = new FormData();
    formData.append('sketch', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload sketch');
        }

        const result = await response.json();
        const portraitUrl = result.portraitUrl;

        const portraitImg = document.getElementById('portrait');
        portraitImg.src = portraitUrl;

        document.getElementById('result').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Error uploading sketch');
    }
});
