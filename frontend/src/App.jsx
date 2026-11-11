import {useState} from 'react'

function App() {
  // Crea el estado username
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  function doLogin(){
    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({ username: username, password: password})
    }).then(function (reply) {
      reply.json().then(function (info){
        console.log(info);
        if(info.token){
          localStorage.setItem('token', info.token);
        }else{
          console.log("NO TOKEN FOR YOU");
        }
      })
    })
  }

  return (
    <div>
      <h1>Mi diario secreto</h1>
      {/* esto es un comentario en JSX */}
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <p>Has escrito: {username.toUpperCase()}</p>
      <button onClick={doLogin}>Iniciar sesion</button>
    </div>
  )
}

export default App