const canvasContainer = document.querySelector(".content");
const canvas = new fabric.Canvas("canvas", { selection: false });
const inputFile = document.getElementById("input-file");
const uploadBtn = document.getElementById("upload-btn");
const clearButton = document.getElementById("clear-selection-btn");
canvas.setWidth(canvasContainer.clientWidth * 0.98);
canvas.setHeight(canvasContainer.clientHeight * 0.98);
canvas.allowTouchScrolling = true; // Allow touch and drag on mobile devices

let isDrawing = false;
let rect, startX, startY;

// Trigger file input when upload button is clicked
uploadBtn.addEventListener("click", function () {
    inputFile.click();
});

// Load Image into Fabric.js Canvas
inputFile.addEventListener("change", function (e) {
    const reader = new FileReader();
    reader.onload = function (event) {
        const imgObj = new Image();
        imgObj.onload = function () {
            const fabricImg = new fabric.Image(imgObj);
            
            // Scale the image to fit within the canvas
            const scaleFactor = Math.min(
                canvas.width / fabricImg.width,
                canvas.height / fabricImg.height
            );
            fabricImg.scale(scaleFactor);

            fabricImg.set({ selectable: false });
            canvas.setBackgroundImage(fabricImg, canvas.renderAll.bind(canvas));
        };
        imgObj.src = event.target.result;
    };
    reader.readAsDataURL(e.target.files[0]);
});

// Mouse Down - Start Drawing
canvas.on("mouse:down", function (event) {
    if (canvas.getActiveObject()) return; // Disable drawing if an object is active
    
    isDrawing = true;
    const pointer = canvas.getPointer(event.e);
    startX = pointer.x;
    startY = pointer.y;

    rect = new fabric.Rect({
        left: startX,
        top: startY,
        width: 0,
        height: 0,
        fill: "transparent", // No fill, only border
        stroke: "red",
        strokeWidth: 2,
        selectable: true,
        hasControls: true,
    });

    canvas.add(rect);
});

// Mouse Move - Update Rectangle Size
canvas.on("mouse:move", function (event) {
    if (!isDrawing) return;
    const pointer = canvas.getPointer(event.e);
    rect.set({
        width: Math.abs(pointer.x - startX),
        height: Math.abs(pointer.y - startY),
        left: pointer.x < startX ? pointer.x : startX,
        top: pointer.y < startY ? pointer.y : startY,
    });
    canvas.renderAll();
});

// Mouse Up - Stop Drawing
canvas.on("mouse:up", function () {
    isDrawing = false;
});

// Double Click - Set Rectangle as Active Object if Clicked in Center
canvas.on("mouse:dblclick", function (event) {
    const pointer = canvas.getPointer(event.e);
    canvas.getObjects().forEach(obj => {
        if (obj.type === "rect") {
            const centerX = obj.left + obj.width / 2;
            const centerY = obj.top + obj.height / 2;
            const tolerance = Math.min(obj.width, obj.height) * 0.25; // 25% of smallest dimension
            
            if (
                Math.abs(pointer.x - centerX) <= tolerance &&
                Math.abs(pointer.y - centerY) <= tolerance
            ) {
                canvas.setActiveObject(obj);
                canvas.renderAll();
                console.log("Rectangle set as active object");
            }
        }
    });
});

// Clear All Selections
clearButton.addEventListener("click", function () {
    canvas.discardActiveObject(); // Deselect active object
    canvas.getObjects().forEach(obj => {
        canvas.remove(obj);
    });
    canvas.renderAll();
});
