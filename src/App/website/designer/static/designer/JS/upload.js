const canvasContainer = document.querySelector(".content");
const canvas = new fabric.Canvas("canvas", { selection: false });

const inputFile = document.getElementById("input-file");
const uploadBtn = document.getElementById("upload-btn");
const clearButton = document.getElementById("clear-selection-btn");
const saveButton = document.getElementById("save-project-btn");
const windowList = document.querySelector(".window-list");
const rectangleMap = {};

canvas.setWidth(canvasContainer.clientWidth * 0.98);
canvas.setHeight(canvasContainer.clientHeight * 0.98);
canvas.allowTouchScrolling = true; // Allow touch and drag on mobile devices

let isDrawing = false;
let rect, startX, startY;
let rectangleCount = 0;
let imageUploaded = false;
let isMoving = false; // Flag to prevent drawing while moving objects (check first comment in each mouse event function)

canvas.on("mouse:down", onMouseDown);
canvas.on("mouse:move", onMouseMove);
canvas.on("mouse:up", onMouseUp);

// Listen for when an object starts moving
canvas.on("object:moving", function () {
    isMoving = true;
    console.log("Moving an object, preventing new drawing.");
});

// Listen for when an object stops moving
canvas.on("object:modified", function () {
    isMoving = false;
    console.log("Object movement stopped.");
});

// Trigger file input when upload button is clicked
uploadBtn.addEventListener("click", function () {
    inputFile.click();
});

