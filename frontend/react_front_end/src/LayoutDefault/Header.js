import { Button } from "antd";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import Personal from "../components/Personal";
import { getCookie } from "../helpers/cookie";

function Header() {
    const token = getCookie("token");
    const isLogin = useSelector(state => state.loginReducer);

    console.log(isLogin);

    return (
        <>
            <div className="header">
                <div className="header__logo">
                    <Link to="/">Translator</Link>
                </div>

                <div className="header__button">
                    {token ? (
                        <>
                            <Personal />
                        </>
                    ) : (
                        <>
                            <Button className="header__button--login" type="primary">
                                <Link to="/login">Đăng nhập</Link>
                            </Button>
                            <Button className="header__button--register">
                                <Link to="/register">Đăng kí</Link>
                            </Button>
                        </>
                    )}
                </div>
            </div>
        </>
    )
}

export default Header;