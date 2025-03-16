const canvasContainer = document.querySelector(".content");
const canvas = new fabric.Canvas("canvas", { selection: false });

const inputFile = document.getElementById("input-file");
const uploadBtn = document.getElementById("upload-btn");
const clearButton = document.getElementById("clear-selection-btn");
const windowList = document.querySelector(".window-list");
const rectangleMap = {};

canvas.setWidth(canvasContainer.clientWidth * 0.98);
canvas.setHeight(canvasContainer.clientHeight * 0.98);
canvas.allowTouchScrolling = true; // Allow touch and drag on mobile devices

let isDrawing = false;
let rect, startX, startY;
let rectangleCount = 0;
let imageUploaded = false;

canvas.on("mouse:down", onMouseDown);
canvas.on("mouse:move", onMouseMove);
canvas.on("mouse:up", onMouseUp);
canvas.on("mouse:dblclick", mouseDbClick);

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
            imageUploaded = true;
        };
        imgObj.src = event.target.result;
    };
    reader.readAsDataURL(e.target.files[0]);
});

// Mouse Down - Start Drawing
function onMouseDown(event) {
    if (canvas.getActiveObject()) return;   // Disable drawing if an object is active
    if (!imageUploaded) return;             // Ensure an image is uploaded before drawing

    isDrawing = true;
    const pointer = canvas.getPointer(event);
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
}

// Mouse Move - Update Rectangle Size
function onMouseMove(event){
    if (!isDrawing) return;
    const pointer = canvas.getPointer(event);
    rect.set({
        width: Math.abs(pointer.x - startX),
        height: Math.abs(pointer.y - startY),
        left: pointer.x < startX ? pointer.x : startX,
        top: pointer.y < startY ? pointer.y : startY,
    });
    canvas.renderAll();
}

// Mouse Up - Stop Drawing
function onMouseUp(event) {
    isDrawing = false;
    if (!imageUploaded) return; // Ensure an image is uploaded before finalizing the rectangle

    rectangleCount++;

    // Assign a unique ID to the rectangle
    const rectId = `rect-${rectangleCount}`;
    rect.set("id", rectId); 

    // Store rectangle reference globally
    rectangleMap[rectId] = rect;

    // Create a new window button
    const newWindowButton = document.createElement("div");
    newWindowButton.classList.add("window");
    newWindowButton.dataset.rectId = rectId;

    // Create delete button with trash icon
    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete-window-btn");
    deleteButton.innerHTML = newWindowButton.innerHTML = 
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
        </svg>`
    ;

    // Append delete button to window button then window button to window list
    newWindowButton.innerHTML = `Window ${rectangleCount} `;
    newWindowButton.appendChild(deleteButton);
    windowList.appendChild(newWindowButton);

    // Add event listener to remove rectangle and button when clicked
    deleteButton.addEventListener("click", function () {
        const rectId = newWindowButton.dataset.rectId; // Get ID from dataset
        const rectangle = rectangleMap[rectId];

        if (rectangle) {
            canvas.remove(rectangle);       
            canvas.renderAll();
            newWindowButton.remove();
            delete rectangleMap[rectId];
        }
    });
}

// Double Click - Set Rectangle as Active Object if Clicked in Center
function mouseDbClick(event) {
    const pointer = canvas.getPointer(event);
    canvas.getObjects().forEach(obj => {
        if (obj.type === "rect") {
            const centerX = obj.left + obj.width / 2;
            const centerY = obj.top + obj.height / 2;
            const tolerance = Math.min(obj.width, obj.height) * 0.25;
            
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
}

// Clear All Selections
clearButton.addEventListener("click", function () {
    canvas.discardActiveObject(); 
    canvas.getObjects().forEach(obj => {
        canvas.remove(obj);
    });
    canvas.renderAll();

    windowList.innerHTML = "";  // Removes all window buttons
    rectangleCount = 0;         // Reset rectangle count
});
