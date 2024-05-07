import { useNavigate } from "react-router-dom";
// import {useDispatch} from "react-redux";
import { useEffect } from "react";

function Logout() {
    const navigate = useNavigate();
    // const dispatch = useDispatch();

    useEffect(() => {
        // dispatch({type: "LOGOUT"});
        navigate("/");
    })
    return (
        <></>
    )
}

export default Logout;