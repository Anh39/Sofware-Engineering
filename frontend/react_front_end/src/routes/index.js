import LayoutDefault from "../LayoutDefault";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Logout from "../pages/Logout";
import Register from "../pages/Register";
import ResetPassword from "../pages/ResetPassword";

export const routes = [
    // Public
    {
        path: "/",
        element: <LayoutDefault />,
        children: [
            {
                path: "/",
                element: <Home />
            },
            {
                path: "/login",
                element: <Login />
            },
            {
                path: "/register",
                element: <Register />
            },
            {
                path: "/resetpassword",
                element: <ResetPassword />
            },
            {
                path: "/logout",
                element: <Logout />
            },
            {
                path: "*",
                element: <h1>404</h1>
            }
        ]
    }
]