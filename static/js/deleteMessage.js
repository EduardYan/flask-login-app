/**
 * This is a script for delete the message, when
 * the password is incorrect,
 * or other funcionalilty.
 */

// after of 3 seconds
setTimeout(() => {
  const message = document.getElementById('message');
  const container = document.querySelector('.messages-view').remove(message);

}, 3000)