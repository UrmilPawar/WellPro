const form = document.getElementById("upload-form");
const input = document.getElementById("image-input");
const resultDiv=document.getElementById("result")

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData();
  formData.append("image", input.files[0]);//getting the 1st file of the input variable

  fetch("http://127.0.0.1:5000/predict2", {
    method: "POST",
    body: formData,
  })
    .then(response => response.json())
    .then((data) => {
        // Getting the disease name from the response
        const disease = data.disease;
        
        // Calling the /wiki endpoint to get additional information
        fetch('http://127.0.0.1:5003/wiki', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({disease_name: disease})
        })
        .then(response => response.json()) //takes the raw response from the server and converts it into a JSON object.
        .then(data => {
          // Displaying the additional information
          let additional;
          if(data.additional.length==0){
            additional="Additional information about the disease cannot be retreived";
          }
          else{
              additional = data.additional.filter(info => info.trim() !== '').map(info => `<li>${info}</li>`).join(''); //join('') indicates that the strings should be joined by nothing <li>apple</li><li>banana</li><li>orange</li>
              //filter() function is used to remove any empty strings from the additional array before calling map() function on it. 
            }
          resultDiv.innerHTML = `
          <div class="predicted-disease">Predicted disease: <b>${disease}</b></div>
          <div class="additional-info"><ul>${additional}</ul></div>`;
          //Here, data.additional is an array of strings, where each string represents a piece of information about the predicted disease. The map function is used to iterate through each element of the array and create a new array of strings with each string wrapped in <li> and </li> tags. For example, if data.additional is ['symptom 1', 'symptom 2', 'symptom 3'], then additional will be the string '<li>symptom 1</li><li>symptom 2</li><li>symptom 3</li>'.
          //The join function is then used to join these strings together with an empty string as a separator. This results in a single string where each individual string is separated by nothing. The resulting string is then inserted into an unordered list element using the ${additional} template string syntax, which creates an unordered list with each element of the list separated by bullet points.

        })
        .catch(error => console.error(error));
            resultDiv.innerHTML = `<p>Predicted disease: ${data.disease}</p>`;
          // handling the response data here
    })
    .catch((error) => {
      console.error("Error:", error);
      // handle the error here
    });
});
























// const form = document.getElementById("upload-form");
// const input = document.getElementById("image-input");
// const resultDiv=document.getElementById("result")

// form.addEventListener("submit", (event) => {
//   event.preventDefault();
//   const formData = new FormData();
//   formData.append("image", input.files[0]);

//   fetch("http://127.0.0.1:5000/predict2", {
//     method: "POST",
//     body: formData,
//   })
//     .then(response => response.json())
//     .then((data) => {
//         // Getting the disease name from the response
//         const disease = data.disease;
        
//         // Calling the /wiki endpoint to get additional information
//         fetch('http://127.0.0.1:5003/wiki', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json'
//           },
//           body: JSON.stringify({disease_name: disease})
//         })
//         .then(response => response.json())
//         .then(data => {
//           // Displaying the additional information
//           const additional = data.additional.join('<br>');
//           resultDiv.innerHTML = `<p>Predicted disease: ${disease}</p><p>Additional information:</p><p>${additional}</p>`;
//         })
//         .catch(error => console.error(error));
//             resultDiv.innerHTML = `<p>Predicted disease: ${data.disease}</p>`;
//           // handling the response data here
//     })
//     .catch((error) => {
//       console.error("Error:", error);
//       // handle the error here
//     });
// });