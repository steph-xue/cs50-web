document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Detects if the compose new email form was submitted to send an email
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function send_email(event) {

  event.preventDefault();

  // Gets information submitted in the compose email form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send information to the backend to create and save new email objects (sent by the user)
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {

    // Print result to the console (shows if there are errors or if the email was sent successfully)
    console.log(result);

    // Redirects user to the sent inbox
    load_mailbox('sent');

  });

}


function view_mail(id) {

  // Show email details view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  pass
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Use the API route to get all the mail from the mailbox chosen (inbox, sent, or archive)
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      // Print emails to the console (shows if there are errors or returns all email objects if successful)
      console.log(emails);

      // Iterate through each of the emails
      emails.forEach(email => {

        // Create div element for each email to display in the mailbox
        const mail = document.createElement('div');
        mail.classList.add('row', 'greyborder');
        mail.innerHTML = `
          <div class="col py-3">
            <strong>${email.sender}</strong>
          </div>
          <div class="col-6 py-3">
            ${email.subject}
          </div>
          <div class="col py-3 text-right greytext">
            ${email.timestamp}
          </div>
        `;

        // Determines if email background color is white (unread) or grey (read)
        if (email.read == true) {
          mail.classList.add('read');
        } else {
          mail.classList.add('unread');
        }

        // Add event handler for when any mail is clicked on
        mail.addEventListener('click', function() {
            view_mail(mail.id);
        });

        // Add each div element to the mailbox view section
        document.querySelector('#emails-view').append(mail);
      });
  });
}
