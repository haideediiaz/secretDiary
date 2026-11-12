import { useEffect } from 'react';
import {useNavigate} from 'react-router-dom';

function Entries() {
    const navigate = useNavigate()

    useEffect(() => {
        // aquí: si no hi ha token, navigate('/login')
        if(!localStorage.getItem('token')){
            navigate('/login');
        }
    }, [])

    return (
        <p>Sesion iniciada</p>
    )
}
export default Entries;