import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useEffect } from "react";
import { deleteAllCookie } from "../../helpers/cookie";
import { checkLogin } from "../../actions/login";

function Logout() {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    deleteAllCookie();

    useEffect(() => {
        dispatch(checkLogin(false));
        navigate("/login");
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <></>
    )
}

export default Logout;