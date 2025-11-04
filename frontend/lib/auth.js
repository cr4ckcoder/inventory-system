import Cookies from "js-cookie";

const TOKEN_NAME = process.env.NEXT_PUBLIC_JWT_COOKIE_NAME || "access_token";

export const setToken = (token) => {
  Cookies.set(TOKEN_NAME, token, { expires: 7 }); // store for 7 days
};

export const getToken = () => Cookies.get(TOKEN_NAME);

export const clearToken = () => {
  Cookies.remove(TOKEN_NAME);
};
