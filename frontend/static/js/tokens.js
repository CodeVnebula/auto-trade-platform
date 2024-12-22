const BASE_URL = 'http://localhost:8000/api/'

export async function getAccessToken(loginUrl) {
    console.log('get access token called')
    try {
        const accessToken = localStorage.getItem('access_token');
        console.log(accessToken);

        if (accessToken) {
            console.log('Access token found:', accessToken);
            return accessToken;
        } else {
            console.error('Access token not found');
            clearStorageAndRedirect(loginUrl);
        }
    } 
    catch (error) {
        console.error('Error getting access token:', error);
        clearStorageAndRedirect(loginUrl);
    }
}

export async function getNewAccessToken(loginUrl) {
    console.log('get new access token called')
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    console.log(accessToken, refreshToken);

    if (accessToken && refreshToken) {
        try {
            const response = await fetch(`${BASE_URL}auth/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: refreshToken }) 
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.clear();

                console.log('Token refreshed:', data.access);

                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                
                return data.access;
            } else {
                console.error('Failed to refresh token:', response.status);
                clearStorageAndRedirect(loginUrl);
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            clearStorageAndRedirect(loginUrl);
        }
    } else {
        console.error('Access or refresh token not found');
        clearStorageAndRedirect(loginUrl);
    }
}

export async function clearStorageAndRedirect(loginUrl) {
    console.log('Clearing cookies and redirecting to login');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = loginUrl;
}
