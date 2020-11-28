// Functions for filling the form

// Disable form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {

    // Get the forms we want to add validation styles to
    var forms = document.getElementsByClassName('needs-validation');

    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

// Get name of file
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});


// Functions related to invite container

// add invite field
function addInviteField() {

  // get invite container #invite
  const container = document.querySelector("#invite");

  // get duplication container #invite
  const fieldsContainer = document.querySelectorAll("#invite");

  // Clone last added invite
  const newFieldContainer = fieldsContainer[
    fieldsContainer.length -1
  ].cloneNode(true);
  const input = newFieldContainer.children[0];
  if (input.value == "") {
    return;
  }

  // Clean field
  input.value = "";

  // delete close button
  if (fieldsContainer.length === 1) {
  const close = document.querySelector("#close")
  close.remove()
   }

  // Add clone to container #invite
  container.appendChild(newFieldContainer);

}

// Deleting containers
function deleteField() {
  const span = event.currentTarget;

  const fieldsContainer = document.querySelectorAll("#invite");

  if (fieldsContainer.length <= 2) {

    // Delete field value
    span.parentNode.value = "";
    return;

  } else {

  // delete field
  span.parentNode.remove();
  }

}