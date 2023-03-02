// Get a reference to the video element
const video = document.getElementById("video");
console.log("Started");
// Get a reference to the start button
const startButton = document.getElementById("start-button");
const stopButton = document.getElementById("stop-button");

// Create an XMLHttpRequest object
const xhr = new XMLHttpRequest();

// Function to start the stream
function startStream() {
  // Send a request to the server to start the stream
  xhr.open("POST", "/start_stream", true);
  xhr.send();
}

// Function to stop the stream
function stopStream() {
  // Send a request to the server to stop the stream
  xhr.open("POST", "/stop_stream", true);
  xhr.send();
}

// Add an event listener to the start button to start the stream
startButton.addEventListener("click", startStream);
stopButton.addEventListener("click", stopStream);
