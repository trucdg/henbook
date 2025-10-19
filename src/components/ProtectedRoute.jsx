// We need an authentication access token to access this routes
import {Navigate} from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';
import api from '../api';
import { REFRESH_TOKEN, ACCESS_TOKEN} from '../constants';
import {useState, useEffect} from 'react';

function ProtectedRoute({children}) {
    const [isAuthorized, setIsAuthorized] = useState(null)
    useEffect(() => {
        auth().catch((error) => {
            console.log('Error during auth', error);
            setIsAuthorized(false);
        });
    }, []);

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            // send a request to backend to get a refreshed access token
            const res = await api.post('api/token/refresh/', {
                refresh: refreshToken
            });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthorized(true);
            } else {
                setIsAuthorized(false);
            }

        } catch (error) {
            console.log('Error refreshing token', error);
            setIsAuthorized(false);
        }
    }

    const auth = async () => {
        // check if we have access token
        // if not, try to refresh
        const accessToken = localStorage.getItem(ACCESS_TOKEN);
        if (!accessToken) {
            setIsAuthorized(false);
            return ;
        }
        const decodedToken = jwtDecode(accessToken);
        const tokenExpiration = decodedToken.exp
        const now = Date.now() / 1000; // in seconds

        if (tokenExpiration < now) {
            // token expired, try to refresh
            await refreshToken();
        } else {
            // token valid
            setIsAuthorized(true);
        }
    }

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }
    
    return isAuthorized ? children : <Navigate to="/login" />;

}

export default ProtectedRoute;