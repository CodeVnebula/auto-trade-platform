import { getAccessToken, getNewAccessToken, clearStorageAndRedirect } from './tokens.js';

const BASE_URL = 'http://localhost:8000/api/'

export async function getProfile(loginUrl) {
    console.log("getProfile called")
    const accessToken = await getAccessToken(loginUrl);
    
    try {
        const response = await fetch(`${BASE_URL}myprofile/info/`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
        console.log("request sent to myprofile info")

        if (response.ok) {
            const data = await response.json();
            // console.log('Profile:', data);
            return data;
        } else if (response.status === 401) {
            console.log("Unauthorised")
            const newAccessToken = await getNewAccessToken(loginUrl);
            console.log("New access:", newAccessToken)
            const newResponse = await fetch(`${BASE_URL}myprofile/info/`, {
                method: 'GET',
                headers: { 
                    Authorization: `Bearer ${newAccessToken}`,
                },
            });
            console.log("request sent again")
            if (newResponse.ok) {
                const data = await newResponse.json();
                // console.log('Profile:', data);
                return data;
            } else {
                console.error('Failed to get profile:', newResponse.status);
            }
        } else {
            console.error('Failed to get profile:', response.status);
        }
    }
    catch (error) {
        console.error('Error getting profile:', error);
    }
}

export async function handleProfileImageChange(loginUrl, newImage) {
    console.log('image', newImage)
    const accessToken = await getAccessToken(loginUrl);
    const formData = new FormData();
    formData.append('profile_picture', newImage);

    try {
        const response = await fetch(`${BASE_URL}myprofile/profile/upload-picture/`, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
            body: formData,
        });

        if (response.ok) {
            console.log('Profile image updated first request');
            return response;
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/profile/upload-picture/`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                },
                body: formData,
            });

            if (newResponse.ok) {
                console.log('Profile image updated second request');
                return newResponse;
            } else {
                console.error('Failed to update profile image:', newResponse.status);
                alert(newResponse)
            }
        } else {
            console.error('Failed to update profile image:', response.status);
            alert(response)
        }
    }
    catch (error) {
        console.error('Error updating profile image:', error);
    }
}

export async function updateProfileInfo(loginUrl) {
    console.log("updateProfileInfo called")
    const accessToken = await getAccessToken(loginUrl);

    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;

    const data = {
        user: {
            first_name: firstName,
            last_name: lastName,
            email: "user@example.com",
            phone: phone,
            address: address,
        }
    };

    try {
        const response = await fetch(`${BASE_URL}myprofile/info/update/`, {
            method: 'PUT',
            headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            console.log('Profile updated first request');
            alert("მონაცემები წარმატებით განახლდა")
            return response;
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/info/update/`, {
                method: 'PUT',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (newResponse.ok) {
                console.log('Profile updated second request');
                alert("მონაცემები წარმატებით განახლდა")
                return newResponse;
            } else {
                console.error('Failed to update profile:', newResponse.status);
                alert(await newResponse.json())
            }
        } else {
            console.error('Failed to update profile:', response.status);
            alert(await response.json())
        }
    }
    catch (error) {
        console.error('Error updating profile:', error);
    }
}


export async function updateProfileSettings(loginUrl) {
    console.log("updateProfileInfo called")
    const accessToken = await getAccessToken(loginUrl);

    var enable_messages = document.getElementById('enable_messages').checked;
    var receive_emails = document.getElementById('receive_emails').checked;
    var receive_messages = document.getElementById('receive_messages').checked;
    var hide_email = document.getElementById('hide_email').checked;
    var hide_phone = document.getElementById('hide_phone').checked;
    var is_public = document.getElementById('is_public').checked;

    var userData = await getProfile(loginUrl);

    console.log('userdata', userData);

    const data = {
        user: {
            first_name: userData.user.first_name,
            last_name: userData.user.last_name,
            email: "user@example.com",
            phone: userData.user.phone,
            address: userData.user.address,
        },
        enable_messages: enable_messages,
        receive_messages: receive_messages,
        receive_emails: receive_emails,
        hide_email: hide_email,
        hide_phone: hide_phone,
        is_public: is_public
    };

    console.log("dataasd", data);
    try {
        const response = await fetch(`${BASE_URL}myprofile/settings/update/`, {
            method: 'PUT',
            headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            console.log('settings updated first request');
            alert("მონაცემები წარმატებით განახლდა")
            return response;
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/settings/update/`, {
                method: 'PUT',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (newResponse.ok) {
                console.log('Settings updated second request');
                alert("მონაცემები წარმატებით განახლდა")
                return newResponse;
            } else {
                console.error('Failed to update settings:', newResponse.status);
                alert(await newResponse.json())
            }
        } else {
            console.error('Failed to update settings:', response.status);
            alert(await response.json())
        }
    }
    catch (error) {
        console.error('Error updating settings:', error);
    }
}


export async function getStats(loginUrl) {
    console.log("getStats called");
    const accessToken = await getAccessToken(loginUrl);

    try {
        const response = await fetch(`${BASE_URL}myprofile/stats/`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });

        if (response.ok) {
            console.log('Profile stats fetched first request');
            const data = await response.json();  
            console.log("data-stats", data)
            return data;  
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/stats/`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                },
            });

            if (newResponse.ok) {
                console.log('Profile stats fetched second request');
                const data = await newResponse.json();  
                console.log("data-stats", data)
                return data;  
            } else {
                const errorData = await newResponse.json();
                console.error('Failed to get profile stats:', newResponse.status);
                alert(errorData);
            }
        } else {
            const errorData = await response.json();
            console.error('Failed to get profile stats:', response.status);
            alert(errorData); 
        }
    } catch (error) {
        console.error('Error while getting profile stats:', error);
    }
}

