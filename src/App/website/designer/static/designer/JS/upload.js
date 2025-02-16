const upload_area = document.getElementById("upload-area");
const input_file = document.getElementById("input-file");
const img_view = document.getElementById("img-view");

input_file.addEventListener("change", uploadImage);

function uploadImage(){
    let img_link = URL.createObjectURL(input_file.files[0]);
    img_view.style.backgroundImage = `url(${img_link})`;
    img_view.textContent = "";
    img_view.style.border = 0;
}