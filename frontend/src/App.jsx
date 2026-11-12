import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Entries from './pages/Entries'

function App() {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/entries" element={<Entries />} />
        </Routes>
    )
}

export default App