// static/js/login.js
document.getElementById('login-form').addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    const data = {
      username: form.username.value,
      password: form.password.value,
    };
    const resp = await fetch(form.action, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(data),
    });
    if (resp.ok) {
      window.location.href = '/dashboard/';
    } else {
      alert('Login failed');
    }
  });
  
  function getCookie(name) {
    return document.cookie.split('; ')
      .find(row => row.startsWith(name + '='))
      ?.split('=')[1];
  }
  