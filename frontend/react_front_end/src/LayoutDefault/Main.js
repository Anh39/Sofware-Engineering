import { Outlet } from "react-router-dom";

function Main(props) {
    return (
        <>
            <div className="main">
                <Outlet />
            </div>
        </>
    );
}

export default Main;