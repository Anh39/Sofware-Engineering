import { getCookie } from "../helpers/cookie";
const API_DOMAIN = "http://127.0.0.1:8081/"; // đổi tại đây


export const get = async (path) => {
    const response = await fetch(API_DOMAIN + path, {
        method : "GET",
        headers : {
            "Token" : getCookie('token')
        }
    });
    return response;
};

export const post = async (path, option) => {
    const response = await fetch(API_DOMAIN + path, {
        method: "POST",
        credentials: "include",
        headers: {
            "Token" : getCookie('token'),
            // Accept: "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(option)
    });

    return response;
};

export const del = async (path) => {
    const response = await fetch(API_DOMAIN + path, {
        method: 'DELETE',
        headers : {
            "Token" : getCookie('token')
        }
    });
    const result = await response.json();
    return result;
}

export const patch = async (path, option) => {
    const response = await fetch(API_DOMAIN + path, {
        method: "PATCH",
        headers: {
            // Accept: "application/json",
            "Content-Type": "application/json",
            "Token" : getCookie('token'),
        },
        body: JSON.stringify(option)
    });
    const result = await response.json();
    return result;
}