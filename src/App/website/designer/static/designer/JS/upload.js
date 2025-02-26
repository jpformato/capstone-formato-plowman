document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    const uploadContainer = document.querySelector('.upload-container');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const imgURL = URL.createObjectURL(this.files[0]);
                preview.src = imgURL;

                // Remove the dotted border when an image is uploaded
                uploadContainer.classList.add('uploaded');
            }
        });
    }
});
