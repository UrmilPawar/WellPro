//Firebase configuration
// const firebaseConfig = {
//   apiKey: "AIzaSyAlV4nMJVTFD030Nl2etkmffW-HhL3UHDg",
//   authDomain: "clicker-8eea7.firebaseapp.com",
//   projectId: "clicker-8eea7",
//   storageBucket: "clicker-8eea7.appspot.com",
//   messagingSenderId: "353336672590",
//   appId: "1:353336672590:web:0abff7fd0add7e82f49e1f",
//   measurementId: "G-8NM617G7L9"
// };

// // Initialize Firebase
// firebase.initializeApp(firebaseConfig);

const form = document.querySelector('form[name="contact-form"]');
const submitButton = document.querySelector('button[type="submit"]');

submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    
    const formData = new FormData(form);
    console.log(formData.get('name'));
    console.log(formData.get('phone_number'));
    console.log(formData.get('email'));
    console.log(formData.get('message'));
    
    fetch('http://127.0.0.1:5004/contacts', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            name: formData.get('name'),
            phone_number: formData.get('phone_number'),
            email: formData.get('email'),
            message: formData.get('message')
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        form.reset();
    })
    .catch(error => {
        console.error(error);
        alert('Oops! Something went wrong.');
    });
});