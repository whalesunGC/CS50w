document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Send email on submit
  document.querySelector('#compose-form').onsubmit = send_email;
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Populate Reply
  if (email) {
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:`;
    
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  

  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h2>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h2>`;

  // Fetch emails from the specified mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    const emailList = document.createElement('div');
    emails.forEach(email => {
      const emailItem = document.createElement('button');
      emailItem.innerHTML = `<p>${email.sender} ${email.subject} ${email.timestamp}</p>`;

       // Set the border and background color based on email.read
      emailItem.style.border = '1px solid black';
      if (email.read) {
        emailItem.style.backgroundColor = 'grey';
      } else {
        emailItem.style.backgroundColor = 'white';
      }

      // Add a click event listener to the email item
      emailItem.addEventListener('click', () => {display_email(email.id);});

      emailList.appendChild(emailItem);
    });
    document.querySelector('#emails-view').appendChild(emailList);
  });
}

function send_email() {
// Prevent default form submission
event.preventDefault();

//Send email via /emails
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  });
}

function display_email(id) {
  const emailId = parseInt(id);
  if (!emailId) {
    console.error(`Invalid email ID: ${id}`);
    return;
  }

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      const emailView = document.querySelector('#emails-view');
      emailView.innerHTML = '';
      const emailItem = document.createElement('div');
      // Create elements for each key-value pair in the email object
      Object.keys(email).forEach(key => {
        // Exclude "id", "read", and "archived" keys
        if (key === "id" || key === "read" || key === "archived") {
          return;
        }

        const emailLabel = document.createElement('span');
        emailLabel.style.fontWeight = "bold";
        emailLabel.textContent = `${key}: `;

        const emailValue = document.createElement('span');
        emailValue.textContent = email[key];

        const emailPair = document.createElement('div');
        emailPair.style.marginBottom = "5px";
        emailPair.appendChild(emailLabel);
        emailPair.appendChild(document.createTextNode("\u00A0")); // Add a non-breaking space
        emailPair.appendChild(emailValue);

        emailItem.appendChild(emailPair);
      });
      emailView.appendChild(emailItem);
      
      //add atchive function
      const archiveButton = document.createElement('button');
      if (email.archived) {
        archiveButton.textContent = 'Unarchive';
      } else {
        archiveButton.textContent = 'Archive';
      }
      archiveButton.addEventListener('click', () => archieve_toggle(email))
      
      emailView.appendChild(archiveButton)
      
      // add reply function
      const replyButton = document.createElement('button');
      replyButton.textContent = 'Reply'
      replyButton.addEventListener('click', () => compose_email(email))
      emailView.appendChild(replyButton)

      // Mark email as read if it was unread
      if (!email.read) {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });
      }
    });
}

function archieve_toggle(email) {
  const newArchiveStatus = !email.archived;
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: newArchiveStatus
    })
  })
  .then(response => response.status)
  .then(result => {
    if (result === 204) {
      email.archived = newArchiveStatus;
      load_mailbox('inbox');
    } else {
      throw new Error('Failed to update email archive status.')
    }
  });
}
