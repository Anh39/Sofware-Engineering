import LayoutDefault from "../LayoutDefault";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Logout from "../pages/Logout";
import Register from "../pages/Register";
import SavedText from "../pages/SavedText";
import TransDocs from "../pages/TransDocs";

export const routes = [
    // Public
    {
        path: "/",
        element: <LayoutDefault />,
        children: [
            {
                path: "/",
                element: <Home />,
                children: [
                    {
                        path: "/docs",
                        element: <TransDocs />
                    }
                ]
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
                path: "/saved",
                element: <SavedText />
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