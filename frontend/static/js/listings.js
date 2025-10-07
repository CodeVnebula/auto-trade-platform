import { getAccessToken, getNewAccessToken } from './tokens.js';

const BASE_URL = 'http://localhost:8000/api/'

// export async function getProfile(loginUrl) {
//     console.log("getProfile called")
//     const accessToken = await getAccessToken(loginUrl);
    
//     try {
//         const response = await fetch(`${BASE_URL}car-listings/config-data/`, {
//             method: 'GET',
//             headers: {
//                 Authorization: `Bearer ${accessToken}`,
//             },
//         });
//         console.log("request sent to myprofile info")

//         if (response.ok) {
//             const data = await response.json();
//             // console.log('Profile:', data);
//             return data;
//         } else if (response.status === 401) {
//             console.log("Unauthorised")
//             const newAccessToken = await getNewAccessToken(loginUrl);
//             console.log("New access:", newAccessToken)
//             const newResponse = await fetch(`${BASE_URL}car-listings/config-data/`, {
//                 method: 'GET',
//                 headers: { 
//                     Authorization: `Bearer ${newAccessToken}`,
//                 },
//             });
//             console.log("request sent again")
//             if (newResponse.ok) {
//                 const data = await newResponse.json();
//                 // console.log('Profile:', data);
//                 return data;
//             } else {
//                 console.error('Failed to get profile:', newResponse.status);
//             }
//         } else {
//             console.error('Failed to get profile:', response.status);
//         }
//     }
//     catch (error) {
//         console.error('Error getting profile:', error);
//     }
// }

export async function getConfigData() {
    console.log("getConfigData called")
    
    try {
        const response = await fetch(`${BASE_URL}car-listings/config-data/`, {
            method: 'GET',
        });
        console.log("request sent to get config data")

        if (response.ok) {
            const data = await response.json();
            console.log('Config Data:', data);
            return data;
        } else {
            console.error('Failed to get data:', response.status);
        }
    }
    catch (error) {
        console.error('Error getting profile:', error);
    }
}
