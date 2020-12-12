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