// Load Image into Fabric.js Canvas
inputFile.addEventListener("change", function (e) {
    const fileInput = e.target;
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);
        const csrfToken = document.querySelector('[name=csrf-token]').content;

        // Upload the image
        fetch('/upload-image/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Image uploaded successfully');

                // load image in canvas
                const reader = new FileReader();
                reader.onload = function(event) {
                    const imgObj = new Image();
                    imgObj.onload = function () {
                        const fabricImg = new fabric.Image(imgObj);
                        
                        // Scale image
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
                reader.readAsDataURL(file);
            } else {
                console.error('Failed to upload image:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

saveButton.addEventListener("click", function (e) {
    console.log("saving")
    windows = [];
    for(let rectId in rectangleMap) {
        const rectangle = rectangleMap[rectId];
        if(!rectangle) {
            console.log("NONE");
            return;
        }
        const frameId = rectangle.frameImage ? rectangle.frameImage.frameId : null;
        const x1 = Math.floor(rectangle.left);
        const y1 = Math.floor(rectangle.top);
        const x2 = Math.floor(rectangle.left + rectangle.width * rectangle.scaleX);
        const y2 = Math.floor(rectangle.top + rectangle.height * rectangle.scaleY);

        windows.push({x1, y1, x2, y2, frameId});
    }

    // Send window data to the backend
    const csrfToken = document.querySelector('[name=csrf-token]').content; // Get CSRF token
    fetch('/save-windows/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ windows: windows }) // Send windows array as JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("success")
        } else {
            console.log("fail")
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Mouse Down - Start Drawing
function onMouseDown(event) {
    console.log("IN CLICK DOWN")
    if (!imageUploaded || isMoving) return; // Ensure an image is uploaded before drawing

    const pointer = canvas.getPointer(event);
    const clicked = event.target;

    // if clicking frame then don't draw a rectangle
    if (clicked && clicked.frameId) {
        return;
    }

    const activeObject = canvas.getActiveObject();
    // If an existing rectangle is being resized, do not create a new one
    if (activeObject && activeObject.type === "rect") {
        console.log("Resizing existing rectangle, not drawing a new one.");
        return; 
    }

    isDrawing = true;
    startX = pointer.x;
    startY = pointer.y;

    console.log("Pointer:", pointer.x, pointer.y); // Debugging output


    rect = new fabric.Rect({
        left: startX,
        top: startY,
        width: 0,
        height: 0,
        fill: "transparent",
        stroke: "red",
        strokeWidth: 2,
        selectable: true,
        hasControls: true,
    });

    canvas.add(rect);
}

canvas.on('mouse:down', function (e) {
    const clickedObject = e.target;

    if (clickedObject && clickedObject.rectId) {
        const rectId = clickedObject.rectId;
        const rectangle = rectangleMap[rectId];

        if (rectangle) {
            canvas.setActiveObject(rectangle);
            canvas.renderAll();
        }

        // Prevent drawing new rectangles on image click
        isDrawing = false;
    }
});


// Mouse Move - Update Rectangle Size
function onMouseMove(event){
    if (!isDrawing || isMoving) return;
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
    console.log("ON MOUSE UP")
    const pointer = canvas.getPointer(event);
    
    isDrawing = false;
    if (!imageUploaded || isMoving) return; // Ensure an image is uploaded before finalizing the rectangle

    // If resizing an existing rectangle, do nothing
    const activeObject = canvas.getActiveObject();
    if (activeObject && activeObject.type === "rect" && activeObject.id) {
        console.log("Resized an existing rectangle. No new button created.");
        return;
    }

    // Prevent creating window buttons for invalid rectangles (width or height too small) 
    // Prevents creating a window on clicking and not dragging
    if (rect.width < 5 || rect.height < 5) {
        console.log("INVALID RECT")
        canvas.remove(rect);
        canvas.renderAll();
        return;
    }

    // Assign a unique ID to the rectangle
    const rectId = `rect-${rectangleCount}`;
    rect.set("id", rectId); 

    // Store rectangle reference globally
    rectangleMap[rectId] = rect;

    canvas.setActiveObject(rect);
    canvas.renderAll();
    console.log("Rectangle set as active object");

    // Create a new window button
    const newWindowButton = document.createElement("button");
    newWindowButton.classList.add("window", "window-button");
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

    rectangleCount++;

    // Append delete button to window button then window button to window list
    newWindowButton.innerHTML = `Window ${rectangleCount} `;
    newWindowButton.appendChild(deleteButton);
    windowList.appendChild(newWindowButton);

    // Add event listener to remove rectangle and button when clicked
    deleteButton.addEventListener("click", function (e) {
        const rectId = newWindowButton.dataset.rectId; // Get ID from dataset
        const rectangle = rectangleMap[rectId];

        if (rectangle) {
            const frameImage = canvas.getObjects().find(obj => obj.rectId === rectId);
            if (frameImage) {
                canvas.remove(frameImage); // Remove frame image from canvas
            }
            canvas.remove(rectangle);       
            canvas.renderAll();
            newWindowButton.remove();
            delete rectangleMap[rectId];
        }

        e.stopPropagation();
    });

    newWindowButton.addEventListener("click", function () {
        console.log("Opening popup...");
        const popup = document.getElementById("popup");
        popup.dataset.targetRectId = newWindowButton.dataset.rectId;

        fetch('/get-frames/')
            .then(response => response.json())
            .then(data => {
                const frameContainer = document.getElementById("frame-options");
                frameContainer.innerHTML = ""; // clear old content

                data.frames.forEach(frame => {
                    const frameDiv = document.createElement("div");
                    frameDiv.classList.add("frame-option");
                    frameDiv.style.cursor = "pointer";
                    frameDiv.style.marginBottom = "10px";

                    frameDiv.innerHTML = `
                        <p>${frame.name}</p>
                        <img src="${frame.image}" alt="${frame.name}" style="width: 100px; height: auto;" />
                    `;

                    canvas.on('object:moving', function (e) {
                        const object = e.target;
                    
                        // Check if rectangle is being moved and find its frame
                        if (object.type === 'rect') {
                            const frameImage = canvas.getObjects().find(obj => obj.rectId === object.id);
                            if (frameImage) {
                                // Change position to same as rectangle
                                frameImage.set({
                                    left: object.left,
                                    top: object.top,
                                });
                                canvas.renderAll();
                            }
                        }
                    });

                    canvas.on('object:scaling', function (e) {
                        const object = e.target;
                    
                        // Check if rectangle and find frame
                        if (object.type === 'rect') {
                            const frameImage = canvas.getObjects().find(obj => obj.rectId === object.id);
                            if (frameImage) {
                                const newWidth = object.width * object.scaleX;
                                const newHeight = object.height * object.scaleY;
                    
                                // Update the frame size and position
                                frameImage.set({
                                    left: object.left,
                                    top: object.top,
                                    scaleX: newWidth / frameImage.width,
                                    scaleY: newHeight / frameImage.height,
                                });
                                canvas.renderAll();
                            }
                        }
                    }); 

                    frameDiv.addEventListener("click", () => {
                        const rectId = popup.dataset.targetRectId;
                        const rectangle = rectangleMap[rectId];

                        if (rectangle) {
                            // If window has a frame remove the frame from canvas
                            if (rectangle.frameImage) {
                                canvas.remove(rectangle.frameImage);
                            }

                            fabric.Image.fromURL(frame.image, function (img) {
                                const actualWidth = rectangle.width * rectangle.scaleX;
                                const actualHeight = rectangle.height * rectangle.scaleY;

                                img.set({
                                    left: rectangle.left,
                                    top: rectangle.top,
                                    scaleX: actualWidth / img.width,
                                    scaleY: actualHeight / img.height,
                                    selectable: false,
                                    frameId: frame.id,
                                    rectId: rectId
                                });
                                canvas.add(img);
                                canvas.renderAll();
                                rectangle.frameImage = img;
                            });
                        }

                        popup.classList.add("hidden");
                    });
                    
                    frameContainer.appendChild(frameDiv);
                });

                popup.classList.remove("hidden");
            });
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

document.getElementById("popup-close").addEventListener("click", function () {
    document.getElementById("popup").classList.add("hidden");
});

const load = `{{ opening_project|yesno:"true,false" }}`;
console.log(load)

if (load) {
    console.log("LOADING IMAGE")
    fetch(`/get-detail-image/`)
            .then(response => response.blob())  // Get the response as a Blob
            .then(imageBlob => {
                const imageObjectURL = URL.createObjectURL(imageBlob);  // Create a URL for the blob

                // Now, let's load the image into the canvas
                const imgObj = new Image();
                imgObj.onload = function () {
                    const fabricImg = new fabric.Image(imgObj);

                    // Scale image to fit canvas
                    const scaleFactor = Math.min(
                        canvas.width / fabricImg.width,
                        canvas.height / fabricImg.height
                    );
                    fabricImg.scale(scaleFactor);

                    fabricImg.set({ selectable: false });
                    canvas.setBackgroundImage(fabricImg, canvas.renderAll.bind(canvas));
                    imageUploaded = true;
                };

                // Set the image source to the object URL of the blob
                imgObj.src = imageObjectURL;

                fetch(`/get-windows/`)
                    .then(response => response.json())
                    .then(windows => {
                        windows.forEach(window => {
                            const rect = new fabric.Rect({
                                left: window.x1,
                                top: window.y1,
                                width: window.x2 - window.x1,
                                height: window.y2 - window.y1,
                                fill: "transparent",
                                stroke: "red",
                                strokeWidth: 2,
                                selectable: true,
                                hasControls: true,
                                id: `rect-${rectangleCount++}`,
                            });
                            // console.log(rect.width)
                            // console.log(rect.height)
                            //const rectId = `rect-${rectangleCount++}`, // Assign unique rectId
                            rectangleMap[rect.id] = rect;

                            // Add the rectangle to the canvas
                            canvas.add(rect);
                            canvas.renderAll();

                            // Create and add a window button to the window list (on the left)
                            const newWindowButton = document.createElement("button");
                            newWindowButton.classList.add("window", "window-button");
                            newWindowButton.dataset.rectId = rect.id;

                            const deleteButton = document.createElement("button");
                            deleteButton.classList.add("delete-window-btn");
                            deleteButton.innerHTML = `
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg>
                            `;

                            newWindowButton.innerHTML = `Window ${rectangleCount}`;
                            newWindowButton.appendChild(deleteButton);
                            windowList.appendChild(newWindowButton);

                            // Add event listener to remove rectangle and button when clicked
                            deleteButton.addEventListener("click", function (e) {
                                const rectId = newWindowButton.dataset.rectId;
                                const rectangle = rectangleMap[rectId];

                                if (rectangle) {
                                    const frameImage = canvas.getObjects().find(obj => obj.rectId === rectId);
                                    if (frameImage) {
                                        canvas.remove(frameImage); // Remove frame image from canvas
                                    }
                                    canvas.remove(rectangle);
                                    canvas.renderAll();
                                    newWindowButton.remove();
                                    delete rectangleMap[rectId];
                                }

                                e.stopPropagation();
                            });

                            // Fetch the frame image associated with the window's frame_id
                            fetch(`/get-window-frame/${window.frame_id}/`)
                                .then(response => response.blob())
                                .then(frameImageBlob => {
                                    const frameImageObjectURL = URL.createObjectURL(frameImageBlob);
                                    const frameImgObj = new Image();

                                    frameImgObj.onload = function () {
                                        const fabricFrameImg = new fabric.Image(frameImgObj);

                                        // Scale the frame image to fit the window
                                        const actualWidth = rect.width * rect.scaleX;
                                        const actualHeight = rect.height * rect.scaleY;

                                        fabricFrameImg.set({
                                            left: rect.left,
                                            top: rect.top,
                                            scaleX: actualWidth / fabricFrameImg.width,
                                            scaleY: actualHeight / fabricFrameImg.height,
                                            selectable: false,
                                            frameId: window.frame_id,
                                            rectId: rect.id,
                                        });

                                        // Add the frame image to the canvas
                                        canvas.add(fabricFrameImg);
                                        canvas.renderAll();
                                        rect.frameImage = fabricFrameImg;
                                    };

                                    // Set the image source to the object URL of the frame image
                                    frameImgObj.src = frameImageObjectURL;
                                })
                                .catch(err => {
                                    console.error(`Error fetching frame image for window ${window.frame_id}:`, err);
                                });
                        })
                    })
                    .catch(err => {
                        console.error("Error fetching windows:", err)
                    })
            })
            .catch(err => {
                console.error("Error fetching image:", err);
            });
}