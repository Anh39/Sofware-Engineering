import { Button } from "antd";
import { Link } from "react-router-dom";

// Laptop gaming, đồ họa

function Header(props) {
    const { token } = props;

    return (
        <>
            <div className="header">
                <div className="header__logo">
                    <Link to="/">Translator</Link>
                </div>

                <div className="header__button">
                    {token ? (
                        <>
                            <Button className="header__button--login" type="primary">
                                bản dịch đã lưu
                            </Button>
                            <Button className="header__button--register">
                                <Link to="/logout">Đăng xuất</Link>
                            </Button>
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