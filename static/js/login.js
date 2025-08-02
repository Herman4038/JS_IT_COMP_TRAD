// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.getElementById('login-form').addEventListener('submit', async e => {
  e.preventDefault();  // Prevent default form submission
  const form = e.target;
  
  // Create FormData object to send as regular form data (not JSON)
  const formData = new FormData(form);

  try {
    const resp = await fetch(form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: formData,
    });

    if (resp.ok) {
      // Check if the response is a redirect
      if (resp.redirected) {
        window.location.href = resp.url;
      } else {
        // If not redirected, check if login was successful
        const responseText = await resp.text();
        if (responseText.includes('dashboard') || responseText.includes('error')) {
          // If there's an error message in the response, show it
          if (responseText.includes('error')) {
            alert('Login failed: Invalid credentials');
          } else {
            window.location.href = '/dashboard/';
          }
        } else {
          window.location.href = '/dashboard/';
        }
      }
    } else {
      alert('Login failed: ' + resp.statusText);
    }
  } catch (error) {
    console.error('Login error:', error);
    alert('Login failed: Network error');
  }
});
