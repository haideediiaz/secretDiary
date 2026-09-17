import {useState} from 'react'

function App() {
  // Crea el estado username
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  return (
    <div>
      <h1>Mi diario secreto</h1>
      {/* esto es un comentario en JSX */}
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <p>Has escrito: {username.toUpperCase()}</p>
      <button onClick={() => console.log(username, password)}>Iniciar sesion</button>
    </div>
  )
}

export default App