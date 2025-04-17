const video = document.getElementById('video');
const videocon = document.getElementById('video-container');
const capturedImage = document.getElementById('captured-image');
const snap = document.getElementById('snap');
const retake = document.getElementById('retake');
const save = document.getElementById('save');
const predict = document.getElementById('predict');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(function(stream) {
    video.srcObject = stream;
    video.play();
  })
  .catch(function(err) {
    console.error('Error accessing camera:', err);
  });

snap.addEventListener('click', function() {
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  capturedImage.src = canvas.toDataURL('image/jpeg');
  capturedImage.style.width = video.offsetWidth + 'px';
  capturedImage.style.height = video.offsetHeight + 'px';
  video.style.display = 'none';
  capturedImage.style.display = 'block';
  snap.style.display = 'none';
  retake.style.display = 'inline-block';
  save.style.display = 'inline-block';
  videocon.style.borderColor = '#008000';
});

retake.addEventListener('click', function() {
  video.style.display = 'block';
  capturedImage.style.display = 'none';
  snap.style.display = 'inline-block';
  retake.style.display = 'none';
  save.style.display = 'none';
  predict.style.display = 'none';
  predictedImage.src = '';
});

save.addEventListener('click', function() {
  const imgData = capturedImage.src;
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/save_image', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        alert('Image saved successfully.');
        predict.style.display = 'inline-block';
      } else {
        console.error('Failed to save image.');
      }
    }
  };
  xhr.send(JSON.stringify({ image: imgData }));
});

function displayPredictionResult(result) {
  alert('Prediction: ' + result);
}


// Hide the predicted image initially
// const predictedImage = document.getElementById('predictedImage');
// predictedImage.style.display = 'none';

// predict.addEventListener('click', function() {
//   // Get the base64 encoded image data from the captured image
//   const imgData = capturedImage.src;
//   // Send the image data to the server for prediction
//   fetch('/predict_image', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ image: imgData })
//   })
//   .then(response => response.json())
//   .then(data => {
//     if (data.status === 'success') {
//       // Show the predicted image on the webpage
//       predictedImage.src = '/results/result_image.jpg'; // Update image source
//       predictedImage.style.display = 'block'; // Display the predicted image
//       // Show the "Retake" button
//       retake.style.display = 'inline-block';

//       // Hide the captured image and the "Save" button
//       capturedImage.style.display = 'none';
//       save.style.display = 'none';
//     } else {
//       console.error('Failed to predict image:', data.message);
//     }
//   })
//   .catch(error => {
//     console.error('Error predicting image:', error);
//   });
// });
const predictedImage = document.getElementById('predictedImage');
predictedImage.style.display = 'none';

predict.addEventListener('click', function() {
  // Get the base64 encoded image data from the captured image
  const imgData = capturedImage.src;
  
  // Send the image data to the server for prediction
  fetch('/predict_image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imgData })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Show the predicted image on the webpage
      predictedImage.src = '/results/' + data.image_name;
      predictedImage.style.display = 'block'; // Display the predicted image

      // Show the "Retake" button
      retake.style.display = 'inline-block';

      // Hide the captured image and the "Save" button
      capturedImage.style.display = 'none';
      save.style.display = 'none';
    } else {
      console.error('Failed to predict image:', data.message);
    }
  })
  .catch(error => {
    console.error('Error predicting image:', error);
  });
});
