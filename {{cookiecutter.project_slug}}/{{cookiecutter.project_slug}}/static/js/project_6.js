


const full_name_valid = () => {
    let valid = false;
    const min = 5, max = 30;
    const full_name = $('#full_name').val().trim();
    if (!isRequired(full_name)) {
        $('#error_text_full_name').text(" Full name cannot be blank.");
    } else if (!isBetween(full_name.length, min, max)) {
        $('#error_text_full_name').text(` Full name must be between ${min} and ${max} characters.`);
    } else {
        valid = true;
        $('#error_text_full_name').text(``);
    }
    return valid;
};


const email_valid = () => {
  let valid = false;
  const email = $('#email').val().trim();
  if (!isRequired(email)) {
    $('#error_text_email').text(" Email cannot be blank.");
  } else if (!isEmailValid(email)) {
    $('#error_text_email').text(` Email does not appear to be valid.`);
  } else {
      valid = true;
      $('#error_text_email').text(``);
  }
  return valid;
};



const message_valid = () => {
  let valid = false;
  const min = 50, max = 5000;
  const message = $('#message').val().trim();
  if (!isRequired(message)) {
    $('#error_text_message').text(" Message cannot be blank.");
  } else if (!isBetween(message.length, min, max)) {
    $('#error_text_message').text(` Message must be between ${min} and ${max} characters.`);
  } else {
      valid = true;
      $('#error_text_message').text(``);
  }
  return valid;
};


const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};

const isRequired = value => value === '' ? false : true;
const isBetween = (length, min, max) => length < min || length > max ? false : true;


const showError = (input, message) => {
    // get the form-field element
    const formField = input.parentElement;

    // show the error message
    const error = formField.querySelector('small');
    error.textContent = message;
};

const showSuccess = (input) => {
  // get the form-field element
  const formField = input.parentElement;

  // show the error message
  const success = formField.querySelector('small');
  success.textContent = "";
};


const debounce = (fn, delay = 1200) => {
    let timeoutId;
    return (...args) => {
        // cancel the previous timer
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        // setup a new timer
        timeoutId = setTimeout(() => {
            fn.apply(null, args)
        }, delay);
    };
};


$(document).ready(function(){
if ( page_title_one == 'contact-us' ) {


  $("#employment_switch").click(function(){
     $(".div_employment").toggleClass("hidden");
  });

var send_message = document.getElementById("send_message");
send_message.addEventListener("click", function(event) {

  var is_full_name_valid = full_name_valid();
  var is_email_valid = email_valid();
  var is_message_valid = message_valid();

  let is_form_valid = is_full_name_valid &&
  is_email_valid &&
  is_message_valid;

  // submit to the server if the form is valid
  if (is_form_valid) {

    event.preventDefault();

    var full_name = $('#full_name').val();
    var email = $('#email').val();
    var message = $('#message').val();

    $.ajax({
      headers: { "X-CSRFToken": csrftoken },
      type: "POST",
      url: window.location.href,
      data: {
        csrfmiddlewaretoken : csrftoken,
        'type': "send_message",
        'full_name': full_name,
        'email': email,
        'message': message,
      },
      success: function (resp) {
        if (resp.result == "FAILURE"){
          $('#modalMailFail').modal('show');
        } else {
          $('#modalMailSent').modal('show');
          createConfetti("modal-message-sent", 500);
        }
      },
      error: function () {
          console.log("Error during refresh");
      }
    });
  }

});

var contact_me_form = document.getElementById("contact_me_form");
contact_me_form.addEventListener('input', debounce(function (e) {
  console.log(e.target.id, e);
  switch (e.target.id) {

    case 'full_name': 
      full_name_valid();
      break;
    case 'email': 
      email_valid();
      break;
    case 'message': 
      message_valid();
      break;

  }
}));

}

});
