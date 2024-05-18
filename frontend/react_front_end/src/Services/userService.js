import { get, patch, post } from "../utils/request";

export const entry = async () => {
    const result = await post('entry');
    return result;
}

export const login = async (options) => {
    const result = await post('login',options);
    return result;
}

export const getHistory = async (options) => {
    const result = await get('history?start_from=0&amount=10');
    return result;
}

export const getSaved = async (options) => {
    const result = await get('saved');
    return result;
}

export const saveRecord = async (options) => {
    const result = await patch('save',options);
    return result;
}

export const register = async (options) => {
    const result = await post("register", options);
    return result;
}

export const checkExists = async (key, value) => {
    const result = await get(`users?${key}=${value}`);
    return result;
}

export const translateTextServer = async (options) => {
    const result = await post('translate/text', options);
    return result;
}