export async function getUserListings(loginUrl) {
    console.log("getMyListings called")
    const accessToken = await getAccessToken(loginUrl);

    try {
        const response = await fetch(`${BASE_URL}myprofile/mylistings/`, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });

        if (response.ok) {
            console.log('Listings fetched first request');
            const data = await response.json();
            console.log("data-listings", data)
            return data;
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/mylistings/`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                },
            });

            if (newResponse.ok) {
                console.log('Listings fetched second request');
                const data = await newResponse.json();
                console.log("data-listings", data)
                return data;
            } else {
                const errorData = await newResponse.json();
                console.error('Failed to get listings:', newResponse.status);
                alert(errorData);
            }
        } else {
            const errorData = await response.json();
            console.error('Failed to get listings:', response.status);
            alert(errorData);
        }
    } catch (error) {
        console.error('Error while getting listings:', error);
    }
}


export async function deleteAccount(loginUrl) {
    var password = document.getElementById('password').value;
    
    const data = {
        password: password
    }

    const accessToken = await getAccessToken(loginUrl);

    try {
        const response = await fetch(`${BASE_URL}myprofile/settings/delete-account/`, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            console.log('acc deleted');
            const data = await response.json();
            console.log("data-listings", data)
            return await clearStorageAndRedirect(loginUrl);
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/settings/delete-account/`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (newResponse.ok) {
                console.log('acc deleted');
                const data = await newResponse.json();
                console.log("data-listings", data)
                return await clearStorageAndRedirect(loginUrl);
            } else {
                const errorData = await newResponse.json();
                console.error('Failed to delete account:', newResponse.status);
                alert(errorData);
            }
        } else {
            const errorData = await response.json();
            console.error('Failed to delete account:', response.status);
            alert(errorData);
        }
    } catch (error) {
        console.error('Error while deleting account', error);
    }
}

export async function deactivateAccount(loginUrl) {
    var password = document.getElementById('password').value;
    
    const data = {
        password: password
    }

    const accessToken = await getAccessToken(loginUrl);

    try {
        const response = await fetch(`${BASE_URL}myprofile/settings/deactivate-account/`, {
            method: 'PUT',
            headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            console.log('acc deactivated');
            return await clearStorageAndRedirect(loginUrl);
        } else if (response.status === 401) {
            const newAccessToken = await getNewAccessToken(loginUrl);
            const newResponse = await fetch(`${BASE_URL}myprofile/settings/deactivate-account/`, {
                method: 'PUT',
                headers: {
                    Authorization: `Bearer ${newAccessToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (newResponse.ok) {
                return await clearStorageAndRedirect(loginUrl);
            } else {
                const errorData = await newResponse.json();
                console.error('Failed to deactivate account:', newResponse.status);
                alert(errorData);
            }
        } else {
            const errorData = await response.json();
            console.error('Failed to deactivate account:', response.status);
            alert(errorData);
        }
    } catch (error) {
        console.error('Error while deactivating account', error);
    }
}


export async function logout(loginUrl) {
    const refreshToken = localStorage.getItem('refresh_token');

    if (refreshToken) {
        console.log('Logging out', refreshToken);
        try {
            const response = await fetch(`${BASE_URL}auth/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: refreshToken }),
            });

            if (response.ok) {
                console.log('Logged out');
                return await clearStorageAndRedirect(loginUrl);
            } else {
                console.error('Failed to logout:', response.status);
                return await clearStorageAndRedirect(loginUrl);
            }
        } catch (error) {
            console.error('Error while logging out:', error);
            return await clearStorageAndRedirect(loginUrl);
        }
    } 
    console.error('Refresh token not found');
    return await clearStorageAndRedirect(loginUrl);
}
