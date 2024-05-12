//
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


// Allows user to access the form to compose an email 
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


//
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


//
function view_mail(id) {

  // Show email details view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Use the API route to get all the mail details based on which mail was selected
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    // Print email details to the console (shows if there are errors or returns email details if successful)
    console.log(email);

    // Update email details view to display details of the email selected
    document.querySelector('#email-details-view').innerHTML = `
      <div class="card">
        <div class="card-header py-3 font20">
          <strong>Subject: ${email.subject}</strong>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <p><strong>From: </strong>${email.sender}</p>
            <p><strong>To: </strong>${email.recipients.join(', ')} <p>
            <p><strong>Timestamp: </strong>${email.timestamp}</p>
          </li>
          <li class="list-group-item">
            <p><strong>Email Contents:</strong></p>
            <p>${email.body}</p>
          </li>
        </ul>
      </div>
    `;

    // Mark email opened as read (if not read already)
    if (email.read == false) {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

    // Create button to reply to an email (redirects user to compose email that is prefilled)
    const replybutton = document.createElement('button');
    replybutton.innerHTML = 'Reply';
    replybutton.classList.add('p-2', 'mt-2', 'mr-2', 'btn', 'btn-primary');
    replybutton.addEventListener('click', function() {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      let subject = email.subject;
      if (subject.split(' ', 1)[0] != 'Re:') {
        subject = 'Re: ' + subject;
      }
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`
    });
    document.querySelector('#email-details-view').append(replybutton);

    // Create button to read/unread email (redirects user to the inbox mailbox)
    const readbutton = document.createElement('button');
    readbutton.innerHTML = email.read? 'Unread' : 'Read';
    readbutton.classList.add('p-2', 'mt-2', 'mr-2', 'btn', 'btn-secondary');
    readbutton.addEventListener('click', function() {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: !email.read
        })
      })
      .then( () => {
        load_mailbox('inbox')
      })
    });
    document.querySelector('#email-details-view').append(readbutton);

    // Create button to archive/unarchive email (redirects user to the archive mailbox)
    const archivebutton = document.createElement('button');
    archivebutton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
    archivebutton.className = email.archived ? 'btn-success' : 'btn-danger';
    archivebutton.classList.add('p-2', 'mt-2', 'mr-2', 'btn');
    archivebutton.addEventListener('click', function() {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then( () => {
        load_mailbox('archive')
      })
    });
    document.querySelector('#email-details-view').append(archivebutton);
  });
}


//
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 id="title">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#title').classList.add('pb-3');  

  // Use the API route to get all the mail from the mailbox chosen (inbox, sent, or archive)
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      // Print emails to the console (shows if there are errors or returns all email objects if successful)
      console.log(emails);

      // Iterate through each of the emails
      emails.forEach(email => {

        // Create div element for each email to display in the mailbox
        const emaildiv = document.createElement('div');
        emaildiv.classList.add('row', 'greyborder');
        emaildiv.innerHTML = `
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
          emaildiv.classList.add('read');
        } else {
          emaildiv.classList.add('unread');
        }

        // Add event handler for when any mail is clicked on
        emaildiv.addEventListener('click', function() {
            view_mail(email.id);
        });

        // Add each div element to the mailbox view section
        document.querySelector('#emails-view').append(emaildiv);
      });
  });
}
