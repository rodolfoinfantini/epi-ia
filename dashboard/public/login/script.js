const form = document.querySelector('form')
form.onsubmit = async (e) => {
    e.preventDefault()

    const [email, password] = e.target

    const response = await fetch('/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    })
    if (response.status === 401) {
        alert('E-mail ou senha inválidos')
        return
    }

    const token = await response.json()
    localStorage.setItem('token', token.token)
    location.href = '/'
}
